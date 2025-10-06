#!/usr/bin/env bash
set -euo pipefail
OUT=axiom-v1.0.zip
rm -f "$OUT"
# Include the frontend dist if present
if [ -d "frontend/dist" ]; then
	zip -r "$OUT" STRATEGY.md PRINCIPLES.md DEPLOYMENT.md legend_manifest.json supremacy_kernel.py README.md frontend/dist
else
	zip -r "$OUT" STRATEGY.md PRINCIPLES.md DEPLOYMENT.md legend_manifest.json supremacy_kernel.py README.md
fi
echo "Wrote $OUT"
