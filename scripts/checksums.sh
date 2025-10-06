#!/usr/bin/env bash
set -euo pipefail
FILE=${1:-axiom-v1.0.zip}
sha256sum "$FILE" | awk '{print $1}' > "$FILE".sha256
sha512sum "$FILE" | awk '{print $1}' > "$FILE".sha512
echo "Wrote $FILE.sha256 and $FILE.sha512"
