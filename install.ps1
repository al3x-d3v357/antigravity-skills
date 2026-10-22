# Script de Instalacao Automatica de Skills & MCPs para Google Antigravity IDE + OpenCode
# Autor: Alex Sandro (@al3x-d3v357)

param (
    [switch]$ConfigureMcp,
    [switch]$SkipMcp
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Instalador de Skills & MCPs - Google Antigravity IDE   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Instalar Skills (Antigravity + OpenCode + compatibilidade)
$destDir = "$env:USERPROFILE\.gemini\config\skills"
$opencodeDir = "$env:USERPROFILE\.config\opencode\skills"
$claudeDir = "$env:USERPROFILE\.claude\skills"
$agentsDir = "$env:USERPROFILE\.agents\skills"
foreach ($d in @($destDir, $opencodeDir, $claudeDir, $agentsDir)) {
    if (!(Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
        Write-Host "[+] Criado diretorio de destino: $d" -ForegroundColor Green
    }
}

$sourceDir = Join-Path $PSScriptRoot "skills"

if (!(Test-Path $sourceDir)) {
    Write-Host "[-] Erro: Pasta 'skills' nao encontrada!" -ForegroundColor Red
    Exit 1
}

$skills = Get-ChildItem -Path $sourceDir -Recurse -Filter "SKILL.md" | ForEach-Object { $_.Directory }

Write-Host "`n[1/2] Copiando $($skills.Count) Skills para Antigravity + OpenCode..." -ForegroundColor Yellow
foreach ($skill in $skills) {
    Copy-Item -Path $skill.FullName -Destination $destDir -Recurse -Force
    Copy-Item -Path $skill.FullName -Destination $opencodeDir -Recurse -Force
    Copy-Item -Path $skill.FullName -Destination $claudeDir -Recurse -Force
    Copy-Item -Path $skill.FullName -Destination $agentsDir -Recurse -Force
    Write-Host "  [+] $($skill.Name)" -ForegroundColor Green
}
Write-Host "[INFO] Skills instaladas em:" -ForegroundColor Cyan
Write-Host "  - Antigravity: $destDir" -ForegroundColor Cyan
Write-Host "  - OpenCode global: $opencodeDir" -ForegroundColor Cyan
Write-Host "  - Compat: $claudeDir, $agentsDir" -ForegroundColor Cyan

# 2. Configurar MCPs
$mcpSetupScript = Join-Path $PSScriptRoot "mcp-servers\setup_all_mcps.ps1"
if (Test-Path $mcpSetupScript) {
    if ($ConfigureMcp) {
        powershell.exe -ExecutionPolicy Bypass -File $mcpSetupScript
    } elseif ($SkipMcp) {
        Write-Host "`n[2/2] Configuracao de MCP ignorada conforme parametro." -ForegroundColor Cyan
    } else {
        Write-Host "`n[2/2] Deseja configurar os MCP Servers (Mixamo, Blender, Unity, Affinity, GameMaker, Stitch)? [S/N] (Padrao: S): " -NoNewline -ForegroundColor Yellow
        $ans = Read-Host
        if ($ans -eq "" -or $ans -match "^[SsYy]") {
            powershell.exe -ExecutionPolicy Bypass -File $mcpSetupScript
        } else {
            Write-Host "[INFO] Configuracao de MCP ignorada. Para configurar mais tarde, execute: .\mcp-servers\setup_all_mcps.ps1" -ForegroundColor Cyan
        }
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " [SUCESSO] Instalacao finalizada!                         " -ForegroundColor Green
Write-Host " Reinicie o Antigravity IDE para carregar as alteracoes.  " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
