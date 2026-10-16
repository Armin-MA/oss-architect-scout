"""Abstract contract for candidate scoring engine."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.entities.candidate_repo import CandidateRepo
    from src.entities.host_profile import HostProfile
    from src.entities.evaluation_score import EvaluationScore
else:
    try:
        from src.entities.candidate_repo import CandidateRepo
    except ImportError:
        CandidateRepo = Any  # type: ignore
    try:
        from src.entities.host_profile import HostProfile
    except ImportError:
        HostProfile = Any  # type: ignore
    try:
        from src.entities.evaluation_score import EvaluationScore
    except ImportError:
        EvaluationScore = Any  # type: ignore


class IScoringEngine(ABC):
    """Abstract interface declaring candidate evaluation across 5 dimensions."""

    @abstractmethod
    def score_candidate(self, repo: CandidateRepo, host: HostProfile) -> EvaluationScore:
        """Evaluate a candidate repository against host profile and compute EvaluationScore."""
        pass
