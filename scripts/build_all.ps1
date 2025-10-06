<#
Build everything: backend deps, frontend build (Vite), compute attestation, and package release ZIP.

Usage (PowerShell, repo root):
    .\scripts\build_all.ps1

Notes:
- This script will call npm for frontend build; ensure Node.js/npm is installed if you want to build the frontend.
- The script is conservative: it will skip frontend build if npm isn't available and still package textual artifacts.
#>

Set-StrictMode -Version Latest
Set-Location -Path (Join-Path $PSScriptRoot '..')

Write-Host "1) Install backend requirements"
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt

Write-Host "2) Build frontend (if npm available)"
$node = Get-Command npm -ErrorAction SilentlyContinue
if ($node) {
    Push-Location frontend
    Write-Host "Running npm install..."
    try {
        npm install
        Write-Host "Running npm run build..."
        npm run build
    } catch {
        Write-Warning "npm install or npm run build failed. Frontend build will be skipped. Ensure Node.js/npm are installed and try running 'cd frontend; npm install; npm run build' manually."
    }
    Pop-Location
} else {
    Write-Host "npm not found; skipping frontend build. If you want the frontend included, install Node.js and rerun this script." -ForegroundColor Yellow
}

Write-Host "3) Compute attestation"
python .\scripts\compute_attestation.py > .\VALIDATION\integrity_attestation.txt

Write-Host "4) Package release ZIP (Windows packaging)"
try {
    $out = Join-Path $PSScriptRoot '..\axiom-v1.0.zip'
    if (Test-Path $out) { Remove-Item $out -Force }
    $items = @('STRATEGY.md','PRINCIPLES.md','DEPLOYMENT.md','legend_manifest.json','supremacy_kernel.py','README.md')
    $frontendDist = Join-Path $PSScriptRoot '..\frontend\dist'
    if (Test-Path $frontendDist) {
        $items += $frontendDist
    } else {
        Write-Host "frontend/dist not found; frontend will not be packaged." -ForegroundColor Yellow
    }
    Write-Host "Creating $out with: $($items -join ', ')"
    Compress-Archive -Path $items -DestinationPath $out -Force
    Write-Host "Wrote $out"
} catch {
    Write-Warning "Packaging via Compress-Archive failed: $_. Exception. Attempting to call package_zip.sh if bash exists."
    if (Get-Command bash -ErrorAction SilentlyContinue) {
        bash -c "./scripts/package_zip.sh"
    } else {
        Write-Warning "No bash available; packaging may have failed."
    }
}

Write-Host "Build script finished. Check axiom-v1.0.zip in repo root (if packaging succeeded)."