param([switch]$CheckInstalled,[string]$SkillsRoot="$env:USERPROFILE\.codex\skills")
$ErrorActionPreference="Stop"
$packageRoot=Split-Path -Parent $PSScriptRoot
$required=@("README.md","install.bat","manifest\skill-pack.json","scripts\install.ps1","scripts\verify.ps1","skills\mike-web-clarity-gate\SKILL.md","skills\mike-web-clarity-gate\agents\openai.yaml","skills\mike-web-clarity-gate\references\rubric.md","skills\mike-web-clarity-gate\scripts\audit-layout.mjs")
$issues=@()
foreach($rel in $required){if(!(Test-Path -LiteralPath (Join-Path $packageRoot $rel))){$issues+="Missing $rel"}}
$skill=Join-Path $packageRoot "skills\mike-web-clarity-gate\SKILL.md"
if(Test-Path -LiteralPath $skill){$text=Get-Content -Raw -Encoding UTF8 $skill;if($text -notmatch "(?s)^---\s*.*name:\s*mike-web-clarity-gate.*description:\s*.+?---"){$issues+="SKILL.md frontmatter is incomplete"};foreach($term in @("BUILD","AUDIT","CLARITY_GATE_PASS","CLARITY_GATE_FAIL")){if($text -notmatch [regex]::Escape($term)){$issues+="SKILL.md missing standard: $term"}}}
$yaml=Join-Path $packageRoot "skills\mike-web-clarity-gate\agents\openai.yaml"
if(Test-Path -LiteralPath $yaml){if((Get-Content -Raw -Encoding UTF8 $yaml) -notmatch '\$mike-web-clarity-gate'){$issues+='openai.yaml default_prompt must mention $mike-web-clarity-gate'}}
if($CheckInstalled -and !(Test-Path -LiteralPath (Join-Path $SkillsRoot "mike-web-clarity-gate\SKILL.md"))){$issues+="Installed skill not found"}
if($issues.Count){$issues|ForEach-Object{Write-Host "[FAIL] $_"};throw "Verification failed with $($issues.Count) issue(s)."}
Write-Host "Mike Web Clarity Gate skill pack verification passed." -ForegroundColor Green
