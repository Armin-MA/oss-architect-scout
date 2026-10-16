"""Core application orchestrator coordinating end-to-end scouting workflow."""
from __future__ import annotations

from dataclasses import dataclass
import inspect
from typing import Any, Iterator, List, Optional, Tuple, Union

from src.contracts.i_architecture_profiler import IArchitectureProfiler
from src.contracts.i_github_client import IGitHubClient
from src.contracts.i_pruning_funnel import IPruningFunnel
from src.contracts.i_scoring_engine import IScoringEngine
from src.contracts.i_scout_repository import IScoutRepository
from src.contracts.i_ui_presenter import IUIPresenter
from src.entities.candidate_repo import CandidateRepo
from src.entities.evaluation_score import EvaluationScore
from src.entities.host_profile import HostProfile


@dataclass
class ScoutResult:
    """Encapsulates the deterministic outcome of a scout execution."""

    report: str
    scores: List[EvaluationScore]
    host_profile: HostProfile
    run_id: Optional[str] = None

    def __iter__(self) -> Iterator[Union[str, List[EvaluationScore]]]:
        """Support tuple-style unpacking: report, scores = orchestrator.scout(...)."""
        yield self.report
        yield self.scores


class ScoutOrchestrator:
    """Coordinates end-to-end flow: profiling -> search -> 3-stage funnel -> scoring -> persistence -> report."""

    def __init__(
        self,
        profiler: IArchitectureProfiler,
        github_client: IGitHubClient,
        pruning_funnel: IPruningFunnel,
        scoring_engine: IScoringEngine,
        repository: Optional[IScoutRepository] = None,
        presenter: Optional[IUIPresenter] = None,
        max_search_limit: int = 50,
        finalist_limit: int = 3,
    ) -> None:
        """Initialize orchestrator with required contracts and optional persistence/presentation.

        Args:
            profiler: Host project architecture profiler contract.
            github_client: GitHub API client contract.
            pruning_funnel: 3-stage pruning funnel contract.
            scoring_engine: 5-dimensional candidate scoring contract.
            repository: Optional persistence repository contract.
            presenter: Optional UI visual report presenter contract.
            max_search_limit: Maximum search candidates to fetch from GitHub (default 50).
            finalist_limit: Maximum final candidates to present (default 3).

        Raises:
            ValueError: If any required contract is None or limits are non-positive.
        """
        if profiler is None or not isinstance(profiler, IArchitectureProfiler):
            raise ValueError("profiler must be an instance of IArchitectureProfiler")
        if github_client is None or not isinstance(github_client, IGitHubClient):
            raise ValueError("github_client must be an instance of IGitHubClient")
        if pruning_funnel is None or not isinstance(pruning_funnel, IPruningFunnel):
            raise ValueError("pruning_funnel must be an instance of IPruningFunnel")
        if scoring_engine is None or not isinstance(scoring_engine, IScoringEngine):
            raise ValueError("scoring_engine must be an instance of IScoringEngine")

        if repository is not None and not isinstance(repository, IScoutRepository):
            raise ValueError("repository must implement IScoutRepository")
        if presenter is not None and not isinstance(presenter, IUIPresenter):
            raise ValueError("presenter must implement IUIPresenter")

        if not isinstance(max_search_limit, int) or max_search_limit <= 0:
            raise ValueError(f"max_search_limit must be a positive integer, got: {max_search_limit}")
        if not isinstance(finalist_limit, int) or finalist_limit <= 0:
            raise ValueError(f"finalist_limit must be a positive integer, got: {finalist_limit}")

        self.profiler = profiler
        self.github_client = github_client
        self.pruning_funnel = pruning_funnel
        self.scoring_engine = scoring_engine
        self.repository = repository
        self.presenter = presenter
        self.max_search_limit = max_search_limit
        self.finalist_limit = finalist_limit

    def scout(
        self,
        query: str,
        project_path: str = ".",
        allow_copyleft: bool = False,
    ) -> ScoutResult:
        """Execute end-to-end scouting pipeline.

        Args:
            query: Repository search query string.
            project_path: Path to host project to inspect architecture (default: current dir).
            allow_copyleft: If True, permissive policy towards viral copyleft licenses.

        Returns:
            ScoutResult holding visual report string, sorted evaluation scores, and run_id.

        Raises:
            ValueError: If input arguments are missing or invalid.
        """
        if query is None or not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if project_path is None or not isinstance(project_path, str):
            raise ValueError("project_path must be a string")
        if not isinstance(allow_copyleft, bool):
            raise ValueError("allow_copyleft must be a boolean")

        # Step 1: Host Profiling
        host_profile = self.profiler.profile_host(project_path)

        # Step 2: GitHub API Search
        candidates = self.github_client.search_repositories(
            query=query.strip(),
            limit=self.max_search_limit,
        )

        if not candidates:
            report = (
                self.presenter.render_evaluation_report([], host_profile)
                if self.presenter
                else "# OSS Candidate Evaluation Report\n\nNo candidate repositories were found or evaluated."
            )
            return ScoutResult(report=report, scores=[], host_profile=host_profile, run_id=None)

        # Step 3: Funnel Stage 1 - Metadata & Veto Pruning
        sig = inspect.signature(self.pruning_funnel.prune_stage1_metadata)
        if "allow_copyleft" in sig.parameters:
            stage1_candidates = self.pruning_funnel.prune_stage1_metadata(
                candidates, allow_copyleft=allow_copyleft  # type: ignore
            )
        else:
            stage1_candidates = self.pruning_funnel.prune_stage1_metadata(candidates)

        if not stage1_candidates:
            report = (
                self.presenter.render_evaluation_report([], host_profile)
                if self.presenter
                else "# OSS Candidate Evaluation Report\n\nAll candidates eliminated in Stage 1 pruning."
            )
            return ScoutResult(report=report, scores=[], host_profile=host_profile, run_id=None)

        # Step 4: Funnel Stage 2 - Deterministic Heuristics & CI Pruning
        stage2_candidates = self.pruning_funnel.prune_stage2_heuristics(
            stage1_candidates, self.github_client
        )

        if not stage2_candidates:
            report = (
                self.presenter.render_evaluation_report([], host_profile)
                if self.presenter
                else "# OSS Candidate Evaluation Report\n\nAll candidates eliminated in Stage 2 pruning."
            )
            return ScoutResult(report=report, scores=[], host_profile=host_profile, run_id=None)

        # Step 5: Funnel Stage 3 - Deep Architecture & Compatibility Inspection
        stage3_candidates = self.pruning_funnel.prune_stage3_deep(
            stage2_candidates, host_profile
        )

        finalists = stage3_candidates[: self.finalist_limit]
        if not finalists:
            report = (
                self.presenter.render_evaluation_report([], host_profile)
                if self.presenter
                else "# OSS Candidate Evaluation Report\n\nNo finalists qualified after Stage 3 deep inspection."
            )
            return ScoutResult(report=report, scores=[], host_profile=host_profile, run_id=None)

        # Step 6: Multi-Dimensional Scoring
        scores: List[EvaluationScore] = []
        for repo in finalists:
            score = self.scoring_engine.score_candidate(repo, host_profile)
            scores.append(score)

        # Sort descending by final_score
        scores.sort(key=lambda s: s.final_score, reverse=True)

        # Step 7: Database Persistence (Encapsulated)
        run_id: Optional[str] = None
        if self.repository is not None:
            try:
                run_record = {
                    "query": query.strip(),
                    "host_architecture": host_profile.architecture_type,
                    "total_candidates": len(candidates),
                    "finalists_count": len(scores),
                    "finalists": scores,
                }
                run_id = self.repository.save_evaluation_run(run_record)
            except Exception:
                # If MySQL database is unreachable, proceed gracefully without failing the scout run
                run_id = None

        # Step 8: Visual Report Presentation
        if self.presenter is not None:
            report = self.presenter.render_evaluation_report(scores, host_profile)
        else:
            report = f"# OSS Candidate Evaluation Report\n\nEvaluated {len(scores)} finalists."

        return ScoutResult(
            report=report,
            scores=scores,
            host_profile=host_profile,
            run_id=run_id,
        )
