"""Community health score calculation mechanics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from src.entities.candidate_repo import CandidateRepo


def calculate_community_score(
    repo: CandidateRepo, reference_date: datetime
) -> float:
    """Compute community health score (0.0 to 100.0) for a candidate repository.

    The score evaluates commit recency and open issue ratio.
    If the repository has not received commits/updates for over 1 year (365 days),
    it is considered abandoned and returns 0.0.

    Args:
        repo: The CandidateRepo entity to evaluate.
        reference_date: The reference baseline datetime to evaluate recency against.

    Returns:
        float score between 0.0 and 100.0 rounded to 2 decimal places.

    Raises:
        ValueError: If repo is not CandidateRepo or reference_date is not datetime.
    """
    if repo is None or not isinstance(repo, CandidateRepo):
        raise ValueError("repo must be an instance of CandidateRepo")
    if reference_date is None or not isinstance(reference_date, datetime):
        raise ValueError("reference_date must be an instance of datetime")

    if not repo.updated_at or not isinstance(repo.updated_at, str):
        return 0.0

    # Parse ISO 8601 updated_at timestamp
    raw_date = repo.updated_at.strip()
    try:
        updated_dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
    except ValueError:
        return 0.0

    # Harmonize timezone awareness between reference_date and updated_dt
    if reference_date.tzinfo is not None and updated_dt.tzinfo is None:
        updated_dt = updated_dt.replace(tzinfo=timezone.utc)
    elif reference_date.tzinfo is None and updated_dt.tzinfo is not None:
        reference_date = reference_date.replace(tzinfo=timezone.utc)

    delta = reference_date - updated_dt
    days_elapsed = delta.total_seconds() / 86400.0

    # Abandoned if older than 365 days
    if days_elapsed > 365.0:
        return 0.0

    if days_elapsed < 0.0:
        days_elapsed = 0.0

    # 1. Recency component (50% max weight)
    recency_factor = max(0.0, 1.0 - (days_elapsed / 365.0))
    recency_score = recency_factor * 50.0

    # 2. Issue health & resolution velocity component (50% max weight)
    engagement = repo.stars + repo.forks
    if engagement == 0:
        if repo.open_issues == 0:
            issue_score = 50.0
        else:
            issue_score = max(0.0, 50.0 - (repo.open_issues * 5.0))
    else:
        issue_ratio = repo.open_issues / max(engagement, 1)
        # Ratio of 0.0 gives 1.0 factor; ratio >= 0.5 gives 0.0 factor
        issue_factor = max(0.0, min(1.0, 1.0 - (issue_ratio * 2.0)))
        issue_score = issue_factor * 50.0

    total_score = recency_score + issue_score
    clamped_score = max(0.0, min(100.0, total_score))
    return round(clamped_score, 2)
