# Adobe After Effects Codex plugin

This local Codex plugin connects to [JUNKDOGE-JOE/after-effects-mcp](https://github.com/JUNKDOGE-JOE/after-effects-mcp) through its installed stable launcher and adds the `after-effects-workflows` skill.

It does not vendor or rebuild the upstream runtime. Install the matching official ae-mcp panel/runtime first, open `Window > Extensions > ae-mcp` in After Effects, and start a new Codex task after installing this plugin.

Run the local launcher check from this directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-ae-mcp.ps1 -Check
```

The default Windows launcher path is `%USERPROFILE%\.ae-mcp\bin\ae-mcp.exe`. Set `AE_MCP_LAUNCHER` only when the official launcher is installed elsewhere.

Compatibility snapshot: ae-mcp v0.9.2, Windows 11 24H2+ x64, After Effects 25.x hardware-validated. Consult upstream release notes for newer information.
