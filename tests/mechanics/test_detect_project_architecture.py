"""Unit tests for detect_project_architecture pure mechanics."""
import pytest

from src.entities.host_profile import HostProfile
from src.mechanics.detect_project_architecture import detect_project_architecture


class TestDetectProjectArchitecture:
    """Test suite for detect_project_architecture."""

    def test_happy_path_detect_interactive_architect(self):
        """Verify Layered Architecture (Interactive Architect) detection."""
        paths = [
            "src/contracts/i_service.py",
            "src/entities/user.py",
            "src/mechanics/process_user.py",
            "specs/ARCHITECTURE.md",
            ".cursorrules",
        ]
        profile = detect_project_architecture(paths)

        assert isinstance(profile, HostProfile)
        assert "Interactive Architect" in profile.architecture_type
        assert "contracts" in profile.required_layers
        assert "mechanics" in profile.required_layers
        assert "interactive-architect-gatekeeper" in profile.active_skills
        assert "cursor-rules" in profile.active_skills

    def test_happy_path_detect_clean_architecture(self):
        """Verify Clean Architecture detection."""
        paths = [
            "src/domain/entities/order.py",
            "src/use_cases/create_order.py",
            "src/adapters/controllers/order_controller.py",
            "src/infrastructure/db.py",
        ]
        profile = detect_project_architecture(paths)

        assert profile.architecture_type == "Clean Architecture"
        assert "domain" in profile.required_layers
        assert "use_cases" in profile.required_layers
        assert "adapters" in profile.required_layers

    def test_happy_path_detect_hexagonal_architecture(self):
        """Verify Hexagonal Architecture detection."""
        paths = [
            "app/ports/inbound.py",
            "app/adapters/outbound.py",
        ]
        profile = detect_project_architecture(paths)

        assert profile.architecture_type == "Hexagonal Architecture"
        assert "ports" in profile.required_layers

    def test_happy_path_detect_mvc(self):
        """Verify MVC pattern detection."""
        paths = [
            "app/models/user.py",
            "app/views/user_view.py",
            "app/controllers/user_controller.py",
        ]
        profile = detect_project_architecture(paths)

        assert profile.architecture_type == "MVC"
        assert "models" in profile.required_layers
        assert "views" in profile.required_layers
        assert "controllers" in profile.required_layers

    def test_edge_case_fallback_modular(self):
        """Verify unmapped or simple project falls back to Modular."""
        paths = [
            "main.py",
            "utils.py",
            "config.py",
        ]
        profile = detect_project_architecture(paths)

        assert profile.architecture_type == "Modular"
        assert "modules" in profile.required_layers

    def test_edge_case_empty_paths(self):
        """Verify empty list falls back to default Modular profile."""
        profile = detect_project_architecture([])

        assert isinstance(profile, HostProfile)
        assert profile.architecture_type == "Modular"
        assert profile.active_skills == []

    def test_edge_case_windows_paths(self):
        """Verify Windows backslash paths are correctly parsed."""
        paths = [
            r"src\contracts\i_repo.py",
            r"src\entities\item.py",
            r"src\mechanics\calculate.py",
        ]
        profile = detect_project_architecture(paths)
        assert "Interactive Architect" in profile.architecture_type

    def test_failure_invalid_input_type(self):
        """Verify ValueError is raised when input is not a list."""
        with pytest.raises(ValueError, match="existing_file_paths must be a list"):
            detect_project_architecture(None)  # type: ignore

        with pytest.raises(ValueError, match="existing_file_paths must be a list"):
            detect_project_architecture("src/main.py")  # type: ignore

    def test_failure_elements_not_strings(self):
        """Verify ValueError is raised when elements are not strings."""
        with pytest.raises(ValueError, match="All elements in existing_file_paths must be strings"):
            detect_project_architecture(["src/main.py", 123])  # type: ignore
