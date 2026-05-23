param(
  [string]$CodexSkillsDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
  $CodexSkillsDir = Join-Path $homeDir ".codex\skills"
}

$installer = Join-Path $homeDir ".codex\skills\.system\skill-installer\scripts\install-skill-from-github.py"
if (-not (Test-Path -LiteralPath $installer)) {
  throw "Codex skill installer not found: $installer"
}

$items = @(
  @{ Repo = "vercel-labs/agent-skills"; Path = "skills/react-best-practices"; Name = "vercel-react-best-practices" },
  @{ Repo = "vercel-labs/agent-skills"; Path = "skills/web-design-guidelines"; Name = $null },
  @{ Repo = "microsoft/github-copilot-for-azure"; Path = "plugin/skills/microsoft-foundry"; Name = $null },
  @{ Repo = "microsoft/github-copilot-for-azure"; Path = "plugin/skills/azure-ai"; Name = $null },
  @{ Repo = "microsoft/github-copilot-for-azure"; Path = "plugin/skills/azure-aigateway"; Name = $null },
  @{ Repo = "microsoft/github-copilot-for-azure"; Path = "plugin/skills/azure-prepare"; Name = $null },
  @{ Repo = "microsoft/github-copilot-for-azure"; Path = "plugin/skills/azure-validate"; Name = $null },
  @{ Repo = "microsoft/github-copilot-for-azure"; Path = "plugin/skills/azure-deploy"; Name = $null }
)

foreach ($item in $items) {
  $args = @($installer, "--repo", $item.Repo, "--path", $item.Path, "--dest", $CodexSkillsDir, "--method", "git")
  if ($item.Name) { $args += @("--name", $item.Name) }
  python @args
}

