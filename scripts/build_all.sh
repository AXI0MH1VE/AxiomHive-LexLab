#!/usr/bin/env bash
set -euo pipefail

# Build backend deps and frontend (if node present), compute attestation and package
ROOT=$(cd "$(dirname "$0")/.." && pwd)
echo "ROOT=$ROOT"

echo "1) Install backend requirements"
python -m pip install --upgrade pip
python -m pip install -r "$ROOT/backend/requirements.txt"

if command -v npm >/dev/null 2>&1; then
  echo "2) Build frontend"
  (cd "$ROOT/frontend" && npm install && npm run build)
else
  echo "npm not found; skipping frontend build"
fi

echo "3) Compute attestation"
python "$ROOT/scripts/compute_attestation.py" > "$ROOT/VALIDATION/integrity_attestation.txt"

echo "4) Package release zip"
"$ROOT/scripts/package_zip.sh"

echo "Build complete"
