$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$skill = Join-Path $root 'skills\youyou-dealer-ppt'
$required = @('README.md','manifest\skill-pack.json','scripts\install.ps1','scripts\verify.ps1','skills\youyou-dealer-ppt\SKILL.md','skills\youyou-dealer-ppt\agents\openai.yaml','skills\youyou-dealer-ppt\references\approved-baseline.md','skills\youyou-dealer-ppt\references\fidelity-contract.md','skills\youyou-dealer-ppt\references\content-boundaries.md','skills\youyou-dealer-ppt\references\design-system.md','skills\youyou-dealer-ppt\references\motion-system.md','skills\youyou-dealer-ppt\references\qa-gates.md','skills\youyou-dealer-ppt\assets\approved-21-fixture.html','skills\youyou-dealer-ppt\assets\approved-black-red-template.html','skills\youyou-dealer-ppt\assets\approved-black-red-density.css','skills\youyou-dealer-ppt\scripts\audit-fidelity.py')
foreach ($rel in $required) { if (!(Test-Path -LiteralPath (Join-Path $root $rel))) { throw "Missing $rel" } }
$text = Get-Content -Raw -Encoding UTF8 (Join-Path $skill 'SKILL.md')
if ($text -notmatch '(?s)^---\s*name:\s*youyou-dealer-ppt\s*description:\s*.+?---') { throw 'Invalid skill frontmatter' }
foreach ($term in @('2026-09-27','references/approved-baseline.md','references/fidelity-contract.md','references/content-boundaries.md','scripts/audit-fidelity.py')) { if (!$text.Contains($term)) { throw "Missing standard: $term" } }
$manifest = Get-Content -Raw -Encoding UTF8 (Join-Path $root 'manifest\skill-pack.json') | ConvertFrom-Json
if ($manifest.name -ne 'youyou-dealer-ppt') { throw 'Manifest mismatch' }
if ($manifest.version -ne '2.1.0') { throw 'Manifest version mismatch' }
$hashes = @{
  'assets\approved-black-red-template.html'='924DCA7EF658263D8292BBAA4FBAD39BD7281FEB70C529D01A5E2EA55808BA25'
  'assets\approved-black-red-density.css'='34F6C88E76E07FC0B061147C9E6BA94CA7D219F6B14DB22C0202FCF240219248'
}
foreach ($rel in $hashes.Keys) { $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $skill $rel)).Hash; if ($actual -ne $hashes[$rel]) { throw "Baseline asset changed: $rel" } }
$forbidden = Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object { $_.Extension -in @('.exe','.lnk','.sqlite','.db') -or $_.FullName -match 'runtime-profile' }
if ($forbidden) { throw 'Executable, shortcut, database or runtime profile must not be published' }
$python = Get-Command python -ErrorAction SilentlyContinue
if (!$python) { throw 'Python 3 is required for fixture audit' }
& $python.Source -X utf8 (Join-Path $skill 'scripts\audit-fidelity.py') (Join-Path $skill 'assets\approved-21-fixture.html') | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Approved 21-style fixture audit failed' }
Write-Host 'youyou-dealer-ppt pack verification passed.'
