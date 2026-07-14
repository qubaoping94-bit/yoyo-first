param([switch]$CheckInstalled,[string]$SkillsRoot="$env:USERPROFILE\\.codex\\skills")
$ErrorActionPreference="Stop"
$packageRoot=Split-Path -Parent $PSScriptRoot
$required=@("README.md","install.bat","manifest\\skill-pack.json","scripts\\install.ps1","scripts\\verify.ps1","skills\\mike-cover-flow\\SKILL.md","skills\\mike-cover-flow\\agents\\openai.yaml")
$issues=@()
foreach($rel in $required){if(!(Test-Path -LiteralPath (Join-Path $packageRoot $rel))){$issues+="Missing $rel"}}
$skill=Join-Path $packageRoot "skills\\mike-cover-flow\\SKILL.md"
if(Test-Path -LiteralPath $skill){$text=Get-Content -Raw -Encoding UTF8 $skill;if($text -notmatch "(?s)^---\s*.*name:\s*mike-cover-flow.*description:\s*.+?---"){$issues+="SKILL.md frontmatter is incomplete"};foreach($term in @("continuous floating-point","windowed","pixel sampling","prefers-reduced-motion")){if($text -notmatch [regex]::Escape($term)){$issues+="SKILL.md missing standard: $term"}}}
$yaml=Join-Path $packageRoot "skills\\mike-cover-flow\\agents\\openai.yaml"
if(Test-Path -LiteralPath $yaml){if((Get-Content -Raw -Encoding UTF8 $yaml) -notmatch '\$mike-cover-flow'){$issues+='openai.yaml default_prompt must mention $mike-cover-flow'}}
if($CheckInstalled -and !(Test-Path -LiteralPath (Join-Path $SkillsRoot "mike-cover-flow\\SKILL.md"))){$issues+="Installed skill not found"}
if($issues.Count){$issues|ForEach-Object{Write-Host "[FAIL] $_"};throw "Verification failed with $($issues.Count) issue(s)."}
Write-Host "Mike Cover Flow skill pack verification passed." -ForegroundColor Green
