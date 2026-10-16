"""VetoResult domain entity representing hard veto gate status."""

from dataclasses import dataclass
from typing import Tuple

ALLOWED_SEVERITIES: Tuple[str, ...] = ("NONE", "WARNING", "CRITICAL")


@dataclass(frozen=True)
class VetoResult:
    """Domain entity representing the evaluation outcome of the Hard Veto Gate."""

    is_passed: bool
    reason: str = ""
    severity: str = "NONE"

    def __post_init__(self) -> None:
        if not isinstance(self.is_passed, bool):
            raise ValueError("is_passed must be a boolean")
        if not isinstance(self.severity, str) or self.severity not in ALLOWED_SEVERITIES:
            raise ValueError(
                f"severity must be one of {ALLOWED_SEVERITIES}, got '{self.severity}'"
            )
        if not isinstance(self.reason, str):
            raise ValueError("reason must be a string")
