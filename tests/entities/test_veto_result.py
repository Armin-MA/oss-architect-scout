"""Unit tests for VetoResult domain entity."""

from dataclasses import FrozenInstanceError
import pytest
from src.entities.veto_result import VetoResult


class TestVetoResult:
    """Test suite for VetoResult."""

    def test_happy_path_pass(self) -> None:
        """Verify successful instantiation when veto passes."""
        veto = VetoResult(is_passed=True, reason="All checks passed", severity="NONE")
        assert veto.is_passed is True
        assert veto.reason == "All checks passed"
        assert veto.severity == "NONE"

    def test_happy_path_critical_fail(self) -> None:
        """Verify successful instantiation when veto triggers critical fail."""
        veto = VetoResult(
            is_passed=False,
            reason="License GPL-3.0 is viral copyleft and incompatible with commercial host profile",
            severity="CRITICAL",
        )
        assert veto.is_passed is False
        assert "GPL-3.0" in veto.reason
        assert veto.severity == "CRITICAL"

    def test_edge_case_warning_severity(self) -> None:
        """Verify WARNING severity with empty and default reason."""
        veto = VetoResult(is_passed=True, severity="WARNING")
        assert veto.is_passed is True
        assert veto.reason == ""
        assert veto.severity == "WARNING"

    def test_immutability(self) -> None:
        """Verify VetoResult is immutable."""
        veto = VetoResult(is_passed=True)
        with pytest.raises(FrozenInstanceError):
            veto.is_passed = False  # type: ignore

    @pytest.mark.parametrize(
        "invalid_severity",
        ["LOW", "HIGH", "UNKNOWN", "", "critical", None],
    )
    def test_failure_invalid_severity(self, invalid_severity) -> None:
        """Verify ValueError is raised on disallowed severity."""
        with pytest.raises(ValueError, match="severity must be one of"):
            VetoResult(is_passed=False, severity=invalid_severity)  # type: ignore

    @pytest.mark.parametrize(
        "invalid_passed",
        ["true", 1, 0, None, [True]],
    )
    def test_failure_invalid_is_passed_type(self, invalid_passed) -> None:
        """Verify ValueError is raised when is_passed is not a bool."""
        with pytest.raises(ValueError, match="is_passed must be a boolean"):
            VetoResult(is_passed=invalid_passed)  # type: ignore

    def test_failure_invalid_reason_type(self) -> None:
        """Verify ValueError is raised when reason is not a string."""
        with pytest.raises(ValueError, match="reason must be a string"):
            VetoResult(is_passed=True, reason=123)  # type: ignore
