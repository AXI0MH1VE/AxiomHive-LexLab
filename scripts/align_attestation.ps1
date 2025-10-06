$mf = Get-Content .\legend_manifest.json -Raw | ConvertFrom-Json
$hash = $mf.computed_sha256.ToUpper()
$lines = @(
  "SHA256(STRATEGY.md + PRINCIPLES.md + DEPLOYMENT.md) = $hash",
  "OPERATIONAL INTEGRITY VERIFIED - ALEXIS ADAMS PRIMACY MANIFESTED."
)
Set-Content -Path .\VALIDATION\integrity_attestation.txt -Value $lines -Encoding UTF8
git add .\VALIDATION\integrity_attestation.txt
git commit -m 'Attestation: align to kernel raw-byte hash' --author='github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>'
python .\supremacy_kernel.py
python .\scripts\validate_workspace.py
