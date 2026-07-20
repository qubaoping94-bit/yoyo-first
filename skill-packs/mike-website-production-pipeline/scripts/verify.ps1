param([switch]$CheckInstalled,[string]$SkillsRoot="$env:USERPROFILE\.codex\skills")
$ErrorActionPreference="Stop"
$packageRoot=Split-Path -Parent $PSScriptRoot
$required=@("README.md","install.bat","manifest\skill-pack.json","scripts\install.ps1","scripts\verify.ps1","skills\mike-website-production-pipeline\SKILL.md","skills\mike-website-production-pipeline\agents\openai.yaml","skills\mike-website-production-pipeline\references\full-workflow.md","skills\mike-website-production-pipeline\scripts\init-website-workflow.ps1")
$issues=@()
foreach($rel in $required){if(!(Test-Path -LiteralPath (Join-Path $packageRoot $rel))){$issues+="Missing $rel"}}
$skill=Join-Path $packageRoot "skills\mike-website-production-pipeline\SKILL.md"
if(Test-Path -LiteralPath $skill){$text=Get-Content -Raw -Encoding UTF8 $skill;if($text -notmatch "(?s)^---\s*.*name:\s*mike-website-production-pipeline.*description:\s*.+?---"){$issues+="SKILL.md frontmatter is incomplete"};foreach($term in @("FIGMA","IDEATE","STATIC_QA_PASS","DELIVERY_APPROVED","PRODUCTION_VALIDATED")){if($text -notmatch [regex]::Escape($term)){$issues+="SKILL.md missing standard: $term"}}}
$yaml=Join-Path $packageRoot "skills\mike-website-production-pipeline\agents\openai.yaml"
if(Test-Path -LiteralPath $yaml){if((Get-Content -Raw -Encoding UTF8 $yaml) -notmatch '\$mike-website-production-pipeline'){$issues+='openai.yaml default_prompt must mention $mike-website-production-pipeline'}}
if($CheckInstalled -and !(Test-Path -LiteralPath (Join-Path $SkillsRoot "mike-website-production-pipeline\SKILL.md"))){$issues+="Installed skill not found"}
if($issues.Count){$issues|ForEach-Object{Write-Host "[FAIL] $_"};throw "Verification failed with $($issues.Count) issue(s)."}
Write-Host "Mike Website Production Pipeline skill pack verification passed." -ForegroundColor Green
