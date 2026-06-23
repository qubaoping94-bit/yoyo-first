param(
  [switch]$CheckInstalled,
  [string]$SkillsRoot = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$skillDir = Join-Path $packageRoot "skills\youyou-ai-product-advisor"
$required = @(
  "README.md",
  "install.bat",
  "manifest\skill-pack.json",
  "scripts\install.ps1",
  "scripts\verify.ps1",
  "skills\youyou-ai-product-advisor\SKILL.md",
  "skills\youyou-ai-product-advisor\agents\openai.yaml",
  "skills\youyou-ai-product-advisor\references\claim-safety.md",
  "skills\youyou-ai-product-advisor\references\intent-router.md",
  "skills\youyou-ai-product-advisor\references\knowledge-data.json",
  "skills\youyou-ai-product-advisor\references\knowledge-library.md",
  "skills\youyou-ai-product-advisor\references\public-links.md",
  "skills\youyou-ai-product-advisor\references\standard-question-routes.json",
  "skills\youyou-ai-product-advisor\scripts\find-youyou-answer.mjs",
  "skills\youyou-ai-product-advisor\scripts\smoke-test.mjs"
)

$issues = @()
foreach ($rel in $required) {
  if (!(Test-Path -LiteralPath (Join-Path $packageRoot $rel))) {
    $issues += "Missing $rel"
  }
}

$skillMd = Join-Path $skillDir "SKILL.md"
if (Test-Path -LiteralPath $skillMd) {
  $text = Get-Content -Raw -Encoding UTF8 $skillMd
  if ($text -notmatch "(?s)^---\s*.*name:\s*youyou-ai-product-advisor.*description:\s*.+?---") {
    $issues += "SKILL.md frontmatter is incomplete"
  }
  if ($text -notmatch "find-youyou-answer\.mjs") {
    $issues += "SKILL.md must route users through find-youyou-answer.mjs"
  }
}

$openaiYaml = Join-Path $skillDir "agents\openai.yaml"
if (Test-Path -LiteralPath $openaiYaml) {
  $yaml = Get-Content -Raw -Encoding UTF8 $openaiYaml
  if ($yaml -notmatch "\$youyou-ai-product-advisor") {
    $issues += 'agents/openai.yaml default_prompt must mention $youyou-ai-product-advisor'
  }
}

$manifestPath = Join-Path $packageRoot "manifest\skill-pack.json"
if (Test-Path -LiteralPath $manifestPath) {
  $manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json
  if ($manifest.name -ne "youyou-ai-product-advisor") {
    $issues += "Manifest name mismatch"
  }
}

if ($CheckInstalled) {
  $installed = Join-Path $SkillsRoot "youyou-ai-product-advisor\SKILL.md"
  if (!(Test-Path -LiteralPath $installed)) {
    $issues += "Installed skill not found at $installed"
  }
}

if ($issues.Count -gt 0) {
  $issues | ForEach-Object { Write-Host "[FAIL] $_" }
  throw "Verification failed with $($issues.Count) issue(s)."
}

node (Join-Path $skillDir "scripts\smoke-test.mjs")
Write-Host "Youyou AI Product Advisor skill pack verification passed."
