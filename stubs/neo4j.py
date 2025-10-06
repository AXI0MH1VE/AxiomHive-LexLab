"""Lightweight neo4j shim for offline testing.

Provides GraphDatabase.driver(...).session() context manager with a run() method
that simply records queries in-memory. No networking.
"""
class Session:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False
    def run(self, query, **kwargs):
        # Return an iterable of dict-like records; keep simple and empty
        return []

class Driver:
    def __init__(self, uri, auth=None):
        self.uri = uri
    def verify_connectivity(self):
        return True
    def session(self):
        return Session()
    def close(self):
        return None

class GraphDatabase:
    @staticmethod
    def driver(uri, auth=None):
        return Driver(uri, auth=auth)
