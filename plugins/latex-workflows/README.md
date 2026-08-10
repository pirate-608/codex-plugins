# LaTeX Workflows

Personal Codex plugin for LaTeX build workflows.

## Purpose

This plugin teaches Codex to compile and validate LaTeX projects with a conservative tool order:

1. Use bundled or PATH-visible Tectonic first for simple projects.
2. Fall back to a detected local MiKTeX installation for fuller projects.
3. Validate local LaTeX readiness before compiling non-trivial projects.
4. Ask the user to verify the MiKTeX path only when no usable system installation is detected.

## Layout

- `.codex-plugin/plugin.json` contains the Codex plugin manifest.
- `skills/latex-workflows/SKILL.md` contains the workflow Codex should follow.
- `scripts/check_latex_readiness.py` detects Tectonic, MiKTeX, common LaTeX tools, likely root
  `.tex` files, and whether a project appears to need a full system toolchain.

## Python And PATH Notes

The readiness helper uses only the Python standard library, so no runtime packages are required.
Before running validation or helper commands, confirm the Python interpreter that Codex sees:

```powershell
where.exe python
python --version
```

If `python` resolves to an unexpected interpreter, restart Codex after fixing the PowerShell
startup environment or call the intended interpreter explicitly.

The plugin and skill validators import `PyYAML`. If validation fails with `No module named 'yaml'`,
install `PyYAML` into the intended user-level Python environment:

```powershell
python -m pip install --user PyYAML
```

Do not run `python -m pip install --upgrade pip` unless the user explicitly approves the
administrator-required pip upgrade path.

## Validation

From the plugin directory, where `python` is the intended interpreter:

```powershell
python <plugin-creator-path>\scripts\validate_plugin.py .
python <skill-creator-path>\scripts\quick_validate.py .\skills\latex-workflows
python .\scripts\check_latex_readiness.py .
```
