param(
    [string]$HttpUrl = 'http://127.0.0.1:8080'
)

$ErrorActionPreference = 'Stop'

$uvxCommand = Get-Command uvx -ErrorAction SilentlyContinue
if ($null -eq $uvxCommand) {
    throw 'uvx was not found on PATH. Install uv from https://docs.astral.sh/uv/ and restart Codex.'
}
$uvxPath = $uvxCommand.Source

& $uvxPath `
    --from 'mcpforunityserver==10.1.2' `
    mcp-for-unity `
    --transport http `
    --http-url $HttpUrl `
    --project-scoped-tools

exit $LASTEXITCODE
