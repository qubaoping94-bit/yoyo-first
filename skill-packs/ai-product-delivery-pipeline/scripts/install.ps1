param(
  [string]$CodexSkillsDir = "",
  [switch]$WithCompanions
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
  $CodexSkillsDir = Join-Path $homeDir ".codex\skills"
}

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$sourceSkills = Join-Path $repoRoot "skills"
New-Item -ItemType Directory -Path $CodexSkillsDir -Force | Out-Null

Get-ChildItem -LiteralPath $sourceSkills -Directory | ForEach-Object {
  $dest = Join-Path $CodexSkillsDir $_.Name
  New-Item -ItemType Directory -Path $dest -Force | Out-Null
  Get-ChildItem -LiteralPath $_.FullName -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
  }
  Write-Host "Installed $($_.Name) -> $dest"
}

if ($WithCompanions) {
  & (Join-Path $PSScriptRoot "install-companion-skills.ps1") -CodexSkillsDir $CodexSkillsDir
}

Write-Host "Done. Restart Codex or open a new session."

