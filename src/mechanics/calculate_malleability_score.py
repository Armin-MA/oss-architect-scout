"""Architectural malleability and refactoring friction score calculation mechanics."""
from __future__ import annotations

from typing import List
from src.entities.host_profile import HostProfile

MODULAR_DIRECTORIES = {
    "src",
    "lib",
    "pkg",
    "core",
    "domain",
    "entities",
    "interfaces",
    "contracts",
    "adapters",
    "modules",
    "internal",
}

ENTRY_POINTS = {
    "__init__.py",
    "index.ts",
    "index.js",
    "api.py",
    "exports.py",
    "mod.rs",
    "main.go",
    "public_api.ts",
}

CODE_EXTENSIONS = (
    ".py",
    ".ts",
    ".js",
    ".go",
    ".rs",
    ".java",
    ".c",
    ".cpp",
    ".cs",
)


def calculate_malleability_score(
    repo_tree_paths: List[str], host_profile: HostProfile
) -> float:
    """Compute architectural malleability score (0.0 to 100.0) for a candidate repository.

    Higher scores indicate the repository's mechanics can be decoupled, refactored,
    and wrapped behind host profile contracts with minimal friction.

    Evaluates:
    1. Modularity and layered directory hierarchy (up to 40 pts)
    2. Freedom from host-banned libraries and intrusive dependencies (up to 30 pts)
    3. Clear entry point and public interface encapsulation (up to 15 pts)
    4. Codebase size and refactoring friction index (up to 15 pts)

    Args:
        repo_tree_paths: List of relative repository file paths.
        host_profile: HostProfile entity specifying architectural constraints.

    Returns:
        float score between 0.0 and 100.0 rounded to 2 decimal places.

    Raises:
        ValueError: If input parameters are invalid.
    """
    if repo_tree_paths is None or not isinstance(repo_tree_paths, list):
        raise ValueError("repo_tree_paths must be a list of strings")
    if host_profile is None or not isinstance(host_profile, HostProfile):
        raise ValueError("host_profile must be an instance of HostProfile")

    for path in repo_tree_paths:
        if not isinstance(path, str):
            raise ValueError("All elements in repo_tree_paths must be strings")

    if not repo_tree_paths:
        return 0.0

    normalized_paths = [p.replace("\\", "/").lower() for p in repo_tree_paths]

    # 1. Modularity & Layer Hierarchy (up to 40.0 pts)
    found_dirs = set()
    for path in normalized_paths:
        parts = path.split("/")
        for part in parts[:-1]:
            if part in MODULAR_DIRECTORIES:
                found_dirs.add(part)

    if len(found_dirs) >= 2:
        modularity_score = 40.0
    elif len(found_dirs) == 1:
        modularity_score = 30.0
    else:
        modularity_score = 10.0

    # 2. Banned Libraries Coupling Penalty (up to 30.0 pts)
    banned_score = 30.0
    if host_profile.banned_libraries:
        for banned in host_profile.banned_libraries:
            banned_lower = banned.strip().lower()
            if not banned_lower:
                continue
            if any(banned_lower in path for path in normalized_paths):
                banned_score = max(0.0, banned_score - 15.0)

    # 3. Entry point / Clean interface surface (up to 15.0 pts)
    basenames = {p.split("/")[-1] for p in normalized_paths}
    if any(ep in basenames for ep in ENTRY_POINTS):
        entrypoint_score = 15.0
    else:
        entrypoint_score = 5.0

    # 4. Codebase Size / Refactoring Friction (up to 15.0 pts)
    code_files_count = sum(
        1 for p in normalized_paths if p.endswith(CODE_EXTENSIONS)
    )

    if code_files_count <= 50:
        size_score = 15.0
    elif code_files_count <= 200:
        size_score = 10.0
    elif code_files_count <= 1000:
        size_score = 5.0
    else:
        size_score = 0.0

    total_score = modularity_score + banned_score + entrypoint_score + size_score
    clamped_score = max(0.0, min(100.0, total_score))
    return round(clamped_score, 2)
