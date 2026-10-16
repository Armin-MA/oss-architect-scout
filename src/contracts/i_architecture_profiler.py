"""Abstract contract for host project architecture profiling."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.entities.host_profile import HostProfile
else:
    try:
        from src.entities.host_profile import HostProfile
    except ImportError:
        HostProfile = Any  # type: ignore


class IArchitectureProfiler(ABC):
    """Abstract interface declaring architecture scanning for host projects."""

    @abstractmethod
    def profile_host(self, project_path: str) -> HostProfile:
        """Scan host project at project_path and extract HostProfile."""
        pass
