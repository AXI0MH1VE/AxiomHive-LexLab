#!/usr/bin/env python3
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = [ROOT / 'STRATEGY.md', ROOT / 'PRINCIPLES.md', ROOT / 'DEPLOYMENT.md']
h = hashlib.sha256()
for f in files:
    h.update(f.read_bytes())
print(h.hexdigest().upper())
