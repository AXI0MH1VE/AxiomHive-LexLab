"""
Pytest: Sanctity + Hybrid.
"""

import pytest
import torch
from axiom_hive.dag import AxiomDAG
from axiom_hive.shard import AIShard
from axiom_hive.sanctity import SanctityProtocol, LexHumanaCorpus
from axiom_hive.formal_proof import ProofVerifier

def test_lhc_validate():
    lhc = LexHumanaCorpus()
    valid_out = [torch.tensor([0.5]), torch.tensor([1.0])]
    invalid_out = [torch.tensor([-0.5])]
    assert lhc.validate(valid_out)
    assert not lhc.validate(invalid_out)

def test_hybrid_proof():
    verifier = ProofVerifier()
    mock_config = {
        'sympy_proofs': {'bounded_reality': 'And(Abs(x) <= 1)'},
        'z3_proofs': {'bounded_reality': 'And(Abs(x) <= 1, Not(Abs(x) > 1))'}
    }
    verifier.load_proofs(mock_config)
    assert verifier.verify('bounded_reality')

def test_governor_valid():
    protocol = SanctityProtocol()
    dag = AxiomDAG()
    shard = AIShard(input_dim=10, output_dim=1)
    dag.add_shard("test", func=lambda: shard(torch.rand(1,10)))
    blueprint = protocol.sanctify(dag)
    assert blueprint['status'] == "SANCTIFIED"
    assert 'proofs' in blueprint

def test_null_path():
    class InvalidShard(AIShard):
        def forward(self, x):
            return torch.tensor([-2.0])  # Violates

    protocol = SanctityProtocol()
    dag = AxiomDAG()
    invalid_shard = InvalidShard()
    dag.add_shard("invalid", func=lambda: invalid_shard(torch.rand(1,10)))
    with pytest.raises(ValueError, match="NULL_PATH"):
        protocol.sanctify(dag)