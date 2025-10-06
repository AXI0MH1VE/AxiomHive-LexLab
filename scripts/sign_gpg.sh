#!/usr/bin/env bash
set -euo pipefail
if [ -z "${GPG_SIGNER:-}" ]; then
  echo "Set GPG_SIGNER environment variable to your key id or email"
  exit 2
fi
FILE=${1:-axiom-v1.0.zip}
gpg --default-key "$GPG_SIGNER" --output "$FILE".sig --detach-sign "$FILE"
echo "Signed $FILE -> $FILE.sig"
