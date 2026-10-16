"""Unit tests for filter_veto_gate pure mechanics."""
import pytest

from src.entities.candidate_repo import CandidateRepo
from src.entities.veto_result import VetoResult
from src.mechanics.filter_veto_gate import filter_veto_gate


@pytest.fixture
def make_repo():
    """Factory fixture to create sample CandidateRepo instances."""
    def _make(license_spdx=None, name="test-repo", full_name="org/test-repo"):
        return CandidateRepo(
            name=name,
            full_name=full_name,
            stars=100,
            forks=20,
            license_spdx=license_spdx,
            open_issues=5,
            default_branch="main",
            updated_at="2026-01-01T00:00:00Z",
            description="Test repo description",
        )
    return _make


class TestFilterVetoGate:
    """Test suite for filter_veto_gate function."""

    @pytest.mark.parametrize("spdx", ["MIT", "Apache-2.0", "BSD-3-Clause", "0BSD", "ISC"])
    def test_happy_path_permissive_licenses(self, make_repo, spdx):
        """Verify permissive licenses pass unconditionally."""
        repo = make_repo(license_spdx=spdx)
        result = filter_veto_gate(repo, allow_copyleft=False)

        assert isinstance(result, VetoResult)
        assert result.is_passed is True
        assert result.severity == "NONE"
        assert "Permissive license" in result.reason

    @pytest.mark.parametrize("spdx", ["GPL-3.0", "AGPL-3.0", "LGPL-3.0", "MPL-2.0"])
    def test_happy_path_copyleft_allowed_by_override(self, make_repo, spdx):
        """Verify copyleft licenses pass with WARNING when allow_copyleft is True."""
        repo = make_repo(license_spdx=spdx)
        result = filter_veto_gate(repo, allow_copyleft=True)

        assert isinstance(result, VetoResult)
        assert result.is_passed is True
        assert result.severity == "WARNING"
        assert "accepted by user override" in result.reason

    @pytest.mark.parametrize("spdx", ["GPL-3.0", "AGPL-3.0", "LGPL-2.1", "EUPL-1.2"])
    def test_failure_copyleft_rejected_by_default(self, make_repo, spdx):
        """Verify copyleft licenses are vetoed by default."""
        repo = make_repo(license_spdx=spdx)
        result = filter_veto_gate(repo, allow_copyleft=False)

        assert isinstance(result, VetoResult)
        assert result.is_passed is False
        assert result.severity == "CRITICAL"
        assert "Viral copyleft license" in result.reason

    @pytest.mark.parametrize("spdx", ["BSL-1.1", "SSPL-1.0", "Commons-Clause"])
    def test_failure_commercial_restricted_rejected(self, make_repo, spdx):
        """Verify commercial restricted / source-available licenses are always vetoed."""
        repo = make_repo(license_spdx=spdx)
        result = filter_veto_gate(repo, allow_copyleft=True)

        assert isinstance(result, VetoResult)
        assert result.is_passed is False
        assert result.severity == "CRITICAL"
        assert "Commercial restricted" in result.reason

    def test_edge_case_missing_license(self, make_repo):
        """Verify missing license (None) results in critical veto."""
        repo = make_repo(license_spdx=None)
        result = filter_veto_gate(repo, allow_copyleft=True)

        assert isinstance(result, VetoResult)
        assert result.is_passed is False
        assert result.severity == "CRITICAL"
        assert "missing or unidentified" in result.reason.lower()

    def test_edge_case_unknown_license(self, make_repo):
        """Verify unrecognized license string results in critical veto."""
        repo = make_repo(license_spdx="Custom-Proprietary-License-2026")
        result = filter_veto_gate(repo, allow_copyleft=False)

        assert isinstance(result, VetoResult)
        assert result.is_passed is False
        assert result.severity == "CRITICAL"
        assert "Unrecognized or unmapped" in result.reason

    def test_failure_invalid_repo_type(self):
        """Verify ValueError is raised if repo is not a CandidateRepo."""
        with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
            filter_veto_gate(None)  # type: ignore

        with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
            filter_veto_gate({"name": "dict-repo"})  # type: ignore

    def test_failure_invalid_allow_copyleft_type(self, make_repo):
        """Verify ValueError is raised if allow_copyleft is not boolean."""
        repo = make_repo(license_spdx="MIT")
        with pytest.raises(ValueError, match="allow_copyleft must be a boolean"):
            filter_veto_gate(repo, allow_copyleft="true")  # type: ignore
