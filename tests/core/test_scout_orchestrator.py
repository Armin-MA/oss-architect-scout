"""Unit tests for ScoutOrchestrator (TASK-028)."""
from typing import Any, List, Optional
import pytest

from src.contracts.i_architecture_profiler import IArchitectureProfiler
from src.contracts.i_github_client import IGitHubClient
from src.contracts.i_pruning_funnel import IPruningFunnel
from src.contracts.i_scoring_engine import IScoringEngine
from src.contracts.i_scout_repository import IScoutRepository
from src.contracts.i_ui_presenter import IUIPresenter
from src.core.scout_orchestrator import ScoutOrchestrator, ScoutResult
from src.entities.candidate_repo import CandidateRepo
from src.entities.evaluation_score import EvaluationScore
from src.entities.host_profile import HostProfile


class MockProfiler(IArchitectureProfiler):
    def __init__(self, profile: Optional[HostProfile] = None) -> None:
        self.profile = profile or HostProfile(
            architecture_type="Clean Layered Architecture",
            active_skills=["test-driven-development"],
            banned_libraries=[],
            required_layers=["contracts", "entities", "core"],
            strict_typing=True,
        )

    def profile_host(self, project_path: str) -> HostProfile:
        return self.profile


class MockGitHubClient(IGitHubClient):
    def __init__(self, candidates: Optional[List[CandidateRepo]] = None) -> None:
        self.candidates = candidates if candidates is not None else []
        self.last_query: Optional[str] = None
        self.last_limit: Optional[int] = None

    def search_repositories(self, query: str, limit: int = 50) -> List[CandidateRepo]:
        self.last_query = query
        self.last_limit = limit
        return self.candidates

    def get_repository_tree(self, full_name: str) -> List[str]:
        return []

    def get_file_content(self, full_name: str, path: str) -> str:
        return ""

    def check_ci_status(self, full_name: str) -> str:
        return "SUCCESS"


class MockFunnel(IPruningFunnel):
    def __init__(self) -> None:
        self.stage1_received: Optional[List[CandidateRepo]] = None
        self.stage2_received: Optional[List[CandidateRepo]] = None
        self.stage3_received: Optional[List[CandidateRepo]] = None
        self.last_allow_copyleft: Optional[bool] = None

    def prune_stage1_metadata(
        self, repos: List[CandidateRepo], allow_copyleft: bool = False
    ) -> List[CandidateRepo]:
        self.stage1_received = repos
        self.last_allow_copyleft = allow_copyleft
        return repos

    def prune_stage2_heuristics(
        self, repos: List[CandidateRepo], client: IGitHubClient
    ) -> List[CandidateRepo]:
        self.stage2_received = repos
        return repos

    def prune_stage3_deep(
        self, repos: List[CandidateRepo], host: HostProfile
    ) -> List[CandidateRepo]:
        self.stage3_received = repos
        return repos


class MockScoringEngine(IScoringEngine):
    def score_candidate(self, repo: CandidateRepo, host: HostProfile) -> EvaluationScore:
        score_val = 80.0 if repo.name == "repo1" else 90.0
        return EvaluationScore(
            repo=repo,
            architecture_score=score_val,
            cleanliness_score=score_val,
            community_score=score_val,
            popularity_score=score_val,
            hygiene_score=score_val,
            final_score=score_val,
            strengths=["Modular"],
            weaknesses=[],
            vibe_analogy="Clean tool",
        )


class MockRepository(IScoutRepository):
    def __init__(self) -> None:
        self.saved_runs: List[Any] = []

    def save_evaluation_run(self, run: Any) -> str:
        self.saved_runs.append(run)
        return "mock-run-id-12345"

    def get_evaluation_history(self, limit: int = 10):
        return []


class MockPresenter(IUIPresenter):
    def render_evaluation_report(
        self, scores: List[EvaluationScore], host_profile: Optional[HostProfile] = None
    ) -> str:
        if not scores:
            return "No candidates evaluated report."
        return f"# Report for {len(scores)} candidates"

    def render_risk_confirmation(self, repo: CandidateRepo, risks: List[str]) -> str:
        return "Risk prompt"


