"""Abstract contract for UI presenter."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from src.entities.evaluation_score import EvaluationScore
    from src.entities.candidate_repo import CandidateRepo
else:
    try:
        from src.entities.evaluation_score import EvaluationScore
    except ImportError:
        EvaluationScore = Any  # type: ignore
    try:
        from src.entities.candidate_repo import CandidateRepo
    except ImportError:
        CandidateRepo = Any  # type: ignore


class IUIPresenter(ABC):
    """Abstract interface declaring visual presentation operations."""

    @abstractmethod
    def render_evaluation_report(self, scores: List[EvaluationScore]) -> str:
        """Render formatted markdown evaluation report from evaluation scores."""
        pass

    @abstractmethod
    def render_risk_confirmation(self, repo: CandidateRepo, risks: List[str]) -> str:
        """Render risk confirmation dialog/text for high-threshold risk gates."""
        pass
