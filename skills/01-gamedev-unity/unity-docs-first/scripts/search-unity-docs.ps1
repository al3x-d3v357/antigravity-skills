param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    [string]$DocType = "All" # "ScriptReference", "Manual", or "All"
)

$baseDocPath = "C:\Program Files\Unity\Hub\Editor\6000.6.2f1\Editor\Data\Documentation\en"
if (-not (Test-Path $baseDocPath)) {
    Write-Error "Local Unity documentation not found at: $baseDocPath"
    exit 1
}

Write-Host "Searching local Unity 6 documentation for: '$Query'..." -ForegroundColor Cyan

# 1. Exact match in ScriptReference
$scriptRefPath = Join-Path $baseDocPath "ScriptReference"
$exactFile = Join-Path $scriptRefPath "$Query.html"
if (Test-Path $exactFile) {
    Write-Host "[EXACT MATCH FOUND]: $exactFile" -ForegroundColor Green
    # Extract title and description
    $content = Get-Content $exactFile -Raw
    if ($content -match '<title>(.*?)</title>') {
        Write-Host "Title: $($matches[1])" -ForegroundColor Yellow
    }
    if ($content -match '(?s)<div class="section"><div class="mb20 clear".*?<p>(.*?)</p>') {
        $cleanDesc = $matches[1] -replace '<[^>]+>', ''
        Write-Host "Summary: $cleanDesc"
    }
}

# 2. Search related files
$files = @()
if ($DocType -eq "All" -or $DocType -eq "ScriptReference") {
    $files += Get-ChildItem -Path $scriptRefPath -Filter "*$Query*.html" -File -ErrorAction SilentlyContinue | Select-Object -First 10
}
if ($DocType -eq "All" -or $DocType -eq "Manual") {
    $manualPath = Join-Path $baseDocPath "Manual"
    $files += Get-ChildItem -Path $manualPath -Filter "*$Query*.html" -File -ErrorAction SilentlyContinue | Select-Object -First 5
}

if ($files.Count -gt 0) {
    Write-Host "`nRelated documentation pages:" -ForegroundColor Magenta
    foreach ($file in $files) {
        Write-Host " - file:///$($file.FullName.Replace('\', '/'))"
    }
} else {
    Write-Host "No direct file name matches. You can inspect ScriptReference/$Query*.html"
}
