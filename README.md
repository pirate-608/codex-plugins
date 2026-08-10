# pirate-608 Codex Plugins

English | [简体中文](README.zh-CN.md)

A public Codex plugin marketplace for Unity, CAD, Adobe, LaTeX, Ren'Py, and Calibre workflows.

## Add the marketplace

~~~sh
codex plugin marketplace add git@github.com:pirate-608/codex-plugins.git
~~~

If SSH is unavailable, use HTTPS:

~~~sh
codex plugin marketplace add https://github.com/pirate-608/codex-plugins.git
~~~

Install a plugin with its stable ID and marketplace name:

~~~sh
codex plugin add unity-mcp@pirate-608-codex-plugins
~~~

## Configure with AI

Copy this prompt into Codex or another coding agent:

~~~text
Configure this Codex plugin marketplace for me:

- SSH repository: git@github.com:pirate-608/codex-plugins.git
- HTTPS fallback: https://github.com/pirate-608/codex-plugins.git
- Expected marketplace name: pirate-608-codex-plugins

Work autonomously and complete the setup:
1. Inspect the installed Codex CLI and its plugin marketplace help before running commands.
2. List the configured marketplaces. If this exact marketplace already exists, refresh it with
   the supported marketplace upgrade command instead of creating a duplicate.
3. If it is missing, add it with the SSH URL. If SSH connectivity or authentication fails, retry
   with the HTTPS URL.
4. Preserve all unrelated marketplaces and settings. Do not install individual plugins unless I
   explicitly ask.
5. Verify that the marketplace is available and that its name is pirate-608-codex-plugins, then
   use the plugin list command to report its available plugin IDs.
6. Report the commands run and the final result. Ask me only if authentication, approval, or a
   missing prerequisite prevents completion. Never print credentials or tokens.
~~~

## Plugins

| Plugin ID | Display name | Focus |
| --- | --- | --- |
| unity-mcp | Unity MCP | Unity project setup, 2D/3D, gameplay, UI, VFX, debugging, optimization, and builds |
| renpy-visual-novel-dev | Ren'Py Visual Novel Development | Ren'Py project development and maintenance |
| latex-workflows | LaTeX Workflows | LaTeX compilation, troubleshooting, and validation |
| solidworks-automation | SolidWorks Automation | SolidWorks COM and MCP automation |
| autocad-mcp-codex | AutoCAD MCP | AutoCAD drafting and inspection through MCP |
| adobe-photoshop | Adobe Photoshop | Photoshop document and layer workflows |
| adobe-premiere | Adobe Premiere Pro | Premiere Pro editing workflows |
| adobe-after-effects | Adobe After Effects | After Effects composition workflows |
| calibre-library-tools | Calibre Library Tools | Calibre library analysis and curation |

## Requirements

Each plugin declares its own runtime integration. Depending on the plugin, the host machine may
need the relevant desktop application plus tools such as Python, uv/uvx, Node.js/npx, or
PowerShell on PATH. Commercial desktop applications and user credentials are not included.

## Repository layout

- .agents/plugins/marketplace.json is the Git marketplace catalog.
- plugins/<plugin-id>/.codex-plugin/plugin.json is each plugin manifest.
- Plugin-specific skills, MCP launchers, scripts, icons, and upstream notices live beside the
  manifest.

## Licensing

This repository aggregates independently licensed plugins and vendored components. Refer to each
plugin manifest and its bundled LICENSE, NOTICE, UPSTREAM.json, or vendor directory for the
applicable terms and attribution. See [NOTICE.md](NOTICE.md) for a concise inventory.
