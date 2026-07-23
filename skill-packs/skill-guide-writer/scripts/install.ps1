param([string]$CodexSkillsDir = "")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$userHome = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
    $CodexSkillsDir = Join-Path $userHome ".codex\skills"
}

$packRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$skillName = "skill-guide-writer"
$source = Join-Path (Join-Path $packRoot "skills") $skillName
$destination = Join-Path $CodexSkillsDir $skillName

if (-not (Test-Path -LiteralPath (Join-Path $source "SKILL.md"))) {
    throw "Missing packaged SKILL.md: $source"
}

New-Item -ItemType Directory -Path $destination -Force | Out-Null
Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force
}

Write-Host "Installed $skillName -> $destination"
Write-Host "Restart Codex or open a new task so the skill list refreshes."
