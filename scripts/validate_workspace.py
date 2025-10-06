#!/usr/bin/env python3
"""Workspace validation helper.

Checks:
- compile all Python files
- run supremacy_kernel.py
- validate JSON files
- compute combined SHA256 and compare with attestation
"""
from __future__ import annotations

import compileall
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def compile_check() -> bool:
    print('Running compileall...')
    ok = compileall.compile_dir(str(ROOT), quiet=1)
    print('compileall OK' if ok else 'compileall FAIL')
    return ok


def run_kernel() -> int:
    print('Running supremacy_kernel.py...')
    p = subprocess.run([sys.executable, str(ROOT / 'supremacy_kernel.py')])
    print('kernel exit code', p.returncode)
    return p.returncode


def validate_json(path: Path) -> bool:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            json.load(fh)
        print(f"{path.name}: JSON OK")
        return True
    except Exception as e:
        print(f"{path.name}: JSON ERR - {e}")
        return False


def compute_combined_hash(files: list[Path]) -> str:
    import hashlib

    h = hashlib.sha256()
    for p in files:
        h.update(p.read_bytes())
    return h.hexdigest().upper()


def read_attestation(path: Path) -> str | None:
    if not path.exists():
        return None
    txt = path.read_text(encoding='utf-8')
    import re
    m = re.search(r'([A-Fa-f0-9]{64})', txt)
    return m.group(1).upper() if m else None


def main() -> None:
    ok = True
    if not compile_check():
        ok = False

    rc = run_kernel()
    if rc != 0:
        ok = False

    manifest = ROOT / 'legend_manifest.json'
    payload = ROOT / 'logs' / 'athena-outreach' / 'recruitment_payload.json'
    attestation = ROOT / 'VALIDATION' / 'integrity_attestation.txt'

    ok &= validate_json(manifest)
    ok &= validate_json(payload)

    files = [ROOT / 'STRATEGY.md', ROOT / 'PRINCIPLES.md', ROOT / 'DEPLOYMENT.md']
    computed = compute_combined_hash(files)
    expected = read_attestation(attestation)
    print('computed:', computed)
    print('expected:', expected)
    if expected is None:
        print('Attestation missing or unreadable')
        ok = False
    elif computed != expected:
        print('Hash mismatch: workspace not attested')
        ok = False
    else:
        print('Attestation matches computed hash')

    print('VALIDATION SUMMARY:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 2)


if __name__ == '__main__':
    main()
