"""
AxiomHive: Sovereign Ascent Protocol
Architect: Alexis Adams
"""

__version__ = "0.3.0"
from .dag import AxiomDAG
from .shard import AIShard
from .compression import compress_model, decompress_model
from .benchmark import run_benchmarks
from .sanctity import SanctityProtocol, LexHumanaCorpus
from .formal_proof import ProofVerifier

__all__ = ["AxiomDAG", "AIShard", "compress_model", "decompress_model", "run_benchmarks", "SanctityProtocol", "LexHumanaCorpus", "ProofVerifier"]