param(
  [switch]$CheckInstalled,
  [switch]$CheckLinks,
  [string]$SkillsRoot = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$skillDir = Join-Path $packageRoot "skills\youyou-inorganic-board-guide"
$required = @(
  "README.md",
  "THIRD_PARTY_NOTICES.md",
  "docs\FEATURES.md",
  "docs\INSTALLATION.md",
  "docs\WORKFLOWS.md",
  "docs\SECURITY.md",
  "docs\GITHUB_UPLOAD.md",
  "examples\prompts.md",
  "manifest\skill-pack.json",
  "manifest\companion-skills.json",
  "scripts\install.ps1",
  "scripts\install-companion-skills.ps1",
  "scripts\verify.ps1",
  "skills\youyou-inorganic-board-guide\SKILL.md",
  "skills\youyou-inorganic-board-guide\agents\openai.yaml",
  "skills\youyou-inorganic-board-guide\references\knowledge-map.md",
  "skills\youyou-inorganic-board-guide\references\audience-playbooks.md",
  "skills\youyou-inorganic-board-guide\references\website-router.md",
  "skills\youyou-inorganic-board-guide\references\image-router.md",
  "skills\youyou-inorganic-board-guide\references\faq-and-sales-scripts.md",
  "skills\youyou-inorganic-board-guide\references\response-templates.md",
  "skills\youyou-inorganic-board-guide\references\claim-safety-checklist.md",
  "skills\youyou-inorganic-board-guide\references\sample-outputs.md",
  "skills\youyou-inorganic-board-guide\scripts\check-links.mjs",
  "skills\youyou-inorganic-board-guide\scripts\find-gallery-images.mjs",
  "skills\youyou-inorganic-board-guide\scripts\smoke-test.mjs"
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
  if ($text -notmatch "(?s)^---\s*.*name:\s*youyou-inorganic-board-guide.*description:\s*.+?---") {
    $issues += "SKILL.md frontmatter is incomplete"
  }
  if ($text -notmatch "First Response") {
    $issues += "SKILL.md does not include first-response guidance"
  }
  if ($text -notmatch "Service Modes") {
    $issues += "SKILL.md does not include service modes"
  }
  if ($text -notmatch "OCR" -or $text -notmatch "image-router.md") {
    $issues += "SKILL.md does not include OCR image matching guidance"
  }
  if ($text -match "Create only the resource directories") {
    $issues += "SKILL.md still contains template residue"
  }
}

$openaiYaml = Join-Path $skillDir "agents\openai.yaml"
if (Test-Path $openaiYaml) {
  $yaml = Get-Content -Raw -Encoding UTF8 $openaiYaml
  if ($yaml -notmatch "\$youyou-inorganic-board-guide") {
    $issues += "agents/openai.yaml default_prompt must mention `$youyou-inorganic-board-guide"
  }
}

$manifestPath = Join-Path $packageRoot "manifest\skill-pack.json"
if (Test-Path $manifestPath) {
  $manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json
  if ($manifest.name -ne "youyou-inorganic-board-guide") {
    $issues += "Manifest name mismatch"
  }
}

if ($CheckInstalled) {
  $installed = Join-Path $SkillsRoot "youyou-inorganic-board-guide\SKILL.md"
  if (!(Test-Path $installed)) {
    $issues += "Installed skill not found at $installed"
  }
}

if ($issues.Count -gt 0) {
  $issues | ForEach-Object { Write-Host "[FAIL] $_" }
  throw "Verification failed with $($issues.Count) issue(s)."
}

node (Join-Path $skillDir "scripts\smoke-test.mjs")

if ($CheckLinks) {
  node (Join-Path $skillDir "scripts\check-links.mjs")
  $galleryQuery = "$([char]0x9632)$([char]0x6f6e) $([char]0x56de)$([char]0x5357)$([char]0x5929) $([char]0x53a8)$([char]0x536b)"
  node (Join-Path $skillDir "scripts\find-gallery-images.mjs") $galleryQuery --limit 2
}

Write-Host "Skill pack verification passed."
