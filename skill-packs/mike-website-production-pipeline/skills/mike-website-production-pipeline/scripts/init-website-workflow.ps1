param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectRoot
)

$ErrorActionPreference = "Stop"
$root = [IO.Path]::GetFullPath($ProjectRoot)
if (!(Test-Path -LiteralPath $root -PathType Container)) {
  throw "Project root does not exist: $root"
}

$workflowRoot = Join-Path $root "docs\website-workflow"
New-Item -ItemType Directory -Path $workflowRoot -Force | Out-Null

$templates = [ordered]@{
  "CURRENT_STATUS.md" = @"
# Current status

- Status: DISCOVERY_IN_PROGRESS
- Current Gate: Preflight
- Visual source route: UNSET
- User visual approval: NO
- Release authority: NO
- Production validation: NO

## Open blockers

- None recorded.
"@
  "SITE_BRIEF.md" = @"
# Site brief

## Product

## Audience

## Intended user outcome

## Offer and evidence

## Primary action

## Routes

## Content-source boundaries
"@
  "VISUAL_SOURCE.md" = @"
# Visual source

- Route: FIGMA | IDEATE | REFERENCE | CLONE | DNA | REDESIGN
- Source URL/path:
- Selected node/option/state:
- Target viewport:
- Approved by:
- Protected elements:
"@
  "HEADING_BUDGET.md" = @"
# Heading budget

| Route/section | Level | Final text | Desktop max lines | Mobile max lines | Exception reason |
|---|---|---|---:|---:|---|
"@
  "LAYOUT_RULES.md" = @"
# Layout rules

## Container and grid

## Shared alignment lines

## Section density

## Mobile recomposition

## Forbidden patterns
"@
  "MOTION_SPEC.md" = @"
# Motion specification

| Motion | Trigger | Purpose | Target/property | Duration/ease | Interrupt | Mobile | Reduced motion | Cleanup |
|---|---|---|---|---|---|---|---|---|
"@
  "QA_REPORT.md" = @"
# QA report

## Build identity

## Viewports and states

## Design comparison

## Clarity gate

## Responsive and accessibility

## Motion quality

## Technical checks

## Findings

## Final result

BLOCKED
"@
  "RELEASE_REPORT.md" = @"
# Release report

- Status: RELEASE_BLOCKED
- Production URL:
- Deployment ID:
- Previous rollback ID:
- Commit/build:
- Approved baseline:
- Production QA evidence:
"@
}

$created = @()
$preserved = @()
foreach ($entry in $templates.GetEnumerator()) {
  $target = Join-Path $workflowRoot $entry.Key
  if (Test-Path -LiteralPath $target) {
    $preserved += $target
    continue
  }
  Set-Content -LiteralPath $target -Value $entry.Value -Encoding UTF8
  $created += $target
}

Write-Host "Website workflow initialized: $workflowRoot" -ForegroundColor Green
Write-Host "Created: $($created.Count); preserved existing: $($preserved.Count)"
foreach ($item in $created) { Write-Host "[CREATED] $item" }
foreach ($item in $preserved) { Write-Host "[PRESERVED] $item" }
