"""Hard veto gate evaluation mechanics for candidate repositories."""
from __future__ import annotations

from typing import Optional
from src.entities.candidate_repo import CandidateRepo
from src.entities.veto_result import VetoResult
from src.utils.license_classifier import classify_license


def filter_veto_gate(repo: CandidateRepo, allow_copyleft: bool = False) -> VetoResult:
    """Evaluate candidate repository against hard veto constraints.

    Checks repository license against viral copyleft, commercial restriction,
    or unknown/missing license policies.

    Args:
        repo: The CandidateRepo entity to evaluate.
        allow_copyleft: If True, copyleft licenses are permitted (with WARNING).
                        If False, copyleft licenses are vetoed (CRITICAL).

    Returns:
        VetoResult indicating whether the candidate passed or was vetoed, with reason.

    Raises:
        ValueError: If input repo or allow_copyleft has invalid types.
    """
    if repo is None or not isinstance(repo, CandidateRepo):
        raise ValueError("repo must be an instance of CandidateRepo")
    if not isinstance(allow_copyleft, bool):
        raise ValueError("allow_copyleft must be a boolean")

    if not repo.license_spdx:
        return VetoResult(
            is_passed=False,
            reason="Repository has missing or unidentified license (all rights reserved)",
            severity="CRITICAL",
        )

    category = classify_license(repo.license_spdx)

    if category == "PERMISSIVE":
        return VetoResult(
            is_passed=True,
            reason=f"Permissive license '{repo.license_spdx}' is fully compatible",
            severity="NONE",
        )

    if category == "COPYLEFT_VIRAL":
        if allow_copyleft:
            return VetoResult(
                is_passed=True,
                reason=f"Copyleft license '{repo.license_spdx}' accepted by user override",
                severity="WARNING",
            )
        return VetoResult(
            is_passed=False,
            reason=f"Viral copyleft license '{repo.license_spdx}' is incompatible with standard commercial policy",
            severity="CRITICAL",
        )

    if category == "COMMERCIAL_RESTRICTED":
        return VetoResult(
            is_passed=False,
            reason=f"Commercial restricted / source-available license '{repo.license_spdx}' is rejected",
            severity="CRITICAL",
        )

    # UNKNOWN or unmapped
    return VetoResult(
        is_passed=False,
        reason=f"Unrecognized or unmapped license '{repo.license_spdx}' is rejected",
        severity="CRITICAL",
    )
