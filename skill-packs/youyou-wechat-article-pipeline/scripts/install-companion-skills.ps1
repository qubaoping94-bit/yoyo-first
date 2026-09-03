$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$manifest = Get-Content -Raw -Encoding UTF8 (Join-Path $packageRoot "manifest\companion-skills.json") | ConvertFrom-Json
Write-Host "Companion skills are not installed automatically because their trusted source is environment-specific."
foreach ($item in $manifest.companions) {
  Write-Host ("- {0}: {1}" -f $item.name, $item.requiredFor)
}

