param([string]$CodexSkillsDir = "")
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) { $CodexSkillsDir = Join-Path $homeDir ".codex\skills" }
$companions = @(
  "youyou-special-demo-system",
  "ian-xiaohei-scenes",
  "html-production-defaults"
)
$missing = @()
foreach ($name in $companions) {
  $path = Join-Path $CodexSkillsDir $name
  if (Test-Path -LiteralPath (Join-Path $path "SKILL.md")) {
    Write-Host "OK companion skill: $name"
  } else {
    Write-Warning "Missing companion skill: $name"
    $missing += $name
  }
}
if ($missing.Count -gt 0) {
  Write-Host "Install missing companion skills from the user's trusted local/upstream sources before running the full Youyou demo workflow."
}

