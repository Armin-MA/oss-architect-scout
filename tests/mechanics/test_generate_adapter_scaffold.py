"""Unit tests for generate_adapter_scaffold pure mechanics."""
import pytest

from src.entities.candidate_repo import CandidateRepo
from src.entities.host_profile import HostProfile
from src.mechanics.generate_adapter_scaffold import generate_adapter_scaffold


@pytest.fixture
def sample_repo():
    return CandidateRepo(
        name="jwt-auth",
        full_name="auth-org/jwt-auth",
        stars=1200,
        forks=300,
        license_spdx="Apache-2.0",
        open_issues=5,
        default_branch="main",
        updated_at="2026-10-01T00:00:00Z",
        description="Fast JWT auth library",
    )


@pytest.fixture
def sample_host():
    return HostProfile(
        architecture_type="Clean Architecture",
        active_skills=["interactive-architect-gatekeeper"],
        banned_libraries=[],
        required_layers=["domain", "adapters"],
        strict_typing=True,
    )


class TestGenerateAdapterScaffold:
    """Test suite for generate_adapter_scaffold."""

    def test_happy_path_scaffold_generation(self, sample_repo, sample_host):
        """Verify successful generation of 4 scaffolded files with valid code content."""
        scaffold = generate_adapter_scaffold(
            repo=sample_repo, host=sample_host, module_name="jwt_verifier"
        )

        assert isinstance(scaffold, dict)
        assert len(scaffold) == 4

        expected_paths = [
            "src/modules/jwt_verifier/contracts/i_jwt_verifier_service.py",
            "src/modules/jwt_verifier/dto/jwt_verifier_dto.py",
            "src/modules/jwt_verifier/adapters/jwt_verifier_adapter.py",
            "src/modules/jwt_verifier/__init__.py",
        ]

        for path in expected_paths:
            assert path in scaffold
            code = scaffold[path]
            assert isinstance(code, str)
            assert len(code) > 50

        # Check content references
        contract_code = scaffold["src/modules/jwt_verifier/contracts/i_jwt_verifier_service.py"]
        assert "class IJwtVerifierService" in contract_code
        assert "auth-org/jwt-auth" in contract_code

        dto_code = scaffold["src/modules/jwt_verifier/dto/jwt_verifier_dto.py"]
        assert "class JwtVerifierDTO" in dto_code

        adapter_code = scaffold["src/modules/jwt_verifier/adapters/jwt_verifier_adapter.py"]
        assert "class JwtVerifierAdapter" in adapter_code
        assert "Apache-2.0" in adapter_code

    def test_edge_case_module_name_sanitization(self, sample_repo, sample_host):
        """Verify module name with hyphens, spaces, and uppercase is sanitized."""
        scaffold = generate_adapter_scaffold(
            repo=sample_repo, host=sample_host, module_name="  My--Cool  Client  "
        )

        expected_dir = "src/modules/my_cool_client"
        assert f"{expected_dir}/__init__.py" in scaffold
        init_code = scaffold[f"{expected_dir}/__init__.py"]
        assert "MyCoolClientAdapter" in init_code

    def test_edge_case_missing_license(self, sample_host):
        """Verify repository without license defaults to UNKNOWN."""
        repo_no_lic = CandidateRepo(
            name="bare-lib",
            full_name="org/bare-lib",
            stars=10,
            forks=2,
            license_spdx=None,
            open_issues=0,
            default_branch="main",
            updated_at="2026-01-01T00:00:00Z",
        )
        scaffold = generate_adapter_scaffold(
            repo=repo_no_lic, host=sample_host, module_name="bare_lib"
        )
        adapter_code = scaffold["src/modules/bare_lib/adapters/bare_lib_adapter.py"]
        assert 'self.license: str = "UNKNOWN"' in adapter_code

    def test_failure_invalid_repo(self, sample_host):
        """Verify ValueError is raised if repo is not CandidateRepo."""
        with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
            generate_adapter_scaffold(None, sample_host, "auth")  # type: ignore

        with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
            generate_adapter_scaffold({"name": "foo"}, sample_host, "auth")  # type: ignore

    def test_failure_invalid_host(self, sample_repo):
        """Verify ValueError is raised if host is not HostProfile."""
        with pytest.raises(ValueError, match="host must be an instance of HostProfile"):
            generate_adapter_scaffold(sample_repo, None, "auth")  # type: ignore

        with pytest.raises(ValueError, match="host must be an instance of HostProfile"):
            generate_adapter_scaffold(sample_repo, "Clean Architecture", "auth")  # type: ignore

    @pytest.mark.parametrize("invalid_name", ["", "   ", None, 123])
    def test_failure_invalid_module_name(self, sample_repo, sample_host, invalid_name):
        """Verify ValueError is raised if module_name is empty or not string."""
        with pytest.raises(ValueError, match="module_name must be a non-empty string"):
            generate_adapter_scaffold(sample_repo, sample_host, invalid_name)  # type: ignore
