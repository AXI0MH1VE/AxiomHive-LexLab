import pytest
from unittest.mock import MagicMock, patch
from src.memory_trace_manager.memory_graph import MemoryTraceManager

@patch('src.memory_trace_manager.memory_graph.neo4j')
def test_add_memory(mock_neo4j):
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    mock_neo4j.GraphDatabase.driver.return_value = mock_driver

    manager = MemoryTraceManager()
    manager.add_memory("test_concept", {"property": "value"})
    
    mock_session.run.assert_called_once()
    args, kwargs = mock_session.run.call_args
    assert "MERGE (c:Concept {name: $concept})" in args[0]
    assert kwargs['concept'] == 'test_concept'

