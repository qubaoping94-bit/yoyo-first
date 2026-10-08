param([string]$SkillDirectory)
$ErrorActionPreference='Stop'
$packRoot=Split-Path $PSScriptRoot -Parent
if(!$SkillDirectory){$SkillDirectory=Join-Path $packRoot 'skills/youyou-card-pipeline'}
$files=@('SKILL.md','agents/openai.yaml','package.json','assets/template.html','assets/deck.example.json','references/layout-map.md','references/copy-rules.md','references/environment.md','scripts/build_deck.py','scripts/count_body_chars.py','scripts/browser-runtime.mjs','scripts/render_deck.mjs','scripts/validate_deck.mjs')
foreach($relative in $files){if(!(Test-Path -LiteralPath (Join-Path $SkillDirectory $relative) -PathType Leaf)){throw "Missing $relative"}}
$entry=Get-Content -LiteralPath (Join-Path $SkillDirectory 'SKILL.md') -Raw -Encoding UTF8
if($entry -notmatch 'name: youyou-card-pipeline' -or $entry -notmatch 'Codex' -or $entry -notmatch 'WorkBuddy'){throw 'Invalid skill identity'}
$deck=Get-Content -LiteralPath (Join-Path $SkillDirectory 'assets/deck.example.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if($deck.cards.Count -ne 8){throw 'Sample must contain 8 cards'}
$manifest=Get-Content -LiteralPath (Join-Path $packRoot 'manifest/skill-pack.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($entry in $manifest.files){
 $actual=(Get-FileHash -LiteralPath (Join-Path $SkillDirectory $entry.path) -Algorithm SHA256).Hash.ToLowerInvariant()
 if($actual -ne $entry.sha256){throw "Hash mismatch: $($entry.path)"}
}
Write-Output "PASS structure and $($manifest.files.Count) file hashes: $SkillDirectory"
