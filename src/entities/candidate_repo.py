"""CandidateRepo domain entity representing an open-source repository candidate."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CandidateRepo:
    """Immutable domain entity holding candidate repository attributes."""

    name: str
    full_name: str
    stars: int = 0
    forks: int = 0
    license_spdx: Optional[str] = None
    open_issues: int = 0
    default_branch: str = "main"
    updated_at: str = ""
    description: Optional[str] = ""

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Repository name cannot be empty")
        if not isinstance(self.full_name, str) or not self.full_name.strip():
            raise ValueError("Repository full_name cannot be empty")
        if not isinstance(self.stars, int) or self.stars < 0:
            raise ValueError("stars cannot be negative")
        if not isinstance(self.forks, int) or self.forks < 0:
            raise ValueError("forks cannot be negative")
        if not isinstance(self.open_issues, int) or self.open_issues < 0:
            raise ValueError("open_issues cannot be negative")
        if not isinstance(self.default_branch, str) or not self.default_branch.strip():
            raise ValueError("default_branch cannot be empty")
