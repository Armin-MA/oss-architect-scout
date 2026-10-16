"""EvaluationScore domain entity representing comprehensive evaluation metrics of a candidate repo."""

from dataclasses import dataclass, field
from typing import List, Optional
from src.entities.candidate_repo import CandidateRepo


@dataclass
class EvaluationScore:
    """Domain entity holding candidate repository multi-dimensional evaluation results."""

    repo: CandidateRepo
    architecture_score: float
    cleanliness_score: float
    community_score: float
    popularity_score: float
    hygiene_score: float
    final_score: float
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    vibe_analogy: str = ""

    def __post_init__(self) -> None:
        if self.repo is None or not isinstance(self.repo, CandidateRepo):
            raise ValueError("repo must be an instance of CandidateRepo")

        sub_scores = {
            "architecture_score": self.architecture_score,
            "cleanliness_score": self.cleanliness_score,
            "community_score": self.community_score,
            "popularity_score": self.popularity_score,
            "hygiene_score": self.hygiene_score,
            "final_score": self.final_score,
        }

        for score_name, score_val in sub_scores.items():
            if score_val is None or not isinstance(score_val, (int, float)) or isinstance(score_val, bool):
                raise ValueError(f"{score_name} must be a numeric value between 0.0 and 100.0")
            float_val = float(score_val)
            if float_val < 0.0 or float_val > 100.0:
                raise ValueError(f"{score_name} must be between 0.0 and 100.0, got {score_val}")

        if self.strengths is None:
            self.strengths = []
        if self.weaknesses is None:
            self.weaknesses = []
        if self.vibe_analogy is None:
            self.vibe_analogy = ""
