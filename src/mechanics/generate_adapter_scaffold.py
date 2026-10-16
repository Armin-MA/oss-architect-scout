"""Adapter and DTO scaffold generation mechanics for shortlisted candidates."""
from __future__ import annotations

import re
from typing import Dict
from src.entities.candidate_repo import CandidateRepo
from src.entities.host_profile import HostProfile


def _sanitize_module_name(name: str) -> str:
    """Sanitize arbitrary string into a valid Python module identifier."""
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name.strip()).lower()
    sanitized = re.sub(r"_+", "_", sanitized).strip("_")
    return sanitized if sanitized else "adapted_component"


def _to_pascal_case(snake_str: str) -> str:
    """Convert snake_case string to PascalCase."""
    return "".join(part.capitalize() for part in snake_str.split("_") if part)


def generate_adapter_scaffold(
    repo: CandidateRepo, host: HostProfile, module_name: str
) -> Dict[str, str]:
    """Generate decoupled DTO and interface adapter code templates for a repository.

    Produces a pure dictionary mapping target file paths to valid Python source code
    conforming to host architectural constraints.

    Args:
        repo: The CandidateRepo entity being adopted.
        host: HostProfile entity specifying host architectural constraints.
        module_name: Desired module name identifier.

    Returns:
        Dict[str, str] mapping relative file paths to generated source code strings.

    Raises:
        ValueError: If inputs are invalid or empty.
    """
    if repo is None or not isinstance(repo, CandidateRepo):
        raise ValueError("repo must be an instance of CandidateRepo")
    if host is None or not isinstance(host, HostProfile):
        raise ValueError("host must be an instance of HostProfile")
    if not isinstance(module_name, str) or not module_name.strip():
        raise ValueError("module_name must be a non-empty string")

    clean_name = _sanitize_module_name(module_name)
    class_name = _to_pascal_case(clean_name)
    license_text = repo.license_spdx or "UNKNOWN"

    base_dir = f"src/modules/{clean_name}"

    contract_path = f"{base_dir}/contracts/i_{clean_name}_service.py"
    dto_path = f"{base_dir}/dto/{clean_name}_dto.py"
    adapter_path = f"{base_dir}/adapters/{clean_name}_adapter.py"
    init_path = f"{base_dir}/__init__.py"

    contract_code = f'''"""Abstract boundary contract interface for {class_name}."""
from __future__ import annotations

from abc import ABC, abstractmethod
from src.modules.{clean_name}.dto.{clean_name}_dto import {class_name}DTO


class I{class_name}Service(ABC):
    """Abstract contract isolating external repository {repo.full_name}."""

    @abstractmethod
    def execute(self, payload: {class_name}DTO) -> {class_name}DTO:
        """Execute operation conforming to {host.architecture_type} contracts."""
        pass
'''

    dto_code = f'''"""Immutable boundary DTO for {class_name} module."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class {class_name}DTO:
    """Immutable data transfer object isolating domain data from {repo.name}."""

    payload: Dict[str, Any] = field(default_factory=dict)
    status: str = "INITIALIZED"
    source_repo: str = "{repo.full_name}"
'''

    adapter_code = f'''"""Interface adapter isolating {repo.full_name} within {host.architecture_type}."""
from __future__ import annotations

from src.modules.{clean_name}.contracts.i_{clean_name}_service import I{class_name}Service
from src.modules.{clean_name}.dto.{clean_name}_dto import {class_name}DTO


class {class_name}Adapter(I{class_name}Service):
    """Swappable interface adapter wrapping external component {repo.full_name}."""

    def __init__(self) -> None:
        self.repo_name: str = "{repo.name}"
        self.full_name: str = "{repo.full_name}"
        self.license: str = "{license_text}"

    def execute(self, payload: {class_name}DTO) -> {class_name}DTO:
        """Execute wrapped mechanics through strict boundary contracts."""
        return {class_name}DTO(
            payload=dict(payload.payload),
            status="EXECUTED",
            source_repo=self.full_name,
        )
'''

    init_code = f'''"""Package entrypoint for {clean_name} module."""
from src.modules.{clean_name}.contracts.i_{clean_name}_service import I{class_name}Service
from src.modules.{clean_name}.dto.{clean_name}_dto import {class_name}DTO
from src.modules.{clean_name}.adapters.{clean_name}_adapter import {class_name}Adapter

__all__ = ["I{class_name}Service", "{class_name}DTO", "{class_name}Adapter"]
'''

    return {
        contract_path: contract_code,
        dto_path: dto_code,
        adapter_path: adapter_code,
        init_path: init_code,
    }
