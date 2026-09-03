param(
  [string]$SkillsRoot = "$env:USERPROFILE\.workbuddy\skills"
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $packageRoot "skills\youyou-wechat-article-pipeline"
$target = Join-Path $SkillsRoot "youyou-wechat-article-pipeline"

if (!(Test-Path -LiteralPath $source)) { throw "Packaged skill folder not found: $source" }
New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null
if (Test-Path -LiteralPath $target) {
  $backup = "$target.backup-$(Get-Date -Format yyyyMMddHHmmss)"
  Copy-Item -LiteralPath $target -Destination $backup -Recurse
  Write-Host "Existing skill backed up to $backup"
}
Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
Write-Host "Installed WorkBuddy skill to $target"
Write-Host "Restart WorkBuddy or open a new session to refresh the skill list."

