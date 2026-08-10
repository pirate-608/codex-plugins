# Adobe Photoshop Codex Plugin

This plugin integrates the Windows-only `loonghao/photoshop-python-api-mcp-server` with Codex and adds a safety-focused Photoshop workflow skill.

## Install the MCP Runtime

Install `uv`, then run from this plugin directory:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-photoshop-mcp.ps1
```

Check the installation and local Photoshop registration without starting the server:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-photoshop-mcp.ps1 -CheckOnly
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-photoshop-mcp.ps1 -Check
```

The launcher intentionally leaves `PS_VERSION` unset so the Python adapter can discover the newest registered Photoshop COM version. Define it only when deliberately overriding discovery.

## Use

Start a new Codex task after installing or updating the plugin so its MCP server and skill are loaded. Ask Codex to inspect the Photoshop session first, then make document changes with explicit output and preservation requirements.

The upstream MCP surface is limited to session/document/selection inspection, document create/open/save-copy, text-layer creation, and raster filled-layer creation. Read the included skill before expanding the workflow with UI automation.
