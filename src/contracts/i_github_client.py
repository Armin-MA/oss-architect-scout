"""Abstract contract for GitHub API client."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from src.entities.candidate_repo import CandidateRepo
else:
    try:
        from src.entities.candidate_repo import CandidateRepo
    except ImportError:
        CandidateRepo = Any  # type: ignore


class IGitHubClient(ABC):
    """Abstract interface declaring GitHub REST/GraphQL API operations."""

    @abstractmethod
    def search_repositories(self, query: str, limit: int = 50) -> List[CandidateRepo]:
        """Search repositories matching search query up to limit candidates."""
        pass

    @abstractmethod
    def get_repository_tree(self, full_name: str) -> List[str]:
        """Retrieve full file path tree of a repository."""
        pass

    @abstractmethod
    def get_file_content(self, full_name: str, path: str) -> str:
        """Fetch raw content of a specific file from a repository."""
        pass

    @abstractmethod
    def check_ci_status(self, full_name: str) -> str:
        """Query CI build status for repository (e.g. 'SUCCESS', 'FAILURE', 'UNKNOWN')."""
        pass
