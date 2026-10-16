"""Popularity and community adoption score calculation mechanics."""
from __future__ import annotations

import math


def calculate_popularity_score(stars: int, forks: int) -> float:
    """Compute normalized popularity score (0.0 to 100.0) using logarithmic scaling.

    Stars contribute 70% and forks contribute 30% to the popularity score.
    Zero stars yields a minimum score of 0.0.

    Args:
        stars: Non-negative integer count of repository stars.
        forks: Non-negative integer count of repository forks.

    Returns:
        float score between 0.0 and 100.0 rounded to 2 decimal places.

    Raises:
        ValueError: If stars or forks are negative or not integers.
    """
    if not isinstance(stars, int) or isinstance(stars, bool):
        raise ValueError("stars must be a non-negative integer")
    if not isinstance(forks, int) or isinstance(forks, bool):
        raise ValueError("forks must be a non-negative integer")

    if stars < 0:
        raise ValueError("stars cannot be negative")
    if forks < 0:
        raise ValueError("forks cannot be negative")

    if stars == 0:
        return 0.0

    # Logarithmic scaling: 100,000 stars = 100.0 points (log10 = 5.0)
    star_score = min(100.0, (math.log10(stars) / 5.0) * 100.0)

    # Logarithmic scaling: 10,000 forks = 100.0 points (log10 = 4.0)
    if forks == 0:
        fork_score = 0.0
    else:
        fork_score = min(100.0, (math.log10(forks) / 4.0) * 100.0)

    total_score = (0.70 * star_score) + (0.30 * fork_score)
    clamped_score = max(0.0, min(100.0, total_score))
    return round(clamped_score, 2)
