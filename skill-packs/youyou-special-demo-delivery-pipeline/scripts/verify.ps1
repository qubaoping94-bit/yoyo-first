param(
  [switch]$CheckInstalled,
  [string]$SkillsRoot = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$skillDir = Join-Path $packageRoot "skills\youyou-special-demo-delivery-pipeline"
$required = @(
  "README.md",
  "docs\FEATURES.md",
  "docs\INSTALLATION.md",
  "docs\WORKFLOWS.md",
  "docs\SECURITY.md",
  "docs\GITHUB_UPLOAD.md",
  "examples\prompts.md",
  "manifest\skill-pack.json",
  "manifest\companion-skills.json",
  "skills\youyou-special-demo-delivery-pipeline\SKILL.md",
  "skills\youyou-special-demo-delivery-pipeline\agents\openai.yaml",
  "skills\youyou-special-demo-delivery-pipeline\references\release-checklist.md"
)

$issues = @()
foreach ($rel in $required) {
  if (!(Test-Path (Join-Path $packageRoot $rel))) {
    $issues += "Missing $rel"
  }
}

$skillMd = Join-Path $skillDir "SKILL.md"
if (Test-Path $skillMd) {
  $text = Get-Content -Raw -Encoding UTF8 $skillMd
  if ($text -notmatch "(?s)^---\s*.*name:\s*youyou-special-demo-delivery-pipeline.*description:\s*.+?---") {
    $issues += "SKILL.md frontmatter is incomplete"
  }
}

$manifestPath = Join-Path $packageRoot "manifest\skill-pack.json"
if (Test-Path $manifestPath) {
  $manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json
  if ($manifest.name -ne "youyou-special-demo-delivery-pipeline") {
    $issues += "Manifest name mismatch"
  }
}

if ($CheckInstalled) {
  $installed = Join-Path $SkillsRoot "youyou-special-demo-delivery-pipeline\SKILL.md"
  if (!(Test-Path $installed)) {
    $issues += "Installed skill not found at $installed"
  }
}

if ($issues.Count -gt 0) {
  $issues | ForEach-Object { Write-Host "[FAIL] $_" }
  throw "Verification failed with $($issues.Count) issue(s)."
}

Write-Host "Skill pack verification passed."

