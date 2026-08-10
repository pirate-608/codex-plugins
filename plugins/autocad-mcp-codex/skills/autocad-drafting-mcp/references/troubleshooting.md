# Troubleshooting

## Status uses `ezdxf`

`auto` found no compatible AutoCAD window. This is expected when AutoCAD is closed. Start AutoCAD with a drawing open, confirm the bundle loaded, then call `system(operation="init")` and `system(operation="status")`.

## AutoCAD detected but dispatcher is not loaded

1. Check that `%APPDATA%\Autodesk\ApplicationPlugins\CodexAutoCADMCP.bundle` exists.
2. Restart AutoCAD.
3. Accept the publisher or trust prompt if shown.
4. Keep `SECURELOAD` enabled and trust only the bundle location.

For a one-session test, load the bundle's `Contents/mcp_dispatch.lsp` with `APPLOAD`.

## Timeout

- Cancel any active AutoCAD command with Escape.
- Confirm both sides use `C:/temp/codex-autocad-mcp`.
- Ensure AutoCAD has an open drawing.
- Retry `system(operation="init")`.
- Do not issue parallel MCP calls.

## Unsupported operation

Read `system(status)` capabilities. Use File IPC for DWG, PDF plotting, undo/redo, offset, fillet, and chamfer. Use ezdxf for offline DXF workflows.

## Screenshots fail

Set `AUTOCAD_MCP_ONLY_TEXT=true` only when text-only operation is acceptable. Otherwise keep AutoCAD available for Win32 capture or use the ezdxf renderer.

## Save failure

Use an absolute path in a writable directory. Do not overwrite the input drawing. Use `.dxf` for headless work; `.dwg` and PDF require File IPC.