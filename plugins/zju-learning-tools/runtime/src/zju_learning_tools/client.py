from __future__ import annotations

from contextlib import contextmanager
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
import threading
import time
from typing import Any, Iterator
from urllib.parse import urljoin, urlparse

import httpx

from .constants import (
    ALLOWED_HOSTS,
    AUTH_HOSTS,
    MAX_REDIRECTS,
    READ_METHODS,
    REQUEST_INTERVAL_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    USER_AGENT,
)
from .errors import AuthenticationRequired, DownloadRejected, UpstreamChanged, ZJUError
from .security import require_allowed_url, safe_destination
from .session import SessionStore


class _Limiter:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._last = 0.0
        self._slots = threading.BoundedSemaphore(2)

    @contextmanager
    def acquire(self) -> Iterator[None]:
        with self._slots:
            with self._lock:
                wait = REQUEST_INTERVAL_SECONDS - (time.monotonic() - self._last)
                if wait > 0:
                    time.sleep(wait)
                self._last = time.monotonic()
            yield


_LIMITER = _Limiter()


class ZJUReadClient:
    def __init__(self) -> None:
        self.store = SessionStore()
        self.payload = self.store.load()
        self.clients = {
            service: httpx.Client(
                cookies=self.store.cookies(service),
                headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/plain, */*"},
                follow_redirects=False,
                timeout=REQUEST_TIMEOUT_SECONDS,
                trust_env=False,
            )
            for service in ("courses", "classroom")
        }

    def _client_for(self, url: str) -> httpx.Client:
        if hasattr(self, "client"):  # Injected only by isolated MockTransport tests.
            return self.client
        host = (urlparse(url).hostname or "").lower()
        return self.clients["courses" if host == "courses.zju.edu.cn" else "classroom"]

    def close(self) -> None:
        if hasattr(self, "client"):
            self.client.close()
            return
        for client in self.clients.values():
            client.close()

    def __enter__(self) -> "ZJUReadClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _send(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        method = method.upper()
        if method not in READ_METHODS:
            raise ZJUError("method_rejected", "Campus-side write methods are not available in this plugin.")
        current = require_allowed_url(url)
        for _ in range(MAX_REDIRECTS + 1):
            with _LIMITER.acquire():
                try:
                    response = self._client_for(current).request(method, current, **kwargs)
                except httpx.TimeoutException as exc:
                    raise ZJUError("upstream_timeout", "The ZJU service timed out.", retryable=True) from exc
                except httpx.RequestError as exc:
                    raise ZJUError("network_error", "The ZJU service could not be reached.", retryable=True) from exc
            if response.status_code not in {301, 302, 303, 307, 308}:
                return response
            location = response.headers.get("location")
            if not location:
                raise UpstreamChanged("A ZJU service returned a redirect without a destination.")
            current = require_allowed_url(urljoin(str(response.url), location))
            if (urlparse(current).hostname or "").lower() in AUTH_HOSTS:
                raise AuthenticationRequired()
        raise ZJUError("redirect_limit", "The ZJU service exceeded the safe redirect limit.")

    def get_json(self, url: str, *, params: dict[str, Any] | None = None) -> Any:
        response = self._send("GET", url, params=params)
        if response.status_code in {401, 403}:
            raise AuthenticationRequired()
        if response.status_code == 429:
            retry_after = response.headers.get("retry-after", "later")
            raise ZJUError("rate_limited", f"ZJU rate-limited the request; retry after {retry_after}.", retryable=True)
        if response.status_code >= 400:
            raise ZJUError("upstream_error", f"The ZJU service returned HTTP {response.status_code}.", retryable=response.status_code >= 500)
        content_type = response.headers.get("content-type", "").lower()
        if "json" not in content_type:
            if "text/html" in content_type:
                raise AuthenticationRequired()
            raise UpstreamChanged("The ZJU service returned an unexpected response type.")
        try:
            return response.json()
        except ValueError as exc:
            raise UpstreamChanged("The ZJU service returned malformed JSON.") from exc

    @contextmanager
    def stream_get(self, url: str) -> Iterator[httpx.Response]:
        current = require_allowed_url(url)
        response: httpx.Response | None = None
        try:
            for _ in range(MAX_REDIRECTS + 1):
                client = self._client_for(current)
                request = client.build_request("GET", current)
                with _LIMITER.acquire():
                    try:
                        response = client.send(request, stream=True)
                    except httpx.TimeoutException as exc:
                        raise ZJUError("upstream_timeout", "The ZJU service timed out.", retryable=True) from exc
                    except httpx.RequestError as exc:
                        raise ZJUError("network_error", "The ZJU service could not be reached.", retryable=True) from exc
                if response.status_code not in {301, 302, 303, 307, 308}:
                    yield response
                    return
                location = response.headers.get("location")
                response.close()
                response = None
                if not location:
                    raise UpstreamChanged("A ZJU download returned a redirect without a destination.")
                current = require_allowed_url(urljoin(current, location))
                if (urlparse(current).hostname or "").lower() in AUTH_HOSTS:
                    raise AuthenticationRequired()
            raise ZJUError("redirect_limit", "The ZJU service exceeded the safe redirect limit.")
        finally:
            if response is not None:
                response.close()

    def courses(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        if not path.startswith("/") or ".." in path:
            raise ZJUError("path_rejected", "An internal endpoint path was rejected.")
        return self.get_json(f"https://courses.zju.edu.cn{path}", params=params)

    def classroom(self, path: str, *, params: dict[str, Any] | None = None, host: str = "classroom.zju.edu.cn") -> Any:
        if host not in ALLOWED_HOSTS or not path.startswith("/") or ".." in path:
            raise ZJUError("path_rejected", "An internal endpoint path was rejected.")
        return self.get_json(f"https://{host}{path}", params=params)

    def download_upload(
        self,
        upload_id: str,
        *,
        destination_root: str,
        filename: str,
        max_bytes: int,
    ) -> dict[str, Any]:
        if not str(upload_id).isdigit():
            raise DownloadRejected("The upload ID must be an opaque numeric ID returned by the resource tools.")
        _, destination = safe_destination(destination_root, filename)
        max_bytes = int(max_bytes)
        if max_bytes < 1:
            raise DownloadRejected("The download size limit must be positive.")
        from .constants import MAX_FILE_LIMIT

        if max_bytes > MAX_FILE_LIMIT:
            raise DownloadRejected("The requested per-file limit exceeds the plugin maximum of 250 MiB.")
        digest = sha256()
        total = 0
        descriptor, temporary_name = tempfile.mkstemp(prefix=".zju-download-", suffix=".part", dir=destination.parent)
        try:
            with self.stream_get(f"https://courses.zju.edu.cn/api/uploads/{upload_id}/blob") as response:
                if response.status_code in {401, 403}:
                    raise AuthenticationRequired()
                if response.status_code != 200:
                    raise ZJUError("download_failed", f"The official resource returned HTTP {response.status_code}.", retryable=response.status_code >= 500)
                declared = response.headers.get("content-length")
                if declared:
                    try:
                        if int(declared) > max_bytes:
                            raise DownloadRejected("The resource exceeds the selected per-file size limit.")
                    except ValueError:
                        pass
                with os.fdopen(descriptor, "wb") as handle:
                    descriptor = -1
                    for chunk in response.iter_bytes(64 * 1024):
                        total += len(chunk)
                        if total > max_bytes:
                            raise DownloadRejected("The streamed resource exceeded the selected size limit.")
                        handle.write(chunk)
                        digest.update(chunk)
                    handle.flush()
                    os.fsync(handle.fileno())
                mime_type = response.headers.get("content-type", "application/octet-stream").split(";", 1)[0]
            os.replace(temporary_name, destination)
        except Exception:
            if descriptor >= 0:
                os.close(descriptor)
            Path(temporary_name).unlink(missing_ok=True)
            raise
        return {
            "upload_id": str(upload_id),
            "path": str(destination),
            "size": total,
            "mime_type": mime_type,
            "sha256": digest.hexdigest(),
        }


def page_info(payload: Any, *, requested_page: int, page_size: int) -> dict[str, Any]:
    if isinstance(payload, dict):
        total = payload.get("total") or payload.get("count") or payload.get("total_count")
        return {"number": requested_page, "size": page_size, "total": total}
    return {"number": requested_page, "size": page_size, "total": None}


def items_from(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("activities", "items", "list", "results", "data", "courses", "todos", "exams", "semesters"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = items_from(value)
            if nested:
                return nested
    return []


def matches_kind(item: dict[str, Any], words: tuple[str, ...]) -> bool:
    selected = " ".join(str(item.get(key, "")) for key in ("type", "activity_type", "title", "name", "category")).lower()
    return any(word.lower() in selected for word in words)
