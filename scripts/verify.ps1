param(
  [string]$CodexSkillsDir = "",
  [switch]$InstalledOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
  $CodexSkillsDir = Join-Path $homeDir ".codex\skills"
}

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$customSkills = @("ai-product-delivery-pipeline", "douyin-skill-installer", "github-skill-pack-publisher")
$validator = Join-Path $homeDir ".codex\skills\.system\skill-creator\scripts\quick_validate.py"

function Test-SkillFolder {
  param([string]$Path, [string]$Name)

  if (-not (Test-Path -LiteralPath $Path)) {
    Write-Host "MISSING $Name -> $Path"
    return
  }
  $skillMd = Join-Path $Path "SKILL.md"
  if (-not (Test-Path -LiteralPath $skillMd)) {
    Write-Host "MISSING SKILL.md for $Name"
    return
  }
  Write-Host "OK $Name -> $Path"
  if (Test-Path -LiteralPath $validator) {
    python $validator $Path
  }
}

foreach ($name in $customSkills) {
  if ($InstalledOnly) {
    $path = Join-Path $CodexSkillsDir $name
  } else {
    $path = Join-Path (Join-Path $repoRoot "skills") $name
  }
  Test-SkillFolder -Path $path -Name $name
}

if ($InstalledOnly) {
  $companions = @(
    "vercel-react-best-practices",
    "web-design-guidelines",
    "microsoft-foundry",
    "azure-ai",
    "azure-aigateway",
    "azure-prepare",
    "azure-validate",
    "azure-deploy"
  )
  foreach ($name in $companions) {
    Test-SkillFolder -Path (Join-Path $CodexSkillsDir $name) -Name $name
  }
}
