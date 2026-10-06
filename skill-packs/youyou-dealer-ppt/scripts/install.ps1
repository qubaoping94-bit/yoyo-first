param([string]$SkillsRoot = "$env:USERPROFILE\.codex\skills")
$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $packageRoot 'skills\youyou-dealer-ppt'
if (!(Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) { throw 'Missing SKILL.md' }
if ($env:CODEX_HOME) { $destRoot = Join-Path $env:CODEX_HOME 'skills' } else { $destRoot = $SkillsRoot }
$fullRoot = [IO.Path]::GetFullPath($destRoot).TrimEnd('\')
$dest = Join-Path $fullRoot 'youyou-dealer-ppt'
$fullDest = [IO.Path]::GetFullPath($dest)
if (!$fullDest.StartsWith(($fullRoot + '\'), [StringComparison]::OrdinalIgnoreCase)) { throw "Unexpected destination: $fullDest" }
New-Item -ItemType Directory -Force -Path $fullRoot | Out-Null
if (Test-Path -LiteralPath $dest) {
  $backupRoot = Join-Path (Split-Path -Parent $fullRoot) 'skill-backups'
  $backup = Join-Path $backupRoot "youyou-dealer-ppt-$(Get-Date -Format yyyyMMddHHmmss)"
  $resolvedBackup = [IO.Path]::GetFullPath($backup)
  if (!$resolvedBackup.StartsWith(([IO.Path]::GetFullPath($backupRoot).TrimEnd('\') + '\'), [StringComparison]::OrdinalIgnoreCase)) { throw "Unexpected backup: $resolvedBackup" }
  New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
  Move-Item -LiteralPath $fullDest -Destination $resolvedBackup
  Write-Host "Previous skill backed up: $backup"
}
Copy-Item -LiteralPath $source -Destination $dest -Recurse -Force
Write-Host "Installed: $dest"
