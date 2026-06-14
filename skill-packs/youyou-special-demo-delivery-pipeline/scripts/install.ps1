param(
  [string]$SkillsRoot = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $packageRoot "skills\youyou-special-demo-delivery-pipeline"
$target = Join-Path $SkillsRoot "youyou-special-demo-delivery-pipeline"

if (!(Test-Path $source)) {
  throw "Packaged skill folder not found: $source"
}

New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null
if (Test-Path $target) {
  $backup = "$target.backup-$(Get-Date -Format yyyyMMddHHmmss)"
  Copy-Item -Recurse -Force $target $backup
  Write-Host "Existing skill backed up to $backup"
}

Copy-Item -Recurse -Force $source $target
Write-Host "Installed skill to $target"
Write-Host "Open a new Codex session to refresh available skills."

