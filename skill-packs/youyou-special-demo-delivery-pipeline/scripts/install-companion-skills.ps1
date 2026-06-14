param(
  [string]$SkillsRoot = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"
$companions = @(
  "youyou-special-demo-system",
  "ian-xiaohei-scenes",
  "html-production-defaults",
  "github-skill-pack-publisher"
)

foreach ($name in $companions) {
  $path = Join-Path $SkillsRoot $name
  if (Test-Path $path) {
    Write-Host "[OK] $name"
  } else {
    Write-Host "[MISSING] $name - install or copy this companion skill if this workflow needs it."
  }
}

