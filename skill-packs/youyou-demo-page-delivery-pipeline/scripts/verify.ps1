param([string]$CodexSkillsDir = "", [switch]$InstalledOnly)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) { $CodexSkillsDir = Join-Path $homeDir ".codex\skills" }
$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$name = Split-Path $repoRoot -Leaf
$path = if ($InstalledOnly) { Join-Path $CodexSkillsDir $name } else { Join-Path (Join-Path $repoRoot "skills") $name }
if (-not (Test-Path -LiteralPath (Join-Path $path "SKILL.md"))) { throw "Missing SKILL.md: $path" }
if (-not (Test-Path -LiteralPath (Join-Path $path "agents\openai.yaml"))) { throw "Missing agents/openai.yaml: $path" }
$requiredDocs = @(
  "README.md",
  "docs\FEATURES.md",
  "docs\INSTALLATION.md",
  "docs\WORKFLOWS.md",
  "docs\SECURITY.md",
  "docs\GITHUB_UPLOAD.md",
  "examples\prompts.md",
  "manifest\skill-pack.json",
  "manifest\companion-skills.json"
)
foreach ($rel in $requiredDocs) {
  if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $rel))) { throw "Missing package file: $rel" }
}
Write-Host "OK $name -> $path"
$validator = Join-Path $homeDir ".codex\skills\.system\skill-creator\scripts\quick_validate.py"
if (Test-Path -LiteralPath $validator) { python $validator $path }

