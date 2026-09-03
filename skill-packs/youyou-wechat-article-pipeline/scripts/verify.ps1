param(
  [switch]$CheckInstalled,
  [string]$SkillsRoot = "$env:USERPROFILE\.workbuddy\skills"
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$required = @(
  "README.md", "THIRD_PARTY_NOTICES.md", "docs\FEATURES.md", "docs\INSTALLATION.md",
  "docs\WORKFLOWS.md", "docs\SECURITY.md", "docs\GITHUB_UPLOAD.md", "examples\prompts.md",
  "manifest\skill-pack.json", "manifest\companion-skills.json", "scripts\install.ps1",
  "scripts\install-companion-skills.ps1", "skills\youyou-wechat-article-pipeline\SKILL.md",
  "skills\youyou-wechat-article-pipeline\agents\openai.yaml"
)
$issues = @()
foreach ($rel in $required) {
  $path = Join-Path $packageRoot $rel
  if (!(Test-Path -LiteralPath $path)) { $issues += "Missing $rel" }
  elseif ((Get-Item -LiteralPath $path).Length -eq 0) { $issues += "Empty $rel" }
}
$skillPath = Join-Path $packageRoot "skills\youyou-wechat-article-pipeline\SKILL.md"
$skillDirectory = Split-Path -Parent $skillPath
if ((Get-ChildItem -LiteralPath $skillDirectory -Filter "*.md" | Where-Object { $_.Name -ne "SKILL.md" }).Count -lt 1) {
  $issues += "Localized usage manual is missing"
}
if (Test-Path -LiteralPath $skillPath) {
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $skillPath
  if ($text -notmatch '(?s)^---\s*.*name:\s*youyou-wechat-article-pipeline.*description:\s*.+?---') { $issues += "SKILL.md frontmatter is incomplete" }
  if ($text -match 'C:/Users/\d+' -or $text -match 'C:\\Users\\\d+') { $issues += "Personal Windows user path found" }
}
$manifestPath = Join-Path $packageRoot "manifest\skill-pack.json"
if (Test-Path -LiteralPath $manifestPath) {
  $manifest = Get-Content -Raw -Encoding UTF8 -LiteralPath $manifestPath | ConvertFrom-Json
  if ($manifest.name -ne "youyou-wechat-article-pipeline") { $issues += "Manifest name mismatch" }
  if ($manifest.runtime -ne "WorkBuddy") { $issues += "Manifest runtime mismatch" }
}
if ($CheckInstalled -and !(Test-Path -LiteralPath (Join-Path $SkillsRoot "youyou-wechat-article-pipeline\SKILL.md"))) {
  $issues += "Installed skill not found"
}
if ($issues.Count -gt 0) {
  $issues | ForEach-Object { Write-Host "[FAIL] $_" }
  throw "Verification failed with $($issues.Count) issue(s)."
}
Write-Host "Skill pack verification passed."
