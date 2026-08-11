param(
    [string]$CodexSkillsDir = "",
    [switch]$InstalledOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

$packRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$manifestPath = Join-Path $packRoot "manifest\skill-pack.json"
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$skillName = [string]$manifest.skill.name

if ([string]::IsNullOrWhiteSpace($CodexSkillsDir)) {
    if ([string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
        throw "USERPROFILE is unavailable; pass -CodexSkillsDir explicitly."
    }
    $CodexSkillsDir = Join-Path $env:USERPROFILE ".codex\skills"
}

$skillPath = if ($InstalledOnly) {
    Join-Path $CodexSkillsDir $skillName
} else {
    Join-Path $packRoot ([string]$manifest.skill.path).Replace("/", "\")
}

$requiredFiles = @("SKILL.md", "contracts\workflow_contract.json")
foreach ($relativePath in $requiredFiles) {
    $candidate = Join-Path $skillPath $relativePath
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw "Missing required file: $candidate"
    }
}

$skillText = Get-Content -LiteralPath (Join-Path $skillPath "SKILL.md") -Raw -Encoding UTF8
if ($skillText -notmatch "(?ms)^---\s*.*?^name:\s*$([regex]::Escape($skillName))\s*$.*?^description:\s*.+?^---\s*$") {
    throw "SKILL.md frontmatter does not match manifest skill name: $skillName"
}

$workflowContract = Get-Content -LiteralPath (Join-Path $skillPath "contracts\workflow_contract.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$workflows = @($workflowContract)
if ($workflows.Count -ne [int]$manifest.skill.workflowCount) {
    throw "Workflow count mismatch: expected $($manifest.skill.workflowCount), got $($workflows.Count)"
}
$workflowIds = @($workflows | ForEach-Object { [string]$_.workflow_id })
if (@($workflowIds | Where-Object { [string]::IsNullOrWhiteSpace($_) }).Count -gt 0) {
    throw "One or more workflows have an empty workflow_id."
}
if (@($workflowIds | Sort-Object -Unique).Count -ne $workflowIds.Count) {
    throw "workflow_id values are not unique."
}

$hashMap = @{}
$relativePaths = @()
$sha = [System.Security.Cryptography.SHA256]::Create()
# Canonical UTF-8/LF content hashing remains stable across Git and Windows line-ending conversions.
$utf8Strict = [System.Text.UTF8Encoding]::new($false, $true)
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
try {
    foreach ($file in Get-ChildItem -LiteralPath $skillPath -Recurse -File) {
        $relative = $file.FullName.Substring($skillPath.Length).TrimStart("\").Replace("\", "/")
        $text = [System.IO.File]::ReadAllText($file.FullName, $utf8Strict)
        $canonicalText = $text.Replace("`r`n", "`n").Replace("`r", "`n")
        $canonicalBytes = $utf8NoBom.GetBytes($canonicalText)
        $hashMap[$relative] = ([System.BitConverter]::ToString($sha.ComputeHash($canonicalBytes))).Replace("-", "")
        $relativePaths += $relative
    }
    $orderedPaths = [string[]]$relativePaths
    [Array]::Sort($orderedPaths, [System.StringComparer]::Ordinal)
    $treeLines = @($orderedPaths | ForEach-Object { "$_`t$($hashMap[$_])" })
    $treePayload = [string]::Join("`n", $treeLines)
    $treeBytes = $utf8NoBom.GetBytes($treePayload)
    $treeHash = ([System.BitConverter]::ToString($sha.ComputeHash($treeBytes))).Replace("-", "")
} finally {
    $sha.Dispose()
}
if ($orderedPaths.Count -ne [int]$manifest.skill.sourceFileCount) {
    throw "Source file count mismatch: expected $($manifest.skill.sourceFileCount), got $($orderedPaths.Count)"
}
if ($treeHash -ne [string]$manifest.skill.sourceTreeSha256) {
    throw "Source tree hash mismatch: expected $($manifest.skill.sourceTreeSha256), got $treeHash"
}

$validator = if ($env:USERPROFILE) { Join-Path $env:USERPROFILE ".codex\skills\.system\skill-creator\scripts\quick_validate.py" } else { "" }
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python -and $validator -and (Test-Path -LiteralPath $validator -PathType Leaf)) {
    & $python.Source $validator $skillPath
    if ($LASTEXITCODE -ne 0) { throw "quick_validate.py failed for $skillPath" }
} else {
    Write-Warning "Codex quick validator or Python was not found; manifest, structure and workflow checks still completed."
}

if ([bool]$manifest.validation.renderer.enabled) {
    if (-not $python) { throw "Python is required for the bundled renderer smoke test." }
    $renderer = Join-Path $skillPath ([string]$manifest.validation.renderer.script).Replace("/", "\")
    $demoInput = Join-Path $skillPath ([string]$manifest.validation.renderer.demoInput).Replace("/", "\")
    $temporaryOutput = [System.IO.Path]::GetTempFileName()
    try {
        & $python.Source $renderer $demoInput $temporaryOutput | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Renderer smoke test failed." }
        $rendered = Get-Content -LiteralPath $temporaryOutput -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($rendered.mode -ne [string]$manifest.validation.renderer.expectedMode) { throw "Unexpected renderer mode: $($rendered.mode)" }
        if ([int]$rendered.formal_write_count -ne 0 -or @($rendered.formal_records).Count -ne 0) {
            throw "Activation renderer created formal writes or formal records."
        }
    } finally {
        if (Test-Path -LiteralPath $temporaryOutput) { Remove-Item -LiteralPath $temporaryOutput -Force }
    }
}

Write-Host "OK $skillName -> $skillPath"
Write-Host "Source files: $($orderedPaths.Count); workflows: $($workflows.Count); tree SHA-256: $treeHash"
