"""Abstract contract for multi-stage candidate pruning funnel."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

from src.contracts.i_github_client import IGitHubClient

if TYPE_CHECKING:
    from src.entities.candidate_repo import CandidateRepo
    from src.entities.host_profile import HostProfile
else:
    try:
        from src.entities.candidate_repo import CandidateRepo
    except ImportError:
        CandidateRepo = Any  # type: ignore
    try:
        from src.entities.host_profile import HostProfile
    except ImportError:
        HostProfile = Any  # type: ignore


class IPruningFunnel(ABC):
    """Abstract interface declaring 3-stage candidate pruning funnel operations."""

    @abstractmethod
    def prune_stage1_metadata(self, repos: List[CandidateRepo]) -> List[CandidateRepo]:
        """Stage 1: Rapid metadata filtering and hard veto elimination."""
        pass

    @abstractmethod
    def prune_stage2_heuristics(self, repos: List[CandidateRepo], client: IGitHubClient) -> List[CandidateRepo]:
        """Stage 2: Deterministic heuristics, CI inspection, and health pruning."""
        pass

    @abstractmethod
    def prune_stage3_deep(self, repos: List[CandidateRepo], host: HostProfile) -> List[CandidateRepo]:
        """Stage 3: Deep architectural inspection and contract compatibility pruning."""
        pass
