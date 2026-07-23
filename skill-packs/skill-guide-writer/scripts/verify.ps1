param(
    [string]$CodexSkillsDir = "",
    [switch]$InstalledOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

$userHome = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
    $CodexSkillsDir = Join-Path $userHome ".codex\skills"
}

$packRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$skillName = "skill-guide-writer"
$skillPath = if ($InstalledOnly) {
    Join-Path $CodexSkillsDir $skillName
} else {
    Join-Path (Join-Path $packRoot "skills") $skillName
}

$requiredFiles = @(
    "SKILL.md",
    "agents\openai.yaml",
    "assets\skill-guide-template.md",
    "references\guide-spec.md",
    "scripts\inventory_skill.py"
)

foreach ($relativePath in $requiredFiles) {
    $candidate = Join-Path $skillPath $relativePath
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw "Missing required file: $candidate"
    }
}

$validator = Join-Path $userHome ".codex\skills\.system\skill-creator\scripts\quick_validate.py"
if (Test-Path -LiteralPath $validator) {
    python $validator $skillPath
    if ($LASTEXITCODE -ne 0) {
        throw "quick_validate.py failed for $skillPath"
    }
} else {
    Write-Warning "Codex quick validator not found; structural checks still completed."
}

$inventoryScript = Join-Path $skillPath "scripts\inventory_skill.py"
$temporaryInventory = [System.IO.Path]::GetTempFileName()
try {
    python $inventoryScript $skillPath --output $temporaryInventory
    if ($LASTEXITCODE -ne 0) {
        throw "inventory_skill.py failed for $skillPath"
    }
    $inventory = Get-Content -LiteralPath $temporaryInventory -Encoding UTF8 -Raw | ConvertFrom-Json
    if ($inventory.frontmatter.name -ne $skillName) {
        throw "Unexpected skill name in inventory: $($inventory.frontmatter.name)"
    }
    if ($inventory.files.Count -lt $requiredFiles.Count) {
        throw "Inventory returned too few files: $($inventory.files.Count)"
    }
} finally {
    if (Test-Path -LiteralPath $temporaryInventory) {
        Remove-Item -LiteralPath $temporaryInventory -Force
    }
}

Write-Host "OK $skillName -> $skillPath"
Write-Host "Required files: $($requiredFiles.Count); inventoried files: $($inventory.files.Count)"
