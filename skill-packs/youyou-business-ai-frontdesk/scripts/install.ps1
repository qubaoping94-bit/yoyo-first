param([string]$CodexSkillsDir = "")

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
    if ([string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
        throw "USERPROFILE is unavailable; pass -CodexSkillsDir explicitly."
    }
    $CodexSkillsDir = Join-Path $env:USERPROFILE ".codex\skills"
}

$packRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$manifest = Get-Content -LiteralPath (Join-Path $packRoot "manifest\skill-pack.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$skillName = [string]$manifest.skill.name
$source = Join-Path $packRoot ([string]$manifest.skill.path).Replace("/", "\")

if (-not (Test-Path -LiteralPath (Join-Path $source "SKILL.md") -PathType Leaf)) {
    throw "Missing packaged SKILL.md: $source"
}

New-Item -ItemType Directory -Path $CodexSkillsDir -Force | Out-Null
$skillsRoot = [System.IO.Path]::GetFullPath($CodexSkillsDir).TrimEnd("\")
$destination = [System.IO.Path]::GetFullPath((Join-Path $skillsRoot $skillName))
$requiredPrefix = $skillsRoot + "\"
if (-not $destination.StartsWith($requiredPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe destination outside Codex skills root: $destination"
}

$backup = $null
if (Test-Path -LiteralPath $destination) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = "$destination.backup-$stamp"
    if (Test-Path -LiteralPath $backup) {
        throw "Backup path already exists: $backup"
    }
    Copy-Item -LiteralPath $destination -Destination $backup -Recurse -ErrorAction Stop
    Remove-Item -LiteralPath $destination -Recurse -Force -ErrorAction Stop
}

New-Item -ItemType Directory -Path $destination -Force | Out-Null
Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -ErrorAction Stop
}

Write-Host "Installed $skillName -> $destination"
if ($backup) { Write-Host "Previous version backed up -> $backup" }
Write-Host "Restart Codex or open a new task so the skill list refreshes."
