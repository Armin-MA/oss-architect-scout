"""Weighted final evaluation score calculation mechanics."""
from __future__ import annotations

from typing import Dict, Mapping, Optional

DEFAULT_WEIGHTS: Dict[str, float] = {
    "architecture": 0.25,
    "cleanliness": 0.25,
    "community": 0.25,
    "popularity": 0.15,
    "hygiene": 0.10,
}


def _normalize_key(key: str) -> str:
    """Normalize score dimension keys by stripping '_score' suffix and lowering case."""
    normalized = key.strip().lower()
    if normalized.endswith("_score"):
        normalized = normalized[:-6]
    return normalized


def calculate_final_score(
    sub_scores: Dict[str, float], weights: Optional[Dict[str, float]] = None
) -> float:
    """Calculate weighted aggregate score from sub-dimension scores.

    Accepts scores for the 5 engineering dimensions (architecture, cleanliness,
    community, popularity, hygiene). Weights can sum to either 1.0 or 100.0.

    Args:
        sub_scores: Dictionary of dimension scores between 0.0 and 100.0.
        weights: Optional dictionary of weights summing to 1.0 or 100.0.
                 Defaults to 25/25/25/15/10 breakdown.

    Returns:
        float final score rounded to 2 decimal places.

    Raises:
        ValueError: If weights do not sum to 1.0 or 100.0, or if inputs are invalid.
    """
    if sub_scores is None or not isinstance(sub_scores, (dict, Mapping)) or not sub_scores:
        raise ValueError("sub_scores must be a non-empty dictionary")

    # Validate and normalize sub_scores
    normalized_sub_scores: Dict[str, float] = {}
    for k, v in sub_scores.items():
        if not isinstance(k, str) or not k.strip():
            raise ValueError("sub_scores keys must be non-empty strings")
        if v is None or not isinstance(v, (int, float)) or isinstance(v, bool):
            raise ValueError(f"Score for '{k}' must be a numeric value, got: {v}")
        f_val = float(v)
        if f_val < 0.0 or f_val > 100.0:
            raise ValueError(f"Score for '{k}' must be between 0.0 and 100.0, got: {v}")
        normalized_sub_scores[_normalize_key(k)] = f_val

    # Validate and normalize weights
    if weights is None:
        active_weights = DEFAULT_WEIGHTS
    else:
        if not isinstance(weights, (dict, Mapping)) or not weights:
            raise ValueError("weights must be a non-empty dictionary when provided")
        active_weights = weights

    normalized_weights: Dict[str, float] = {}
    for k, v in active_weights.items():
        if not isinstance(k, str) or not k.strip():
            raise ValueError("weights keys must be non-empty strings")
        if v is None or not isinstance(v, (int, float)) or isinstance(v, bool):
            raise ValueError(f"Weight for '{k}' must be a numeric value, got: {v}")
        f_val = float(v)
        if f_val < 0.0:
            raise ValueError(f"Weight for '{k}' cannot be negative, got: {v}")
        normalized_weights[_normalize_key(k)] = f_val

    weight_sum = sum(normalized_weights.values())
    if abs(weight_sum - 1.0) < 1e-4:
        scale = 1.0
    elif abs(weight_sum - 100.0) < 1e-2:
        scale = 100.0
    else:
        raise ValueError(
            f"Weights must sum to 1.0 or 100.0, got: {weight_sum}"
        )

    # Compute weighted sum
    total_score = 0.0
    for dim, weight_val in normalized_weights.items():
        norm_weight = weight_val / scale
        dim_score = normalized_sub_scores.get(dim, 0.0)
        total_score += dim_score * norm_weight

    clamped_score = max(0.0, min(100.0, total_score))
    return round(clamped_score, 2)
