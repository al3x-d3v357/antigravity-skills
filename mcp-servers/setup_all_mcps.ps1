# Script de Configuracao e Instalacao de MCP Servers para Antigravity IDE + OpenCode
# Autor: Alex Sandro (@al3x-d3v357)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Instalador de MCP Servers - Antigravity + OpenCode     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$geminiConfigDir = "$env:USERPROFILE\.gemini\config"
$targetMcpConfig = Join-Path $geminiConfigDir "mcp_config.json"
$templateMcpConfig = Join-Path $PSScriptRoot "mcp_config.template.json"
$opencodeConfigDir = "$env:USERPROFILE\.config\opencode"
$opencodeConfigFile = Join-Path $opencodeConfigDir "opencode.jsonc"
$opencodeTemplate = Join-Path $PSScriptRoot "opencode.mcp.template.jsonc"

if (!(Test-Path $geminiConfigDir)) {
    New-Item -ItemType Directory -Path $geminiConfigDir -Force | Out-Null
    Write-Host "[+] Diretorio de configuracao criado: $geminiConfigDir" -ForegroundColor Green
}

# 1. Instalar dependencias Python comuns (MCP SDK, Playwright)
Write-Host "`n[1/3] Verificando dependencias Python para Mixamo & MCPs..." -ForegroundColor Yellow
try {
    python -m pip install --quiet --upgrade "mcp[cli]" playwright pydantic 2>$null
    Write-Host "[OK] Dependencias Python instaladas com sucesso." -ForegroundColor Green
} catch {
    Write-Host "[!] Aviso: Nao foi possivel instalar via pip automaticamente. Execute 'pip install mcp[cli] playwright pydantic' se necessario." -ForegroundColor DarkYellow
}

# 2. Instalar Chromium para o Playwright (Mixamo MCP)
Write-Host "`n[2/3] Verificando Chromium para Playwright (Mixamo MCP)..." -ForegroundColor Yellow
try {
    playwright install chromium 2>$null
    Write-Host "[OK] Navegador Chromium do Playwright pronto." -ForegroundColor Green
} catch {
    Write-Host "[!] Aviso: Execute 'playwright install chromium' manualmente se for usar o Mixamo MCP." -ForegroundColor DarkYellow
}

# 3. Aplicar mcp_config.json
Write-Host "`n[3/4] Configurando mcp_config.json no Antigravity..." -ForegroundColor Yellow
if (Test-Path $templateMcpConfig) {
    if (Test-Path $targetMcpConfig) {
        $backup = "$targetMcpConfig.bak"
        Copy-Item -Path $targetMcpConfig -Destination $backup -Force
        Write-Host "[INFO] Backup do config anterior salvo em: $backup" -ForegroundColor Cyan
    }
    Copy-Item -Path $templateMcpConfig -Destination $targetMcpConfig -Force
    Write-Host "[OK] mcp_config.json aplicado com sucesso em: $targetMcpConfig" -ForegroundColor Green
} else {
    Write-Host "[-] Arquivo de template nao encontrado em: $templateMcpConfig" -ForegroundColor Red
}

# 4. Aplicar MCPs no OpenCode (merge em ~/.config/opencode/opencode.jsonc)
Write-Host "`n[4/4] Configurando MCPs no OpenCode..." -ForegroundColor Yellow
if (Test-Path $opencodeTemplate) {
    if (!(Test-Path $opencodeConfigDir)) {
        New-Item -ItemType Directory -Path $opencodeConfigDir -Force | Out-Null
        Write-Host "[+] Diretorio OpenCode criado: $opencodeConfigDir" -ForegroundColor Green
    }
    try {
        $templateRaw = Get-Content $opencodeTemplate -Raw
        # Remove linhas de comentario JSONC e $schema para parse
        $templateClean = ($templateRaw -split "`n" | Where-Object { $_ -notmatch '^\s*//' } ) -join "`n"
        $templateObj = $templateClean | ConvertFrom-Json
        $templateServers = $templateObj.mcp.servers

        if (Test-Path $opencodeConfigFile) {
            $existingRaw = Get-Content $opencodeConfigFile -Raw
            $existingClean = ($existingRaw -split "`n" | Where-Object { $_ -notmatch '^\s*//' } ) -join "`n"
            try { $existingObj = $existingClean | ConvertFrom-Json }
            catch { $existingObj = [pscustomobject]@{} }
            $backup = "$opencodeConfigFile.bak"
            Copy-Item -Path $opencodeConfigFile -Destination $backup -Force
            Write-Host "[INFO] Backup do opencode.jsonc salvo em: $backup" -ForegroundColor Cyan
        } else {
            $existingObj = [pscustomobject]@{ '$schema' = 'https://opencode.ai/config.json' }
        }
        if (-not $existingObj.mcp) { $existingObj | Add-Member -NotePropertyName 'mcp' -NotePropertyValue ([pscustomobject]@{}) -Force }
        if (-not $existingObj.mcp.servers) { $existingObj.mcp | Add-Member -NotePropertyName 'servers' -NotePropertyValue ([pscustomobject]@{}) -Force }
        foreach ($prop in $templateServers.PSObject.Properties) {
            $existingObj.mcp.servers | Add-Member -NotePropertyName $prop.Name -NotePropertyValue $prop.Value -Force
        }
        # Garante skills locais quando o repo e o working dir
        if (-not $existingObj.skills) { $existingObj | Add-Member -NotePropertyName 'skills' -NotePropertyValue @() -Force }
        $mergedJson = $existingObj | ConvertTo-Json -Depth 10
        $header = "// OpenCode config gerenciado por antigravity-skills (merge automatico).`n// Template: mcp-servers/opencode.mcp.template.jsonc`n"
        Set-Content -Path $opencodeConfigFile -Value ($header + $mergedJson) -Encoding UTF8
        Write-Host "[OK] MCPs mesclados em: $opencodeConfigFile" -ForegroundColor Green
        Write-Host "[INFO] Verifique com: opencode mcp list" -ForegroundColor Cyan
    } catch {
        Write-Host "[!] Falha ao mesclar config do OpenCode: $($_.Exception.Message)" -ForegroundColor DarkYellow
        Write-Host "    Aplique manualmente o template: $opencodeTemplate" -ForegroundColor DarkYellow
    }
} else {
    Write-Host "[-] Template OpenCode nao encontrado em: $opencodeTemplate" -ForegroundColor Red
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " [SUCESSO] MCP Servers configurados com sucesso!           " -ForegroundColor Green
Write-Host " MCPs inclusos: Mixamo, Blender, Unity, Affinity,          " -ForegroundColor White
Write-Host "                GameMaker, Stitch                          " -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "`nNota: Para o Mixamo MCP funcionar, certifique-se de que o" -ForegroundColor Yellow
Write-Host "repositorio esta em D:\GitHub\mixamo-mcp e que a sessao" -ForegroundColor Yellow
Write-Host "esta salva em ~/.mixamo_session.json (execute python save_session.py)." -ForegroundColor Yellow
