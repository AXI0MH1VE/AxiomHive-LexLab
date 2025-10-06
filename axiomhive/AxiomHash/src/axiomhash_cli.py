#!/usr/bin/env python3
"""AxiomHash CLI: streaming SHA-256 and Merkle root stub"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Iterable, List


def iter_chunks(fileobj, size: int = 8192):
    while True:
        data = fileobj.read(size)
        if not data:
            break
        yield data


def sha256_stream(path: Path, chunk_size: int = 8192) -> str:
    h = hashlib.sha256()
    if path == Path('-'):
        f = sys.stdin.buffer
        for c in iter_chunks(f, chunk_size):
            h.update(c)
    else:
        with path.open('rb') as f:
            for c in iter_chunks(f, chunk_size):
                h.update(c)
    return h.hexdigest()


def merkle_root(chunks: Iterable[bytes]) -> str:
    # Simple concatenation tree stub: hash of concatenated chunk hashes
    h = hashlib.sha256()
    for c in chunks:
        h.update(hashlib.sha256(c).digest())
    return h.hexdigest()


def constant_time_compare(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    res = 0
    for x, y in zip(a.encode(), b.encode()):
        res |= x ^ y
    return res == 0


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog='axiomhash')
    p.add_argument('file', nargs='?', default='-')
    p.add_argument('--algorithm', choices=['sha256'], default='sha256')
    p.add_argument('--compare')
    p.add_argument('--merkle', action='store_true')
    p.add_argument('--chunk-size', type=int, default=8192)
    args = p.parse_args(argv)

    path = Path(args.file)
    try:
        digest = sha256_stream(path, args.chunk_size)
    except Exception as e:
        print('ERROR', e, file=sys.stderr)
        return 3

    if args.compare:
        ok = constant_time_compare(digest, args.compare)
        print(digest)
        return 0 if ok else 1

    print(digest)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
#!/usr/bin/env python3
import argparse
import hashlib
import sys
from pathlib import Path
from typing import Iterator


def iter_chunks(path: Path, chunk_size: int) -> Iterator[bytes]:
    if path == Path('-'):
        stream = sys.stdin.buffer
        while True:
            c = stream.read(chunk_size)
            if not c:
                break
            yield c
    else:
        with open(path, 'rb') as fh:
            while True:
                b = fh.read(chunk_size)
                if not b:
                    break
                yield b


def constant_time_compare(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    res = 0
    for x, y in zip(a.encode('utf-8'), b.encode('utf-8')):
        res |= x ^ y
    return res == 0


def merkle_root(chunks: list[bytes]) -> str:
    # Simple concatenation tree as a deterministic stub
    import hashlib

    nodes = [hashlib.sha256(c).digest() for c in chunks]
    while len(nodes) > 1:
        paired = []
        for i in range(0, len(nodes), 2):
            a = nodes[i]
            b = nodes[i+1] if i+1 < len(nodes) else nodes[i]
            paired.append(hashlib.sha256(a + b).digest())
        nodes = paired
    return nodes[0].hex().upper() if nodes else hashlib.sha256(b'').hexdigest().upper()


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('path', nargs='?', default='-')
    p.add_argument('--algorithm', default='sha256', choices=['sha256'])
    p.add_argument('--chunk-size', type=int, default=65536)
    p.add_argument('--merkle', action='store_true')
    p.add_argument('--compare')
    p.add_argument('--verbose', action='store_true')
    args = p.parse_args(argv)

    path = Path(args.path)
    chunks = []
    h = hashlib.sha256()
    try:
        for c in iter_chunks(path, args.chunk_size):
            chunks.append(c)
            h.update(c)
        digest = h.hexdigest().upper()
        if args.verbose:
            print(digest)
        if args.compare:
            ok = constant_time_compare(digest, args.compare.upper())
            return 0 if ok else 1
        if args.merkle:
            print(merkle_root(chunks))
        else:
            print(digest)
        return 0
    except Exception as e:
        print('ERROR', e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
