param(
    [string]$McpUrl = 'http://127.0.0.1:8080/mcp'
)

$ErrorActionPreference = 'Stop'
$headers = @{ Accept = 'application/json, text/event-stream' }
$initializeBody = @{
    jsonrpc = '2.0'
    id = 1
    method = 'initialize'
    params = @{
        protocolVersion = '2025-06-18'
        capabilities = @{}
        clientInfo = @{ name = 'unity-mcp-plugin-diagnostic'; version = '1.0.0' }
    }
} | ConvertTo-Json -Depth 6 -Compress

$initializeResponse = Invoke-WebRequest -Uri $McpUrl -Method Post -Headers $headers -ContentType 'application/json' -Body $initializeBody
$sessionId = [string]($initializeResponse.Headers['Mcp-Session-Id'] | Select-Object -First 1)
$headers['Mcp-Session-Id'] = $sessionId

Invoke-WebRequest -Uri $McpUrl -Method Post -Headers $headers -ContentType 'application/json' -Body '{"jsonrpc":"2.0","method":"notifications/initialized"}' | Out-Null
$instancesResponse = Invoke-WebRequest -Uri $McpUrl -Method Post -Headers $headers -ContentType 'application/json' -Body '{"jsonrpc":"2.0","id":2,"method":"resources/read","params":{"uri":"mcpforunity://instances"}}'

[pscustomobject]@{
    StatusCode = $instancesResponse.StatusCode
    SessionId = $sessionId
    InstancesResponse = $instancesResponse.Content
}
