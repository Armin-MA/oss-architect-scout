"""EvaluationRecordDTO dataclass crossing repository boundaries."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Union


@dataclass(frozen=True)
class EvaluationRecordDTO:
    """Data transfer object representing a persisted candidate evaluation record.

    Encapsulates evaluation run records across repository boundary without
    leaking database drivers or raw database rows.
    """

    run_id: str
    repo_full_name: str
    stars: int
    license_type: str
    final_score: float
    created_at: Optional[Union[datetime, str]] = None

    def __post_init__(self) -> None:
        """Validate input attributes on instantiation."""
        if not self.run_id or not isinstance(self.run_id, str):
            raise ValueError("run_id must be a non-empty string")
        if not self.repo_full_name or not isinstance(self.repo_full_name, str):
            raise ValueError("repo_full_name must be a non-empty string")
        if not isinstance(self.stars, int) or self.stars < 0:
            raise ValueError("stars must be a non-negative integer")
        if not isinstance(self.license_type, str):
            raise ValueError("license_type must be a string")
        if not isinstance(self.final_score, (int, float)):
            raise ValueError("final_score must be a numeric value")
        if not (0.0 <= float(self.final_score) <= 100.0):
            raise ValueError("final_score must be between 0.0 and 100.0")

    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to serializable dictionary."""
        created_str = (
            self.created_at.isoformat()
            if isinstance(self.created_at, datetime)
            else self.created_at
        )
        return {
            "run_id": self.run_id,
            "repo_full_name": self.repo_full_name,
            "stars": self.stars,
            "license_type": self.license_type,
            "final_score": float(self.final_score),
            "created_at": created_str,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvaluationRecordDTO":
        """Construct DTO instance from dictionary data."""
        return cls(
            run_id=data["run_id"],
            repo_full_name=data["repo_full_name"],
            stars=int(data["stars"]),
            license_type=str(data.get("license_type", "Unknown")),
            final_score=float(data["final_score"]),
            created_at=data.get("created_at"),
        )
