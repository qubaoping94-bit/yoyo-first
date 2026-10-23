param(
  [ValidateSet('Codex','WorkBuddy','Both')][string]$Target='Both',
  [string]$DestinationRoot
)
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot '..\skills\internal-cooperation-brief'
if(-not(Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))){throw 'Skill source missing'}
if($DestinationRoot -and $Target -eq 'Both'){throw 'Custom destination supports one target at a time'}
$targets=if($Target -eq 'Both'){@('Codex','WorkBuddy')}else{@($Target)}
$plans=@()
foreach($item in $targets){
  $root=if($DestinationRoot){[IO.Path]::GetFullPath($DestinationRoot)}elseif($item -eq 'Codex'){Join-Path $env:USERPROFILE '.codex\skills'}else{Join-Path $env:USERPROFILE '.workbuddy\skills'}
  $dest=Join-Path $root 'internal-cooperation-brief'
  $same=Test-Path -LiteralPath $dest
  if($same){foreach($file in Get-ChildItem -LiteralPath $source -Recurse -File){$rel=$file.FullName.Substring(([IO.Path]::GetFullPath($source)).TrimEnd('\').Length+1);$other=Join-Path $dest $rel;if(-not(Test-Path -LiteralPath $other)-or (Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath $other).Hash){throw "Different version exists at $dest; preserve it before installing"}}}
  $plans+=@{Root=$root;Destination=$dest;Same=$same}
}
foreach($plan in $plans){if($plan.Same){Write-Output "Already identical: $($plan.Destination)"}else{New-Item -ItemType Directory -Force -Path $plan.Root | Out-Null;Copy-Item -LiteralPath $source -Destination $plan.Root -Recurse;Write-Output "Installed: $($plan.Destination)"}}
