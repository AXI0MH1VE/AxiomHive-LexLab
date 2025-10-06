"""Run lightweight smoke tests for core modules without requiring pytest or heavy packages.
This script prepends the local `stubs` directory to sys.path so imports resolve to our offline stubs.
"""
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUBS = str(ROOT / 'stubs')
if STUBS not in sys.path:
    sys.path.insert(0, STUBS)
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)

RESULTS = []

def run(name, fn):
    try:
        fn()
        print(f"PASS: {name}")
        RESULTS.append((name, True, ''))
    except Exception as e:
        tb = traceback.format_exc()
        print(f"FAIL: {name}\n{tb}")
        RESULTS.append((name, False, tb))

def test_reasoning():
    from src.reasoning_body.logic_engine import ReasoningBody
    engine = ReasoningBody()
    r = engine.analyze("If A then B. A is true, therefore B.")
    assert 'type' in r

def test_emotional():
    from src.emotional_analyzer.emotion_processor import EmotionalAnalyzer
    ea = EmotionalAnalyzer()
    r = ea.analyze("I am very happy today")
    assert 'emotion' in r

def test_memory():
    from src.memory_trace_manager.memory_graph import MemoryTraceManager
    m = MemoryTraceManager()
    m.add_memory('x', {'a':1})

def test_pattern_detector():
    from src.abstract_pattern_detector.pattern_finder import AbstractPatternDetector
    import torch as _torch
    det = AbstractPatternDetector(input_dim=4, latent_dim=2)
    t = _torch.rand(1,4)
    r = det.detect(t)
    assert 'reconstruction_error' in r

def test_harmonizer():
    from src.entropy_matrix_harmonizer.coherence_engine import EntropyMatrixHarmonizer
    h = EntropyMatrixHarmonizer()
    out = h.synthesize({'type':'Inductive Reasoning','observation':'x','confidence':0.5},{'emotion':'NEUTRAL','intensity':0.4})
    assert isinstance(out, str)

def test_ethics():
    from src.ethics_sentinel.ethical_guard import EthicsSentinel
    s = EthicsSentinel()
    assert s.validate_request('hello')
    assert not s.validate_request('how to harm')

def test_safety():
    from src.safety_guardian.ooda_loop import SafetyGuardianLayer
    g = SafetyGuardianLayer(requests_per_second=100)
    assert g.check_safety()

def test_marketplace():
    from src.monetization.marketplace import DigitalMarketplace
    m = DigitalMarketplace()
    m.post_task('t','d',1.0)
    m.place_bid('t','a',2.0)
    w = m.close_auction('t')
    assert w['agent_id']=='a'

def test_quantum():
    from src.shard_network.quantum_refractor import QuantumRefractor
    q = QuantumRefractor(num_qubits=2)
    qc = q.create_entangled_state()
    res = q.execute_circuit(qc)
    assert '00' in res and '11' in res

def main():
    tests = [
        ('reasoning', test_reasoning),
        ('emotional', test_emotional),
        ('memory', test_memory),
        ('pattern_detector', test_pattern_detector),
        ('harmonizer', test_harmonizer),
        ('ethics', test_ethics),
        ('safety', test_safety),
        ('marketplace', test_marketplace),
        ('quantum', test_quantum),
    ]

    for name, fn in tests:
        run(name, fn)

    failed = [r for r in RESULTS if not r[1]]
    print('\nSummary:')
    print(f'Total: {len(RESULTS)}, Passed: {len(RESULTS)-len(failed)}, Failed: {len(failed)}')
    if failed:
        sys.exit(2)
    sys.exit(0)

if __name__ == '__main__':
    main()