@pytest.fixture
def sample_candidates() -> List[CandidateRepo]:
    return [
        CandidateRepo(
            name="repo1",
            full_name="org/repo1",
            stars=100,
            forks=20,
            license_spdx="MIT",
        ),
        CandidateRepo(
            name="repo2",
            full_name="org/repo2",
            stars=200,
            forks=40,
            license_spdx="Apache-2.0",
        ),
    ]


# --- 1. Happy Path Tests ---

def test_scout_orchestrator_happy_path(sample_candidates: List[CandidateRepo]):
    """Verify complete orchestrator flow from profiling to markdown presentation."""
    profiler = MockProfiler()
    client = MockGitHubClient(sample_candidates)
    funnel = MockFunnel()
    scoring = MockScoringEngine()
    repo = MockRepository()
    presenter = MockPresenter()

    orchestrator = ScoutOrchestrator(
        profiler=profiler,
        github_client=client,
        pruning_funnel=funnel,
        scoring_engine=scoring,
        repository=repo,
        presenter=presenter,
        max_search_limit=10,
        finalist_limit=3,
    )

    result = orchestrator.scout(query="fastapi clean architecture", project_path=".", allow_copyleft=True)

    assert isinstance(result, ScoutResult)
    assert result.run_id == "mock-run-id-12345"
    assert len(result.scores) == 2
    # Verify scores sorted descending by final_score (repo2 has 90.0, repo1 has 80.0)
    assert result.scores[0].repo.name == "repo2"
    assert result.scores[1].repo.name == "repo1"
    assert "# Report for 2 candidates" in result.report
    assert result.host_profile.architecture_type == "Clean Layered Architecture"

    # Verify funnel was called with allow_copyleft
    assert funnel.last_allow_copyleft is True

    # Verify repository received run data
    assert len(repo.saved_runs) == 1
    assert repo.saved_runs[0]["query"] == "fastapi clean architecture"
    assert repo.saved_runs[0]["finalists_count"] == 2


def test_scout_orchestrator_tuple_unpacking(sample_candidates: List[CandidateRepo]):
    """Verify tuple-style unpacking: report, scores = orchestrator.scout(...)."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(sample_candidates),
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
    )

    report, scores = orchestrator.scout(query="test-query")
    assert isinstance(report, str)
    assert isinstance(scores, list)
    assert len(scores) == 2


# --- 2. Edge Case Tests ---

def test_scout_orchestrator_empty_github_search():
    """Verify empty search results return early without failing."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient([]),  # No candidates
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
        presenter=MockPresenter(),
    )

    result = orchestrator.scout(query="nonexistent-library")
    assert result.scores == []
    assert result.run_id is None
    assert "No candidates evaluated report." in result.report


def test_scout_orchestrator_stage1_eliminates_all(sample_candidates: List[CandidateRepo]):
    """Verify pipeline handles Stage 1 funnel eliminating all candidates."""
    funnel = MockFunnel()
    funnel.prune_stage1_metadata = lambda repos, allow_copyleft=False: []  # type: ignore

    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(sample_candidates),
        pruning_funnel=funnel,
        scoring_engine=MockScoringEngine(),
        presenter=MockPresenter(),
    )

    result = orchestrator.scout(query="test")
    assert result.scores == []
    assert result.run_id is None


def test_scout_orchestrator_stage2_eliminates_all(sample_candidates: List[CandidateRepo]):
    """Verify pipeline handles Stage 2 funnel eliminating all candidates."""
    funnel = MockFunnel()
    funnel.prune_stage2_heuristics = lambda repos, client: []  # type: ignore

    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(sample_candidates),
        pruning_funnel=funnel,
        scoring_engine=MockScoringEngine(),
        presenter=MockPresenter(),
    )

    result = orchestrator.scout(query="test")
    assert result.scores == []
    assert result.run_id is None


