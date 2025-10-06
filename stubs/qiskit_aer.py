"""Very small Aer simulator shim used by tests to execute QuantumCircuit objects."""
class AerSimulator:
    def run(self, circuit):
        # produce deterministic fake results: if circuit contains a CX, return entangled counts
        gates = getattr(circuit, 'gates', [])
        if any(g[0] == 'cx' for g in gates):
            return {'00': 0.5, '11': 0.5}
        return {'00': 1.0}
