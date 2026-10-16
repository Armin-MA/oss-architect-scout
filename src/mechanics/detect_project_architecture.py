"""Host project architecture detection and profiling mechanics."""
from __future__ import annotations

from typing import List, Set
from src.entities.host_profile import HostProfile


def detect_project_architecture(existing_file_paths: List[str]) -> HostProfile:
    """Scan existing project file paths to detect architecture and construct a HostProfile.

    Detects architectural patterns:
    - Layered Architecture (Interactive Architect Gatekeeper)
    - Clean Architecture
    - Hexagonal Architecture (Ports & Adapters)
    - MVC
    - Fallback: Modular

    Also extracts active skills, required architectural layers, and strict typing status.

    Args:
        existing_file_paths: List of relative or absolute file paths in the host project.

    Returns:
        HostProfile domain entity with detected configuration.

    Raises:
        ValueError: If existing_file_paths is not a list of strings.
    """
    if existing_file_paths is None or not isinstance(existing_file_paths, list):
        raise ValueError("existing_file_paths must be a list of file path strings")

    for path in existing_file_paths:
        if not isinstance(path, str):
            raise ValueError("All elements in existing_file_paths must be strings")

    if not existing_file_paths:
        return HostProfile(
            architecture_type="Modular",
            active_skills=[],
            banned_libraries=[],
            required_layers=["modules"],
            strict_typing=True,
        )

    normalized_paths = [p.replace("\\", "/").lower() for p in existing_file_paths]

    # Collect unique directory segments and file basenames
    dir_segments: Set[str] = set()
    basenames: Set[str] = set()
    for path in normalized_paths:
        parts = path.split("/")
        basenames.add(parts[-1])
        for seg in parts[:-1]:
            dir_segments.add(seg)

    # 1. Detect Architecture Pattern
    if (
        "contracts" in dir_segments
        and "mechanics" in dir_segments
        and "entities" in dir_segments
    ):
        arch_type = "Layered Architecture (Interactive Architect)"
        required_layers = ["contracts", "entities", "mechanics", "database", "ui", "core"]
    elif (
        ("domain" in dir_segments or "entities" in dir_segments)
        and ("usecases" in dir_segments or "use_cases" in dir_segments)
        and ("adapters" in dir_segments or "infrastructure" in dir_segments)
    ):
        arch_type = "Clean Architecture"
        required_layers = ["domain", "use_cases", "adapters", "infrastructure"]
    elif "ports" in dir_segments and "adapters" in dir_segments:
        arch_type = "Hexagonal Architecture"
        required_layers = ["domain", "ports", "adapters"]
    elif (
        "models" in dir_segments
        and "views" in dir_segments
        and "controllers" in dir_segments
    ):
        arch_type = "MVC"
        required_layers = ["models", "views", "controllers"]
    else:
        arch_type = "Modular"
        required_layers = ["modules"]

    # 2. Detect Active Skills & Rule Sets
    active_skills: List[str] = []
    if any(
        "interactive-architect-gatekeeper" in p or "specs/architecture.md" in p
        for p in normalized_paths
    ):
        active_skills.append("interactive-architect-gatekeeper")

    if any(".cursorrules" in base for base in basenames) or any(
        ".cursor/rules" in p for p in normalized_paths
    ):
        active_skills.append("cursor-rules")

    if any("rules/" in p or p.startswith("rules") for p in normalized_paths):
        if "rules" not in active_skills:
            active_skills.append("rules")

    if any("superpowers" in p for p in normalized_paths):
        active_skills.append("superpowers")

    # 3. Detect Strict Typing
    has_typing_config = any(
        base in ("mypy.ini", ".mypy.ini", "tsconfig.json", "py.typed")
        for base in basenames
    )
    has_typed_files = any(
        p.endswith((".ts", ".tsx")) for p in normalized_paths
    )
    # Default to True for modern projects or if typing indicators exist
    strict_typing = True if (has_typing_config or has_typed_files or not normalized_paths) else True

    return HostProfile(
        architecture_type=arch_type,
        active_skills=active_skills,
        banned_libraries=[],
        required_layers=required_layers,
        strict_typing=strict_typing,
    )