def test_scout_orchestrator_stage3_eliminates_all(sample_candidates: List[CandidateRepo]):
    """Verify pipeline handles Stage 3 funnel eliminating all candidates."""
    funnel = MockFunnel()
    funnel.prune_stage3_deep = lambda repos, host: []  # type: ignore

    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(sample_candidates),
        pruning_funnel=funnel,
        scoring_engine=MockScoringEngine(),
        presenter=MockPresenter(),
    )

    result = orchestrator.scout(query="test")
    assert result.scores == []
    assert result.run_id is None


def test_scout_orchestrator_without_repository(sample_candidates: List[CandidateRepo]):
    """Verify persistence is skipped cleanly when repository is None."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(sample_candidates),
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
        repository=None,
    )

    result = orchestrator.scout(query="test")
    assert result.run_id is None
    assert len(result.scores) == 2


def test_scout_orchestrator_without_presenter(sample_candidates: List[CandidateRepo]):
    """Verify default report string generated when presenter is None."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(sample_candidates),
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
        presenter=None,
    )

    result = orchestrator.scout(query="test")
    assert "# OSS Candidate Evaluation Report" in result.report
    assert "Evaluated 2 finalists." in result.report


def test_scout_orchestrator_finalist_limit_capping(sample_candidates: List[CandidateRepo]):
    """Verify finalists are capped to finalist_limit."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(sample_candidates),
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
        finalist_limit=1,
    )

    result = orchestrator.scout(query="test")
    assert len(result.scores) == 1


# --- 3. Failure State Tests ---

def test_scout_orchestrator_missing_required_dependencies():
    """Verify constructor raises ValueError if any required contract is None."""
    profiler = MockProfiler()
    client = MockGitHubClient()
    funnel = MockFunnel()
    scoring = MockScoringEngine()

    with pytest.raises(ValueError, match="profiler must be an instance"):
        ScoutOrchestrator(None, client, funnel, scoring)  # type: ignore

    with pytest.raises(ValueError, match="github_client must be an instance"):
        ScoutOrchestrator(profiler, None, funnel, scoring)  # type: ignore

    with pytest.raises(ValueError, match="pruning_funnel must be an instance"):
        ScoutOrchestrator(profiler, client, None, scoring)  # type: ignore

    with pytest.raises(ValueError, match="scoring_engine must be an instance"):
        ScoutOrchestrator(profiler, client, funnel, None)  # type: ignore


def test_scout_orchestrator_invalid_limits():
    """Verify constructor raises ValueError if limits are non-positive."""
    profiler = MockProfiler()
    client = MockGitHubClient()
    funnel = MockFunnel()
    scoring = MockScoringEngine()

    with pytest.raises(ValueError, match="max_search_limit must be a positive integer"):
        ScoutOrchestrator(profiler, client, funnel, scoring, max_search_limit=0)

    with pytest.raises(ValueError, match="finalist_limit must be a positive integer"):
        ScoutOrchestrator(profiler, client, funnel, scoring, finalist_limit=-1)


def test_scout_orchestrator_invalid_query():
    """Verify scout raises ValueError on empty or invalid query."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(),
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
    )

    with pytest.raises(ValueError, match="query must be a non-empty string"):
        orchestrator.scout(query="")

    with pytest.raises(ValueError, match="query must be a non-empty string"):
        orchestrator.scout(query="   ")

    with pytest.raises(ValueError, match="query must be a non-empty string"):
        orchestrator.scout(query=None)  # type: ignore


def test_scout_orchestrator_invalid_project_path():
    """Verify scout raises ValueError on invalid project_path."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(),
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
    )

    with pytest.raises(ValueError, match="project_path must be a string"):
        orchestrator.scout(query="valid", project_path=None)  # type: ignore


def test_scout_orchestrator_invalid_allow_copyleft():
    """Verify scout raises ValueError on non-bool allow_copyleft."""
    orchestrator = ScoutOrchestrator(
        profiler=MockProfiler(),
        github_client=MockGitHubClient(),
        pruning_funnel=MockFunnel(),
        scoring_engine=MockScoringEngine(),
    )

    with pytest.raises(ValueError, match="allow_copyleft must be a boolean"):
        orchestrator.scout(query="valid", allow_copyleft="true")  # type: ignore
