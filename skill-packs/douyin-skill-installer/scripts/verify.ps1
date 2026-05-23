param([string]$CodexSkillsDir = "", [switch]$InstalledOnly)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) { $CodexSkillsDir = Join-Path $homeDir ".codex\skills" }
$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$name = Split-Path $repoRoot -Leaf
$path = if ($InstalledOnly) { Join-Path $CodexSkillsDir $name } else { Join-Path (Join-Path $repoRoot "skills") $name }
if (-not (Test-Path -LiteralPath (Join-Path $path "SKILL.md"))) { throw "Missing SKILL.md: $path" }
Write-Host "OK $name -> $path"
$validator = Join-Path $homeDir ".codex\skills\.system\skill-creator\scripts\quick_validate.py"
if (Test-Path -LiteralPath $validator) { python $validator $path }

