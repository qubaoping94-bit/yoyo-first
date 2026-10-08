param([ValidateSet('Codex','WorkBuddy','Both')][string]$HostTarget='Both',[string]$UserRoot=$env:USERPROFILE)
$ErrorActionPreference='Stop'
$packRoot=Split-Path $PSScriptRoot -Parent
$source=Join-Path $packRoot 'skills/youyou-card-pipeline'
& (Join-Path $PSScriptRoot 'verify.ps1')
$hosts=if($HostTarget -eq 'Both'){@('Codex','WorkBuddy')}else{@($HostTarget)}
foreach($hostName in $hosts){
 $folder=if($hostName -eq 'Codex'){'.codex'}else{'.workbuddy'}
 $hostRoot=Join-Path $UserRoot $folder
 $destination=Join-Path $hostRoot 'skills/youyou-card-pipeline'
 if(Test-Path -LiteralPath $destination){
  $backup=Join-Path $hostRoot ('skill-backups/youyou-card-pipeline-'+(Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
  New-Item -ItemType Directory -Path (Split-Path $backup -Parent) -Force | Out-Null
  Move-Item -LiteralPath $destination -Destination $backup
  Write-Output "BACKUP $backup"
 }
 New-Item -ItemType Directory -Path $destination -Force | Out-Null
 Get-ChildItem -LiteralPath $source -Force | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force}
 Write-Output "INSTALLED $hostName $destination"
}
