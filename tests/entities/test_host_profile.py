"""Unit tests for HostProfile domain entity."""

import pytest
from src.entities.host_profile import HostProfile


class TestHostProfile:
    """Test suite for HostProfile."""

    def test_happy_path_instantiation(self) -> None:
        """Verify successful instantiation with valid profile attributes."""
        profile = HostProfile(
            architecture_type="Layered Architecture",
            active_skills=["Architect", "TDD", "Brainstorming"],
            banned_libraries=["requests", "axios", "flask"],
            required_layers=["contracts", "entities", "mechanics", "database", "ui"],
            strict_typing=True,
        )
        assert profile.architecture_type == "Layered Architecture"
        assert profile.active_skills == ["Architect", "TDD", "Brainstorming"]
        assert profile.banned_libraries == ["requests", "axios", "flask"]
        assert profile.required_layers == ["contracts", "entities", "mechanics", "database", "ui"]
        assert profile.strict_typing is True

    def test_defaults_and_boundary_conditions(self) -> None:
        """Verify defaults and edge cases with empty lists and None coercion."""
        profile = HostProfile(architecture_type="Clean Architecture")
        assert profile.architecture_type == "Clean Architecture"
        assert profile.active_skills == []
        assert profile.banned_libraries == []
        assert profile.required_layers == []
        assert profile.strict_typing is True

        profile_none_lists = HostProfile(
            architecture_type="Hexagonal",
            active_skills=None,  # type: ignore
            banned_libraries=None,  # type: ignore
            required_layers=None,  # type: ignore
            strict_typing=False,
        )
        assert profile_none_lists.active_skills == []
        assert profile_none_lists.banned_libraries == []
        assert profile_none_lists.required_layers == []
        assert profile_none_lists.strict_typing is False

    @pytest.mark.parametrize(
        "invalid_arch",
        ["", "   ", None, 12345],
    )
    def test_failure_invalid_architecture_type(self, invalid_arch) -> None:
        """Verify ValueError is raised on invalid architecture_type."""
        with pytest.raises(ValueError, match="architecture_type cannot be empty"):
            HostProfile(architecture_type=invalid_arch)

    def test_failure_invalid_strict_typing(self) -> None:
        """Verify ValueError is raised on non-boolean strict_typing."""
        with pytest.raises(ValueError, match="strict_typing must be a boolean"):
            HostProfile(architecture_type="Microservices", strict_typing="yes")  # type: ignore
