"""Minimal qiskit shim for tests. Provides QuantumCircuit with basic gates."""
class QuantumCircuit:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.gates = []
    def h(self, qubit):
        self.gates.append(('h', qubit))
    def cx(self, q1, q2):
        self.gates.append(('cx', q1, q2))
    def __repr__(self):
        return f"QuantumCircuit({self.num_qubits}, gates={self.gates})"
