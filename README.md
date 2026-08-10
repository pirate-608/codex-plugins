# pirate-608 Codex Plugins

A public Codex plugin marketplace for Unity, CAD, Adobe, LaTeX, Ren'Py, and Calibre workflows.

## Add the marketplace

~~~sh
codex plugin marketplace add git@github.com:pirate-608/codex-plugins.git
~~~

Install a plugin with its stable ID and marketplace name:

~~~sh
codex plugin add unity-mcp@pirate-608-codex-plugins
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
