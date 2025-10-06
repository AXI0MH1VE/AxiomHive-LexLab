#!/usr/bin/env python3
"""Supremacy Kernel

Loads STRATEGY.md, PRINCIPLES.md, DEPLOYMENT.md, validates SHA256 against
VALIDATION/integrity_attestation.txt, and writes legend_manifest.json.

Constraints: Python 3.10+, standard library only.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parent


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    # strip common fenced code block markers if present (``` or ~~~)
    # remove any leading or trailing fence blocks and normalize newlines
    text = re.sub(r"^(```|~~~)[^\n]*\n", "", text)
    text = re.sub(r"\n(```|~~~)\s*$", "", text)
    # normalize line endings and trim
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = '\n'.join([ln.rstrip() for ln in text.split('\n')]).strip() + '\n'
    return text


def compute_combined_sha256(paths: List[Path]) -> str:
    h = hashlib.sha256()
    for p in paths:
        data = p.read_bytes() if p.exists() else b""
        h.update(data)
    return h.hexdigest().upper()


def parse_supremacy_vector(strategy_text: str) -> str:
    # Find the first non-empty, non-separator line as title
    for line in strategy_text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("---"):
            continue
        if s.startswith("#"):
            return s.lstrip('#').strip()
        # ignore fenced ticks
        if s.startswith('```'):
            continue
        return s
    return "Apex Strategy"


def parse_principles(principles_text: str) -> List[str]:
    # Normalize text and split into lines
    text = principles_text
    lines = [ln for ln in (text or '').splitlines()]

    # Find the markdown table header
    header_idx = None
    for i, ln in enumerate(lines):
        # detect a markdown table header where first column is 'Principle'
        if re.match(r"^\|\s*Principle\s*\|", ln, flags=re.IGNORECASE):
            header_idx = i
            break

    directives: List[dict] = []
    if header_idx is not None:
        # parse subsequent rows until a blank line or non-table line
        for ln in lines[header_idx + 1:]:
            if not ln.strip():
                break
            if '|' not in ln:
                break
            parts = [p.strip() for p in ln.split('|')]
            # parts may have empty first/last due to leading/trailing '|'
            # ensure at least two meaningful columns
            meaningful = [p for p in parts if p != '']
            if len(meaningful) < 2:
                continue
            # The first meaningful token is principle, second is description
            principle = meaningful[0]
            description = meaningful[1]
            # skip separator-like rows (---)
            if re.match(r'^-+$', principle.replace(' ', '')):
                continue
            directives.append({"principle": principle, "description": description})

    # fallback: if no directives parsed from table, attempt to extract bullets
    if not directives:
        for ln in lines:
            s = ln.strip()
            if s.startswith(('-', '*')):
                s = s.lstrip('-* ').strip()
                # try to split into principle and description by ' - ' or ':'
                if ' - ' in s:
                    a, b = s.split(' - ', 1)
                    directives.append({"principle": a.strip(), "description": b.strip()})
                elif ':' in s:
                    a, b = s.split(':', 1)
                    directives.append({"principle": a.strip(), "description": b.strip()})
                else:
                    directives.append({"principle": s, "description": ""})

    # Return principles as list of dicts
    return directives


def read_attestation(path: Path) -> str | None:
    if not path.exists():
        return None
    txt = path.read_text(encoding="utf-8")
    # find a 64-hex char sequence
    m = re.search(r'([A-Fa-f0-9]{64})', txt)
    return m.group(1).upper() if m else None


def main() -> None:
    strategy_p = ROOT / "STRATEGY.md"
    principles_p = ROOT / "PRINCIPLES.md"
    deployment_p = ROOT / "DEPLOYMENT.md"
    attestation_p = ROOT / "VALIDATION" / "integrity_attestation.txt"

    # Read texts
    strategy_text = read_text(strategy_p)
    principles_text = read_text(principles_p)
    deployment_text = read_text(deployment_p)

    # Compute combined SHA256
    computed = compute_combined_sha256([strategy_p, principles_p, deployment_p])

    # Read attestation expected value (if present)
    expected = read_attestation(attestation_p)

    verified = (expected is not None and computed == expected)

    # Parse manifest fields
    supremacy_vector = parse_supremacy_vector(strategy_text)
    directives = parse_principles(principles_text)

    # Execution stack: known artifact directories (relative paths)
    execution_stack = [
        "axiomhive-core/",
        "AxiomSSI/",
        "athena-engine/",
        "gemini-portable/",
        "temporal-gated-attn/",
        "tesseract/",
        "axiom-library/",
        "supremacy-protocol/",
        "recruitment-whitepaper/",
        "downloads/",
        "runtime-zero/",
    ]

    manifest = {
        "operator": "Alexis Adams",
        "supremacy_vector": supremacy_vector,
        "directives": directives,
        "execution_stack": execution_stack,
        "verified": bool(verified),
        "computed_sha256": computed,
        "expected_sha256": expected,
    }

    out_path = ROOT / "legend_manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Supremacy Kernel Initialized :: Operator Confirmed")
    if verified:
        print("Integrity: VERIFIED")
    else:
        print("Integrity: MISMATCH (computed vs attestation)")


if __name__ == '__main__':
    main()
