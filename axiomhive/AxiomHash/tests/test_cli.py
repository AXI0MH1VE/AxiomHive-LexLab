import subprocess
import sys
from pathlib import Path
import hashlib


def run_cli(script_path: Path, args, input_bytes: bytes | None = None):
    cmd = [sys.executable, str(script_path)] + list(args)
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE if input_bytes is not None else None,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate(input=input_bytes)
    return p.returncode, out.decode().strip(), err.decode()


def test_sha256_stdin(tmp_path):
    data = b'hello world\n'
    script_path = Path(__file__).resolve().parents[1] / 'src' / 'axiomhash_cli.py'
    rc, out, err = run_cli(script_path, [], input_bytes=data)
    assert rc == 0
    expected = hashlib.sha256(data).hexdigest()
    assert out == expected
