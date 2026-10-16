"""Unit tests for calculate_malleability_score pure mechanics."""
import pytest

from src.entities.host_profile import HostProfile
from src.mechanics.calculate_malleability_score import calculate_malleability_score


@pytest.fixture
def default_host():
    return HostProfile(
        architecture_type="Layered",
        active_skills=["interactive-architect-gatekeeper"],
        banned_libraries=["tensorflow", "django"],
        required_layers=["contracts", "mechanics"],
        strict_typing=True,
    )


class TestCalculateMalleabilityScore:
    """Test suite for calculate_malleability_score."""

    def test_happy_path_highly_malleable_repo(self, default_host):
        """Verify modular, compact repo without banned libs scores 100.0."""
        paths = [
            "src/domain/model.py",
            "src/adapters/client.py",
            "src/__init__.py",
            "src/core/utils.py",
        ]
        score = calculate_malleability_score(paths, default_host)

        assert isinstance(score, float)
        assert score == 100.0

    def test_happy_path_banned_libraries_penalty(self, default_host):
        """Verify detection of banned libraries reduces malleability score."""
        clean_paths = [
            "src/core/math.py",
            "src/lib/helper.py",
            "src/__init__.py",
        ]
        score_clean = calculate_malleability_score(clean_paths, default_host)

        tainted_paths = [
            "src/core/math.py",
            "src/lib/django_models.py",
            "src/__init__.py",
        ]
        score_tainted = calculate_malleability_score(tainted_paths, default_host)

        assert score_tainted == score_clean - 15.0

    def test_edge_case_empty_tree(self, default_host):
        """Verify empty tree returns 0.0."""
        assert calculate_malleability_score([], default_host) == 0.0

    def test_edge_case_large_monolithic_repo(self, default_host):
        """Verify large flat codebase receives lower score."""
        flat_paths = [f"file_{i}.py" for i in range(1200)]
        score = calculate_malleability_score(flat_paths, default_host)

        # Flat dirs: 10, no banned: 30, no init: 5, size > 1000: 0 -> 45.0
        assert score == 45.0

    def test_edge_case_windows_paths(self, default_host):
        """Verify Windows backslash paths are handled correctly."""
        paths = [
            r"src\pkg\service.py",
            r"src\domain\entity.py",
            r"src\__init__.py",
        ]
        score = calculate_malleability_score(paths, default_host)
        assert score == 100.0

    def test_edge_case_multiple_banned_libraries(self, default_host):
        """Verify multiple banned libraries deduct multiple times down to floor."""
        tainted_paths = [
            "src/core/django_view.py",
            "src/lib/tensorflow_model.py",
        ]
        score = calculate_malleability_score(tainted_paths, default_host)
        # dirs: 40, banned: 30 - 30 = 0, entry: 5, size: 15 -> 60.0
        assert score == 60.0

    def test_failure_invalid_repo_tree_paths(self, default_host):
        """Verify ValueError is raised if repo_tree_paths is not a list."""
        with pytest.raises(ValueError, match="repo_tree_paths must be a list"):
            calculate_malleability_score(None, default_host)  # type: ignore

        with pytest.raises(ValueError, match="repo_tree_paths must be a list"):
            calculate_malleability_score("src/app.py", default_host)  # type: ignore

    def test_failure_invalid_host_profile(self):
        """Verify ValueError is raised if host_profile is not HostProfile."""
        with pytest.raises(ValueError, match="host_profile must be an instance of HostProfile"):
            calculate_malleability_score(["src/main.py"], None)  # type: ignore

        with pytest.raises(ValueError, match="host_profile must be an instance of HostProfile"):
            calculate_malleability_score(["src/main.py"], {"type": "layered"})  # type: ignore

    def test_failure_elements_not_strings(self, default_host):
        """Verify ValueError is raised if elements are not strings."""
        with pytest.raises(ValueError, match="All elements in repo_tree_paths must be strings"):
            calculate_malleability_score(["src/main.py", 100], default_host)  # type: ignore
