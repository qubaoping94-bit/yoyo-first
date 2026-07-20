param([string]$SkillsRoot = "$env:USERPROFILE\.codex\skills")
$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $packageRoot "skills\mike-website-production-pipeline"
if (!(Test-Path -LiteralPath (Join-Path $source "SKILL.md"))) { throw "Missing skills\mike-website-production-pipeline\SKILL.md" }
if ($env:CODEX_HOME) { $destRoot = Join-Path $env:CODEX_HOME "skills" } else { $destRoot = $SkillsRoot }
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
$dest = Join-Path $destRoot "mike-website-production-pipeline"
$fullRoot = [IO.Path]::GetFullPath($destRoot)
$fullDest = [IO.Path]::GetFullPath($dest)
if (!$fullDest.StartsWith($fullRoot,[StringComparison]::OrdinalIgnoreCase)) { throw "Unexpected install target: $fullDest" }
if (Test-Path -LiteralPath $dest) { $backup="$dest.backup-$(Get-Date -Format yyyyMMddHHmmss)"; Rename-Item -LiteralPath $dest -NewName (Split-Path -Leaf $backup); Write-Host "Backed up old version: $backup" }
Copy-Item -LiteralPath $source -Destination $dest -Recurse -Force
Write-Host "Mike Website Production Pipeline installed to: $dest" -ForegroundColor Green
Write-Host 'Restart Codex, then invoke $mike-website-production-pipeline.'
