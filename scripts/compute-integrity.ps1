Write-Output "Computing SHA256 for STRATEGY.md + PRINCIPLES.md + DEPLOYMENT.md"
$files = @('STRATEGY.md','PRINCIPLES.md','DEPLOYMENT.md')
$combined = "combined.txt"
if (Test-Path $combined) { Remove-Item $combined }
foreach ($f in $files) {
    if (-Not (Test-Path $f)) { Write-Error "$f not found"; exit 2 }
    Get-Content $f | Out-File -FilePath $combined -Append -Encoding utf8
}
$sha = Get-FileHash -Path $combined -Algorithm SHA256
"SHA256(STRATEGY.md + PRINCIPLES.md + DEPLOYMENT.md) = $($sha.Hash)" | Out-File -FilePath VALIDATION/integrity_attestation.txt -Encoding utf8
Write-Output "Wrote VALIDATION/integrity_attestation.txt with hash: $($sha.Hash)"
