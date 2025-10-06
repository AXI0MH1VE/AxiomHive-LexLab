"""
Compression: Zlib lossless for models.
"""

import zlib
import io
import torch

def compress_model(state_dict: Dict[str, torch.Tensor]) -> bytes:
    buffer = io.BytesIO()
    torch.save(state_dict, buffer)
    data = buffer.getvalue()
    return zlib.compress(data)

def decompress_model(compressed_bytes: bytes) -> Dict[str, torch.Tensor]:
    data = zlib.decompress(compressed_bytes)
    buffer = io.BytesIO(data)
    return torch.load(buffer)