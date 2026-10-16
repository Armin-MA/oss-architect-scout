"""Unit tests for CLI presentation controller (TASK-029)."""
import io
from typing import List
import pytest

from src.contracts.i_architecture_profiler import IArchitectureProfiler
from src.contracts.i_github_client import IGitHubClient
from src.contracts.i_pruning_funnel import IPruningFunnel
from src.contracts.i_scoring_engine import IScoringEngine
from src.contracts.i_scout_repository import IScoutRepository
from src.contracts.i_ui_presenter import IUIPresenter
from src.core.container import Container
from src.database.dto.evaluation_record_dto import EvaluationRecordDTO
from src.entities.candidate_repo import CandidateRepo
from src.entities.evaluation_score import EvaluationScore
from src.entities.host_profile import HostProfile
from src.ui.cli_controller import CLIController, create_parser, main


class MockProfiler(IArchitectureProfiler):
    def profile_host(self, project_path: str) -> HostProfile:
        return HostProfile(architecture_type="Clean Layered Architecture")


class MockGitHubClient(IGitHubClient):
    def search_repositories(self, query: str, limit: int = 50) -> List[CandidateRepo]:
        return [
            CandidateRepo(
                name="test-repo",
                full_name="org/test-repo",
                stars=500,
                forks=50,
                license_spdx="MIT",
            )
        ]

    def get_repository_tree(self, full_name: str) -> List[str]:
        return []

    def get_file_content(self, full_name: str, path: str) -> str:
        return ""

    def check_ci_status(self, full_name: str) -> str:
        return "SUCCESS"


class MockFunnel(IPruningFunnel):
    def prune_stage1_metadata(self, repos: List[CandidateRepo]) -> List[CandidateRepo]:
        return repos

    def prune_stage2_heuristics(
        self, repos: List[CandidateRepo], client: IGitHubClient
    ) -> List[CandidateRepo]:
        return repos

    def prune_stage3_deep(
        self, repos: List[CandidateRepo], host: HostProfile
    ) -> List[CandidateRepo]:
        return repos


class MockScoringEngine(IScoringEngine):
    def score_candidate(self, repo: CandidateRepo, host: HostProfile) -> EvaluationScore:
        return EvaluationScore(
            repo=repo,
            architecture_score=90.0,
            cleanliness_score=90.0,
            community_score=90.0,
            popularity_score=90.0,
            hygiene_score=90.0,
            final_score=90.0,
        )


class MockRepository(IScoutRepository):
    def __init__(self, history: List[EvaluationRecordDTO] = None) -> None:
        self.history = history or []

    def save_evaluation_run(self, run) -> str:
        return "run-cli-123"

    def get_evaluation_history(self, limit: int = 10) -> List[EvaluationRecordDTO]:
        return self.history


class MockPresenter(IUIPresenter):
    def render_evaluation_report(self, scores: List[EvaluationScore], host_profile=None) -> str:
        return f"# CLI Visual Report for {len(scores)} candidates"

    def render_risk_confirmation(self, repo: CandidateRepo, risks: List[str]) -> str:
        return ""


@pytest.fixture
def mock_container() -> Container:
    container = Container()
    container.register_instance(IArchitectureProfiler, MockProfiler())
    container.register_instance(IGitHubClient, MockGitHubClient())
    container.register_instance(IPruningFunnel, MockFunnel())
    container.register_instance(IScoringEngine, MockScoringEngine())
    container.register_instance(IScoutRepository, MockRepository())
    container.register_instance(IUIPresenter, MockPresenter())
    return container


# --- 1. Happy Path Tests ---

def test_cli_controller_happy_path(mock_container: Container):
    """Verify standard execution with --query prints report and exits with 0."""
    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(container=mock_container, stdout=out, stderr=err)

    exit_code = controller.run(["--query", "fastapi clean architecture"])

    assert exit_code == 0
    assert "# CLI Visual Report for 1 candidates" in out.getvalue()
    assert err.getvalue() == ""


def test_cli_controller_with_all_options(mock_container: Container):
    """Verify execution with path and allow-copyleft flags."""
    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(container=mock_container, stdout=out, stderr=err)

    exit_code = controller.run([
        "-q", "flask template",
        "-p", "custom/project/path",
        "--allow-copyleft",
    ])

    assert exit_code == 0
    assert "# CLI Visual Report" in out.getvalue()


def test_cli_controller_history_mode(mock_container: Container):
    """Verify --mode history retrieves and displays previous records."""
    history_records = [
        EvaluationRecordDTO(
            run_id="run-1",
            repo_full_name="example/awesome-repo",
            stars=1500,
            license_type="MIT",
            final_score=89.5,
        )
    ]
    mock_container.register_instance(IScoutRepository, MockRepository(history=history_records))

    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(container=mock_container, stdout=out, stderr=err)

    exit_code = controller.run(["--query", "unused", "--mode", "history"])

    assert exit_code == 0
    assert "# Past Evaluation History" in out.getvalue()
    assert "example/awesome-repo: Score 89.5" in out.getvalue()


# --- 2. Edge Case Tests ---

def test_cli_controller_help_flag():
    """Verify --help flag exits cleanly with code 0."""
    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(stdout=out, stderr=err)

    exit_code = controller.run(["--help"])
    assert exit_code == 0


def test_cli_controller_history_empty(mock_container: Container):
    """Verify history mode with empty database prints informative message."""
    mock_container.register_instance(IScoutRepository, MockRepository(history=[]))

    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(container=mock_container, stdout=out, stderr=err)

    exit_code = controller.run(["--query", "unused", "--mode", "history"])

    assert exit_code == 0
    assert "No previous evaluation history found." in out.getvalue()


def test_cli_controller_main_entrypoint(monkeypatch, mock_container: Container):
    """Verify main() entrypoint runs and returns 0."""
    monkeypatch.setattr(
        "src.ui.cli_controller.CLIController",
        lambda: CLIController(container=mock_container, stdout=io.StringIO(), stderr=io.StringIO())
    )
    exit_code = main(["--query", "fastapi"])
    assert exit_code == 0


# --- 3. Failure State Tests ---

def test_cli_controller_missing_query():
    """Verify missing required --query argument returns non-zero code."""
    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(stdout=out, stderr=err)

    exit_code = controller.run([])
    assert exit_code != 0


def test_cli_controller_empty_query_string():
    """Verify empty or blank query returns error code 1."""
    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(stdout=out, stderr=err)

    exit_code = controller.run(["--query", "   "])
    assert exit_code == 1
    assert "Error: --query argument cannot be empty." in err.getvalue()


def test_cli_controller_orchestrator_failure_handled(mock_container: Container):
    """Verify exceptions during orchestration are cleanly caught with code 1."""
    class FailingProfiler(IArchitectureProfiler):
        def profile_host(self, project_path: str):
            raise RuntimeError("Host profile filesystem read error")

    mock_container.register_instance(IArchitectureProfiler, FailingProfiler())

    out = io.StringIO()
    err = io.StringIO()
    controller = CLIController(container=mock_container, stdout=out, stderr=err)

    exit_code = controller.run(["--query", "valid-query"])

    assert exit_code == 1
    assert "Scout execution failed: Host profile filesystem read error" in err.getvalue()
