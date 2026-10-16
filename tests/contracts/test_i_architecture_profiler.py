"""Unit tests for src/contracts/i_architecture_profiler.py."""
import pytest
from typing import Any
from src.contracts.i_architecture_profiler import IArchitectureProfiler


class DummyArchitectureProfiler(IArchitectureProfiler):
    """Concrete implementation of IArchitectureProfiler for testing."""

    def profile_host(self, project_path: str) -> Any:
        if not project_path:
            return None
        return {
            "project_path": project_path,
            "architecture_type": "layered",
            "required_layers": ["contracts", "mechanics", "database"],
        }


class IncompleteArchitectureProfiler(IArchitectureProfiler):
    """Subclass that does not implement abstract profile_host."""
    pass


def test_i_architecture_profiler_happy_path():
    """Verify concrete subclass successfully implements profile_host."""
    profiler = DummyArchitectureProfiler()
    assert isinstance(profiler, IArchitectureProfiler)

    profile = profiler.profile_host("/path/to/project")
    assert profile is not None
    assert profile["architecture_type"] == "layered"


def test_i_architecture_profiler_edge_cases():
    """Verify boundary handling for empty path."""
    profiler = DummyArchitectureProfiler()
    assert profiler.profile_host("") is None


def test_i_architecture_profiler_failure_states():
    """Verify abstract class cannot be instantiated directly or without implementation."""
    with pytest.raises(TypeError):
        IArchitectureProfiler()  # type: ignore

    with pytest.raises(TypeError):
        IncompleteArchitectureProfiler()  # type: ignore
