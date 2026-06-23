param(
  [string]$SkillsRoot = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $packageRoot "skills\youyou-ai-product-advisor"
if (!(Test-Path -LiteralPath (Join-Path $source "SKILL.md"))) {
  throw "Missing skills\youyou-ai-product-advisor\SKILL.md. Please unzip the full repository first."
}

if ($env:CODEX_HOME) {
  $destRoot = Join-Path $env:CODEX_HOME "skills"
} else {
  $destRoot = $SkillsRoot
}

New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
$dest = Join-Path $destRoot "youyou-ai-product-advisor"
$fullDestRoot = [System.IO.Path]::GetFullPath($destRoot)
$fullDest = [System.IO.Path]::GetFullPath($dest)
if (!$fullDest.StartsWith($fullDestRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Unexpected install target: $fullDest"
}

if (Test-Path -LiteralPath $dest) {
  $backup = "$dest.backup-$(Get-Date -Format yyyyMMddHHmmss)"
  Rename-Item -LiteralPath $dest -NewName (Split-Path -Leaf $backup)
  Write-Host "Backed up old version: $backup"
}

Copy-Item -LiteralPath $source -Destination $dest -Recurse -Force
Write-Host ""
Write-Host "Youyou AI Product Advisor Skill installed to: $dest" -ForegroundColor Green
Write-Host 'Restart Codex, then use: Use $youyou-ai-product-advisor to answer a Youyou customer question.'
