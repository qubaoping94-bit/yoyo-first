param([string]$CodexSkillsDir = "")
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
  $CodexSkillsDir = Join-Path $homeDir ".codex\skills"
}

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$name = Split-Path $repoRoot -Leaf
$src = Join-Path (Join-Path $repoRoot "skills") $name
$dest = Join-Path $CodexSkillsDir $name

if (-not (Test-Path -LiteralPath (Join-Path $src "SKILL.md"))) {
  throw "Missing packaged skill: $src"
}

New-Item -ItemType Directory -Path $dest -Force | Out-Null
Get-ChildItem -LiteralPath $src -Force | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
}

Write-Host "Installed $name -> $dest"
Write-Host "Restart Codex or open a new session."
