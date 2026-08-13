from __future__ import annotations


class ZJUError(RuntimeError):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool = False,
        auth_required: bool = False,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.retryable = retryable
        self.auth_required = auth_required


class AuthenticationRequired(ZJUError):
    def __init__(self, message: str = "Run the local ZJU authentication script, then retry.") -> None:
        super().__init__("auth_required", message, auth_required=True)


class UpstreamChanged(ZJUError):
    def __init__(self, message: str = "The unofficial campus API contract appears to have changed.") -> None:
        super().__init__("upstream_changed", message)


class DownloadRejected(ZJUError):
    def __init__(self, message: str) -> None:
        super().__init__("download_rejected", message)
