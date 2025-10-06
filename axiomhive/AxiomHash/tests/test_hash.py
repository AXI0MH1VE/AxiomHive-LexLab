import subprocess
import sys
from pathlib import Path


def test_hash_exact(tmp_path):
    f = tmp_path / 'data.txt'
    f.write_bytes(b'hello world')
    p = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / 'src' / 'axiomhash_cli.py'), str(f)], capture_output=True, text=True)
    assert p.returncode == 0
    assert 'B94D27B9934D3E08A52E52D7DA7DABFA' in p.stdout.upper()


def test_compare_mismatch(tmp_path):
    f = tmp_path / 'data.txt'
    f.write_bytes(b'foo')
    p = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / 'src' / 'axiomhash_cli.py'), str(f), '--compare', '0'*64], capture_output=True, text=True)
    assert p.returncode == 1
