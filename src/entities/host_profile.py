"""HostProfile domain entity representing host project architectural constraints."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class HostProfile:
    """Domain entity holding detected architecture profile and rules of the host project."""

    architecture_type: str
    active_skills: List[str] = field(default_factory=list)
    banned_libraries: List[str] = field(default_factory=list)
    required_layers: List[str] = field(default_factory=list)
    strict_typing: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.architecture_type, str) or not self.architecture_type.strip():
            raise ValueError("architecture_type cannot be empty")
        if self.active_skills is None:
            self.active_skills = []
        if self.banned_libraries is None:
            self.banned_libraries = []
        if self.required_layers is None:
            self.required_layers = []
        if not isinstance(self.strict_typing, bool):
            raise ValueError("strict_typing must be a boolean")
