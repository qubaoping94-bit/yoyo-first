param([string]$OutputRoot=(Join-Path $env:TEMP 'internal-brief-verification'))
$ErrorActionPreference='Stop'
$pack=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$manifest=Get-Content -LiteralPath (Join-Path $pack 'manifest\skill-pack.json') -Raw | ConvertFrom-Json
foreach($entry in $manifest.files){$file=Join-Path $pack $entry.path;if(-not(Test-Path -LiteralPath $file)){throw "Missing $($entry.path)"};if((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256){throw "Hash mismatch $($entry.path)"}}
$skill=Join-Path $pack 'skills\internal-cooperation-brief'
foreach($name in @('render.cjs','export.cjs','check.cjs')){& node --check (Join-Path $skill "scripts\$name");if($LASTEXITCODE -ne 0){throw "Syntax failed: $name"}}
& node (Join-Path $skill 'scripts\check.cjs') $OutputRoot
if($LASTEXITCODE -ne 0){throw 'Behavior checks failed'}
Write-Output 'PASS: manifest hashes, scripts, input validation and no-overwrite'
