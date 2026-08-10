#!/usr/bin/env python3
"""Start the bundled Ren'Py MCP server for the active Codex workspace."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _is_project(path: Path) -> bool:
    return path.is_dir() and (path / "game").is_dir()


def _walk_to_project(path: Path) -> Path | None:
    path = path.expanduser().resolve()
    for candidate in (path, *path.parents):
        if _is_project(candidate):
            return candidate
    return None


def _project_from_codex_session() -> Path | None:
    thread_id = os.environ.get("CODEX_THREAD_ID", "").strip()
    sessions_root = Path.home() / ".codex" / "sessions"
    if not thread_id or not sessions_root.is_dir():
        return None
    try:
        matches = sorted(
            sessions_root.rglob(f"*{thread_id}*.jsonl"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return None
    for session_path in matches:
        try:
            with session_path.open("r", encoding="utf-8") as session:
                item = json.loads(session.readline())
            cwd = item.get("payload", {}).get("cwd")
            if item.get("type") == "session_meta" and cwd:
                project = _walk_to_project(Path(cwd))
                if project is not None:
                    return project
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    return None


def _discover_project() -> Path | None:
    for env_name in ("RENPY_PROJECT", "CODEX_WORKSPACE_ROOT", "INIT_CWD"):
        raw = os.environ.get(env_name, "").strip()
        if raw:
            project = _walk_to_project(Path(raw))
            if project is not None:
                return project
    return _walk_to_project(Path.cwd()) or _project_from_codex_session()


def _sdk_launcher_exists(path: Path) -> bool:
    launcher = "renpy.exe" if os.name == "nt" else "renpy.sh"
    return path.is_dir() and (path / launcher).is_file()


def _sdk_dirs(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        (path for path in root.glob("sdk-*") if _sdk_launcher_exists(path)),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def _discover_sdk(project: Path) -> Path | None:
    explicit = os.environ.get("RENPY_SDK", "").strip()
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
        if _sdk_launcher_exists(candidate):
            return candidate
    cache_roots = (
        project / ".tools" / "renpy-mcp" / "sdk-cache",
        Path.home() / ".cache" / "renpy-mcp",
        Path.home() / "AppData" / "Local" / "renpy-mcp",
    )
    for root in cache_roots:
        candidates = _sdk_dirs(root)
        if candidates:
            return candidates[0].resolve()
    for root in (Path.home() / "renpy", Path.home() / "Documents" / "RenPy"):
        if root.is_dir():
            candidates = [path for path in root.glob("renpy-*-sdk") if _sdk_launcher_exists(path)]
            if candidates:
                return sorted(candidates, key=lambda path: path.stat().st_mtime)[-1].resolve()
    return None


def main() -> int:
    project = _discover_project()
    if project is None:
        print("renpy-mcp: no active Ren'Py project; set RENPY_PROJECT.", file=sys.stderr)
        return 2
    sdk = _discover_sdk(project)
    if sdk is None:
        print("renpy-mcp: no Ren'Py SDK; set RENPY_SDK or install the project SDK cache.", file=sys.stderr)
        return 2
    plugin_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(plugin_root / "vendor" / "renpy-mcp"))
    from renpy_mcp.__main__ import main as renpy_mcp_main
    sys.argv = [
        "renpy-mcp", "--project", str(project), "--sdk", str(sdk),
        "--tiers", os.environ.get("RENPY_MCP_TIERS", "1,2,3"),
    ]
    return renpy_mcp_main()


if __name__ == "__main__":
    raise SystemExit(main())
