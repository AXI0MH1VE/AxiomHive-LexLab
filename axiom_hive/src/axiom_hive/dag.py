"""
AxiomDAG: NetworkX-based topological execution.
"""

import networkx as nx
from typing import Dict, Any, List, Callable

class AxiomDAG:
    """
    DAG for executing AI shards in topological order.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, Callable] = {}

    def add_shard(self, name: str, func: Callable, dependencies: List[str] = None):
        if dependencies is None:
            dependencies = []
        self.nodes[name] = func
        self.graph.add_node(name)
        for dep in dependencies:
            self.graph.add_edge(dep, name)

    def execute(self) -> Dict[str, Any]:
        results = {}
        for node in nx.topological_sort(self.graph):
            if node in self.nodes:
                deps = {dep: results[dep] for dep in self.graph.predecessors(node)}
                if deps:
                    # Assume func takes deps as *args in order
                    args = [results[dep] for dep in sorted(deps.keys())]  # sorted for consistency
                    results[node] = self.nodes[node](*args)
                else:
                    results[node] = self.nodes[node]()
        return results