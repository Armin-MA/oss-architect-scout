"""Pure Business Mechanics layer for oss-architect-scout.

Conforms strictly to the 'One File, One Logical Action' architectural rule.
Contains deterministic business algorithms with ZERO global state, ZERO network,
and ZERO database dependencies.
"""

from src.mechanics.filter_veto_gate import filter_veto_gate
from src.mechanics.calculate_community_score import calculate_community_score
from src.mechanics.calculate_code_cleanliness_score import calculate_code_cleanliness_score
from src.mechanics.calculate_popularity_score import calculate_popularity_score
from src.mechanics.calculate_malleability_score import calculate_malleability_score
from src.mechanics.calculate_final_score import calculate_final_score
from src.mechanics.detect_project_architecture import detect_project_architecture
from src.mechanics.generate_adapter_scaffold import generate_adapter_scaffold

__all__ = [
    "filter_veto_gate",
    "calculate_community_score",
    "calculate_code_cleanliness_score",
    "calculate_popularity_score",
    "calculate_malleability_score",
    "calculate_final_score",
    "detect_project_architecture",
    "generate_adapter_scaffold",
]
