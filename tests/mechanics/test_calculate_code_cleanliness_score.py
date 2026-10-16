"""Unit tests for calculate_code_cleanliness_score pure mechanics."""
import pytest

from src.mechanics.calculate_code_cleanliness_score import calculate_code_cleanliness_score


class TestCalculateCodeCleanlinessScore:
    """Test suite for calculate_code_cleanliness_score."""

    def test_happy_path_ideal_repository(self):
        """Verify repository with full test suite, passing CI, typing and linter scores 100."""
        paths = [
            "src/main.py",
            "tests/test_main.py",
            "tests/test_service.py",
            "tests/test_utils.py",
            ".github/workflows/ci.yml",
            "pyproject.toml",
            ".flake8",
        ]
        score = calculate_code_cleanliness_score(paths, ci_status="success")

        assert isinstance(score, float)
        assert score == 100.0

    def test_happy_path_partial_score(self):
        """Verify partial presence gives appropriate weighted score."""
        paths = [
            "src/index.ts",
            "test_basic.py",
            "tsconfig.json",
        ]
        score = calculate_code_cleanliness_score(paths, ci_status="unknown")

        # 25 (1 test) + 10 (neutral CI) + 15 (tsconfig typing) = 50.0
        assert score == 50.0

    def test_edge_case_empty_tree_failing_ci(self):
        """Verify empty tree with failing CI returns 0.0."""
        score = calculate_code_cleanliness_score([], ci_status="failure")
        assert score == 0.0

    def test_edge_case_empty_tree_passing_ci(self):
        """Verify empty tree with passing CI receives base CI score (30.0)."""
        score = calculate_code_cleanliness_score([], ci_status="passing")
        assert score == 30.0

    def test_edge_case_windows_paths(self):
        """Verify Windows backslash paths are handled seamlessly."""
        paths = [
            r"src\core\service.py",
            r"tests\unit\test_service.py",
            r"tests\unit\test_core.py",
            r"tests\unit\test_utils.py",
            r".github\workflows\tests.yml",
            r"mypy.ini",
            r"ruff.toml",
        ]
        score = calculate_code_cleanliness_score(paths, ci_status="passed")
        assert score == 100.0

    def test_edge_case_pyproject_fallback_linter(self):
        """Verify pyproject.toml alone provides typing and partial linter score."""
        paths = [
            "src/app.py",
            "pyproject.toml",
        ]
        score = calculate_code_cleanliness_score(paths, ci_status="unknown")
        # 0 (tests) + 10 (unknown CI) + 15 (typing) + 10 (pyproject linter) = 35.0
        assert score == 35.0

    def test_edge_case_test_dir_without_code_files(self):
        """Verify directory containing tests gives directory score (15.0)."""
        paths = ["tests/README.md"]
        score = calculate_code_cleanliness_score(paths, ci_status="error")
        assert score == 15.0

    def test_failure_invalid_repo_tree_type(self):
        """Verify ValueError is raised when repo_tree_paths is not a list."""
        with pytest.raises(ValueError, match="repo_tree_paths must be a list"):
            calculate_code_cleanliness_score(None, "passing")  # type: ignore

        with pytest.raises(ValueError, match="repo_tree_paths must be a list"):
            calculate_code_cleanliness_score("src/app.py", "passing")  # type: ignore

    def test_failure_invalid_ci_status_type(self):
        """Verify ValueError is raised when ci_status is not a string."""
        with pytest.raises(ValueError, match="ci_status must be a string"):
            calculate_code_cleanliness_score([], 123)  # type: ignore

    def test_failure_elements_not_strings(self):
        """Verify ValueError is raised when list elements are not strings."""
        with pytest.raises(ValueError, match="All elements in repo_tree_paths must be strings"):
            calculate_code_cleanliness_score(["src/app.py", 42], "passing")  # type: ignore
