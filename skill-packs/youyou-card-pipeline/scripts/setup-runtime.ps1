param([ValidateSet('Codex','WorkBuddy')][string]$HostTarget='Codex',[string]$SkillDirectory,[switch]$InstallChromium)
$ErrorActionPreference='Stop'
if(!$SkillDirectory){$folder=if($HostTarget -eq 'Codex'){'.codex'}else{'.workbuddy'};$SkillDirectory=Join-Path $env:USERPROFILE "$folder/skills/youyou-card-pipeline"}
Push-Location -LiteralPath $SkillDirectory
try{
 & npm.cmd install --ignore-scripts
 if($LASTEXITCODE -ne 0){throw 'npm install failed'}
 if($InstallChromium){& npx.cmd playwright install chromium;if($LASTEXITCODE -ne 0){throw 'Browser download failed'}}
}finally{Pop-Location}
