param([string]$CodexSkillsDir = "")
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
  $CodexSkillsDir = Join-Path $homeDir ".codex\skills"
}

$installer = Join-Path $homeDir ".codex\skills\.system\skill-installer\scripts\install-skill-from-github.py"
if (-not (Test-Path -LiteralPath $installer)) {
  throw "Missing Codex skill installer: $installer"
}

$companions = @(
  @{ Name = "just-scrape"; Repo = "ScrapeGraphAI/just-scrape"; Path = "skills/just-scrape" },
  @{ Name = "lark-shared"; Repo = "larksuite/cli"; Path = "skills/lark-shared" },
  @{ Name = "lark-base"; Repo = "larksuite/cli"; Path = "skills/lark-base" },
  @{ Name = "cold-email"; Repo = "coreyhaines31/marketingskills"; Path = "skills/cold-email" }
)

foreach ($skill in $companions) {
  $dest = Join-Path $CodexSkillsDir $skill.Name
  if (Test-Path -LiteralPath (Join-Path $dest "SKILL.md")) {
    Write-Host "Already installed: $($skill.Name)"
    continue
  }

  python $installer --repo $skill.Repo --path $skill.Path --method git --dest $CodexSkillsDir
}

function Remove-FrontmatterKeys {
  param([string]$SkillName, [string[]]$Keys)
  $skillPath = Join-Path (Join-Path $CodexSkillsDir $SkillName) "SKILL.md"
  if (-not (Test-Path -LiteralPath $skillPath)) { return }

  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  $text = [System.IO.File]::ReadAllText($skillPath, $utf8NoBom)
  if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) {
    $text = $text.Substring(1)
  }

  $match = [regex]::Match($text, "\A---\r?\n(?<frontmatter>.*?)(\r?\n)---", [System.Text.RegularExpressions.RegexOptions]::Singleline)
  if (-not $match.Success) {
    [System.IO.File]::WriteAllText($skillPath, $text, $utf8NoBom)
    return
  }

  $frontmatter = $match.Groups["frontmatter"].Value
  foreach ($key in $Keys) {
    $frontmatter = [regex]::Replace($frontmatter, "(?m)^" + [regex]::Escape($key) + ":.*\r?\n?", "")
  }

  $updated = "---`n" + $frontmatter.TrimEnd("`r", "`n") + "`n---" + $text.Substring($match.Length)
  if ($updated -ne $text) {
    [System.IO.File]::WriteAllText($skillPath, $updated, $utf8NoBom)
    Write-Host "Normalized metadata: $SkillName"
  }
}

Remove-FrontmatterKeys -SkillName "just-scrape" -Keys @("compatibility")
Remove-FrontmatterKeys -SkillName "lark-shared" -Keys @("version")
Remove-FrontmatterKeys -SkillName "lark-base" -Keys @("version")

$validator = Join-Path $homeDir ".codex\skills\.system\skill-creator\scripts\quick_validate.py"
if (Test-Path -LiteralPath $validator) {
  foreach ($skill in $companions) {
    $path = Join-Path $CodexSkillsDir $skill.Name
    if (Test-Path -LiteralPath (Join-Path $path "SKILL.md")) {
      python $validator $path
    }
  }
}

Write-Host "Companion skill installation complete."
Write-Host "Restart Codex or open a new session."
