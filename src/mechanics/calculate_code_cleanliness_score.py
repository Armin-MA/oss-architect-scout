"""Code cleanliness and test coverage score calculation mechanics."""
from __future__ import annotations

from typing import List

TYPING_CONFIG_FILES = {
    "mypy.ini",
    ".mypy.ini",
    "tsconfig.json",
    "pyproject.toml",
    "setup.cfg",
    "py.typed",
    "types.d.ts",
}

LINTER_CONFIG_FILES = {
    ".flake8",
    ".eslintrc",
    ".eslintrc.json",
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.yaml",
    ".prettierrc",
    "ruff.toml",
    ".ruff.toml",
    ".pylintrc",
    "biome.json",
    ".editorconfig",
}

CI_CONFIG_PATTERNS = (
    ".github/workflows",
    ".travis.yml",
    ".circleci",
    "azure-pipelines.yml",
    "jenkinsfile",
    ".gitlab-ci.yml",
)


def calculate_code_cleanliness_score(
    repo_tree_paths: List[str], ci_status: str
) -> float:
    """Compute code cleanliness score (0.0 to 100.0) from tree paths and CI status.

    Evaluates:
    1. Test presence and directory structure (up to 35 pts)
    2. CI build status and workflow configuration (up to 35 pts)
    3. Type checking configuration (up to 15 pts)
    4. Linter/formatter configuration (up to 15 pts)

    Args:
        repo_tree_paths: List of relative repository file paths.
        ci_status: CI execution status ('passing', 'success', 'failing', etc.).

    Returns:
        float score between 0.0 and 100.0 rounded to 2 decimal places.

    Raises:
        ValueError: If input parameters are of invalid type.
    """
    if repo_tree_paths is None or not isinstance(repo_tree_paths, list):
        raise ValueError("repo_tree_paths must be a list of file path strings")
    if ci_status is None or not isinstance(ci_status, str):
        raise ValueError("ci_status must be a string")

    for path in repo_tree_paths:
        if not isinstance(path, str):
            raise ValueError("All elements in repo_tree_paths must be strings")

    normalized_paths = [p.replace("\\", "/").lower() for p in repo_tree_paths]

    # 1. Test suite evaluation (max 35.0)
    test_files_count = 0
    has_test_dir = False

    for path in normalized_paths:
        parts = path.split("/")
        filename = parts[-1]

        if any(seg in ("tests", "test", "__tests__", "spec", "specs") for seg in parts[:-1]):
            has_test_dir = True
            if filename.endswith((".py", ".ts", ".js", ".go", ".rs", ".java")):
                test_files_count += 1
        elif (
            filename.startswith("test_")
            or filename.endswith(("_test.py", ".spec.ts", ".test.ts", ".spec.js", ".test.js"))
        ):
            test_files_count += 1

    if test_files_count >= 3:
        test_score = 35.0
    elif test_files_count >= 1:
        test_score = 25.0
    elif has_test_dir:
        test_score = 15.0
    else:
        test_score = 0.0

    # 2. CI build evaluation (max 35.0)
    normalized_ci = ci_status.strip().lower()
    has_ci_config = any(
        any(pattern in path for pattern in CI_CONFIG_PATTERNS)
        for path in normalized_paths
    )

    if normalized_ci in ("success", "passing", "passed"):
        ci_score = 30.0 + (5.0 if has_ci_config else 0.0)
    elif normalized_ci in ("pending", "running"):
        ci_score = 15.0 + (5.0 if has_ci_config else 0.0)
    elif normalized_ci in ("neutral", "skipped", "unknown", "none", ""):
        ci_score = 10.0 + (5.0 if has_ci_config else 0.0)
    elif normalized_ci in ("failure", "failing", "failed", "error"):
        ci_score = 0.0
    else:
        ci_score = 5.0 if has_ci_config else 0.0

    ci_score = min(35.0, ci_score)

    # 3. Typing & Linter configs (max 30.0)
    typing_score = 0.0
    linter_score = 0.0

    basenames = {p.split("/")[-1] for p in normalized_paths}

    if any(cfg.lower() in basenames for cfg in TYPING_CONFIG_FILES):
        typing_score = 15.0

    if any(cfg.lower() in basenames for cfg in LINTER_CONFIG_FILES):
        linter_score = 15.0
    elif "pyproject.toml" in basenames:
        # pyproject.toml often defines linter tool configs (ruff, flake8)
        linter_score = 10.0

    total_score = test_score + ci_score + typing_score + linter_score
    clamped_score = max(0.0, min(100.0, total_score))
    return round(clamped_score, 2)
