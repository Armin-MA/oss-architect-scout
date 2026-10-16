"""Abstract contract for scout persistence repository."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from src.entities.evaluation_score import EvaluationScore
    from src.database.dto.evaluation_record_dto import EvaluationRecordDTO
else:
    EvaluationScore = Any  # type: ignore
    EvaluationRecordDTO = Any  # type: ignore



class IScoutRepository(ABC):
    """Abstract interface declaring persistence operations for evaluation runs and history."""

    @abstractmethod
    def save_evaluation_run(self, run: Any) -> str:
        """Persist evaluation run and return the generated run_id string."""
        pass

    @abstractmethod
    def get_evaluation_history(self, limit: int = 10) -> List[EvaluationRecordDTO]:
        """Retrieve past evaluation records from database."""
        pass
