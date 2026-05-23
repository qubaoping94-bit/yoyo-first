param(
  [string]$CodexSkillsDir = "$env:USERPROFILE\.codex\skills",
  [switch]$WithCompanions
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$sourceSkills = Join-Path $repoRoot "skills"

if (-not (Test-Path -LiteralPath $sourceSkills)) {
  throw "Missing skills directory: $sourceSkills"
}

New-Item -ItemType Directory -Path $CodexSkillsDir -Force | Out-Null

Get-ChildItem -LiteralPath $sourceSkills -Directory | ForEach-Object {
  $dest = Join-Path $CodexSkillsDir $_.Name
  if (Test-Path -LiteralPath $dest) {
    Write-Host "Updating $($_.Name) -> $dest"
  } else {
    Write-Host "Installing $($_.Name) -> $dest"
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
  }
  Get-ChildItem -LiteralPath $_.FullName -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
  }
}

if ($WithCompanions) {
  & (Join-Path $PSScriptRoot "install-companion-skills.ps1") -CodexSkillsDir $CodexSkillsDir
}

Write-Host ""
Write-Host "Done. Restart Codex or open a new session so newly installed skills are discovered."
