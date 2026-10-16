"""Dependency Injection (IoC) Container for OSS Architect Scout."""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

from src.config.settings import Settings, get_settings
from src.contracts.i_architecture_profiler import IArchitectureProfiler
from src.contracts.i_github_client import IGitHubClient
from src.contracts.i_pruning_funnel import IPruningFunnel
from src.contracts.i_scoring_engine import IScoringEngine
from src.contracts.i_scout_repository import IScoutRepository
from src.contracts.i_ui_presenter import IUIPresenter
from src.database.repositories.mysql_scout_repository import MySQLScoutRepository
from src.entities.candidate_repo import CandidateRepo
from src.entities.evaluation_score import EvaluationScore
from src.entities.host_profile import HostProfile
from src.ui.markdown_presenter import MarkdownPresenter
from src.utils.github_api_client import GitHubAPIClient

T = TypeVar("T")


class DefaultArchitectureProfiler(IArchitectureProfiler):
    """Default baseline host architecture profiler."""

    def profile_host(self, project_path: str) -> HostProfile:
        return HostProfile(
            architecture_type="Modular Architecture",
            active_skills=["default-profiler"],
            banned_libraries=[],
            required_layers=["contracts", "entities", "mechanics", "database", "ui", "core"],
            strict_typing=True,
        )


class DefaultPruningFunnel(IPruningFunnel):
    """Default baseline multi-stage pruning funnel."""

    def prune_stage1_metadata(self, repos: list[CandidateRepo]) -> list[CandidateRepo]:
        # Filter out repos with invalid or missing names
        return [r for r in repos if r.name and r.full_name]

    def prune_stage2_heuristics(
        self, repos: list[CandidateRepo], client: IGitHubClient
    ) -> list[CandidateRepo]:
        # Filter out repos with negative or invalid star/fork counts
        return [r for r in repos if r.stars >= 0]

    def prune_stage3_deep(
        self, repos: list[CandidateRepo], host: HostProfile
    ) -> list[CandidateRepo]:
        # Shortlist top candidates up to 3
        return repos[:3]


class DefaultScoringEngine(IScoringEngine):
    """Default baseline candidate scoring engine."""

    def score_candidate(self, repo: CandidateRepo, host: HostProfile) -> EvaluationScore:
        arch = 85.0
        clean = 80.0
        comm = min(100.0, max(0.0, 50.0 + (repo.stars / 100.0)))
        pop = min(100.0, max(0.0, 40.0 + (repo.stars / 50.0)))
        hyg = 75.0
        final = round(0.25 * arch + 0.25 * clean + 0.25 * comm + 0.15 * pop + 0.10 * hyg, 2)
        return EvaluationScore(
            repo=repo,
            architecture_score=arch,
            cleanliness_score=clean,
            community_score=comm,
            popularity_score=pop,
            hygiene_score=hyg,
            final_score=final,
            strengths=[f"Popularity: {repo.stars} stars", f"License: {repo.license_spdx or 'Unknown'}"],
            weaknesses=[],
            vibe_analogy="Modular utility candidate",
        )


class Container:
    """IoC Dependency Injection Container wiring contracts to concrete implementations."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Initialize the container with settings and default service registrations.

        Args:
            settings: Optional Settings instance. Defaults to get_settings().

        Raises:
            ValueError: If settings is provided but not an instance of Settings.
        """
        if settings is not None and not isinstance(settings, Settings):
            raise ValueError("settings must be an instance of Settings")

        self._settings: Settings = settings if settings is not None else get_settings()
        self._services: Dict[Type[Any], Union[Any, Callable[['Container'], Any]]] = {}
        self._singletons: Dict[Type[Any], Any] = {}

        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default contract implementations."""
        self.register_instance(Settings, self._settings)

        # GitHub Client
        self.register_factory(
            IGitHubClient,
            lambda c: GitHubAPIClient(
                base_url=c.settings.github_api_url,
                timeout=float(c.settings.timeout),
            ),
        )

        # MySQL Repository
        self.register_factory(
            IScoutRepository,
            lambda c: MySQLScoutRepository(db_connection_params=c.settings.db_config),
        )

        # UI Presenter
        self.register_factory(IUIPresenter, lambda _: MarkdownPresenter())

        # Profiler, Funnel, Scoring defaults
        self.register_factory(IArchitectureProfiler, lambda _: DefaultArchitectureProfiler())
        self.register_factory(IPruningFunnel, lambda _: DefaultPruningFunnel())
        self.register_factory(IScoringEngine, lambda _: DefaultScoringEngine())

    def register(
        self,
        contract: Type[T],
        implementation: Union[T, Callable[['Container'], T]],
    ) -> None:
        """Register an instance or factory callable for a contract."""
        if contract is None:
            raise ValueError("contract type cannot be None")
        self._services[contract] = implementation
        # Invalidate cached singleton if re-registered
        self._singletons.pop(contract, None)

    def register_instance(self, contract: Type[T], instance: T) -> None:
        """Register a pre-constructed singleton instance for a contract."""
        if contract is None:
            raise ValueError("contract type cannot be None")
        if instance is None:
            raise ValueError("instance cannot be None")
        self._services[contract] = instance
        self._singletons[contract] = instance

    def register_factory(
        self,
        contract: Type[T],
        factory: Callable[['Container'], T],
    ) -> None:
        """Register a factory callable for a contract."""
        if contract is None:
            raise ValueError("contract type cannot be None")
        if not callable(factory):
            raise ValueError("factory must be callable")
        self._services[contract] = factory
        self._singletons.pop(contract, None)

    def resolve(self, contract: Type[T]) -> T:
        """Resolve a registered contract to its concrete instance.

        Args:
            contract: The interface or class type to resolve.

        Returns:
            The resolved instance.

        Raises:
            RuntimeError: If the contract is not registered.
        """
        if contract is None:
            raise RuntimeError("Cannot resolve None contract")

        if contract in self._singletons:
            return self._singletons[contract]  # type: ignore

        if contract not in self._services:
            name = getattr(contract, "__name__", str(contract))
            raise RuntimeError(f"Required dependency could not be resolved: '{name}'")

        entry = self._services[contract]
        if callable(entry) and not isinstance(entry, type):
            resolved = entry(self)
            self._singletons[contract] = resolved
            return resolved  # type: ignore

        self._singletons[contract] = entry
        return entry  # type: ignore

    @property
    def settings(self) -> Settings:
        """Return resolved Settings instance."""
        return self.resolve(Settings)

    @property
    def github_client(self) -> IGitHubClient:
        """Return resolved IGitHubClient instance."""
        return self.resolve(IGitHubClient)

    @property
    def repository(self) -> IScoutRepository:
        """Return resolved IScoutRepository instance."""
        return self.resolve(IScoutRepository)

    @property
    def ui_presenter(self) -> IUIPresenter:
        """Return resolved IUIPresenter instance."""
        return self.resolve(IUIPresenter)

    @property
    def profiler(self) -> IArchitectureProfiler:
        """Return resolved IArchitectureProfiler instance."""
        return self.resolve(IArchitectureProfiler)

    @property
    def pruning_funnel(self) -> IPruningFunnel:
        """Return resolved IPruningFunnel instance."""
        return self.resolve(IPruningFunnel)

    @property
    def scoring_engine(self) -> IScoringEngine:
        """Return resolved IScoringEngine instance."""
        return self.resolve(IScoringEngine)

    def create_orchestrator(self) -> Any:
        """Construct and return a ScoutOrchestrator instance wired with container dependencies."""
        from src.core.scout_orchestrator import ScoutOrchestrator

        return ScoutOrchestrator(
            profiler=self.profiler,
            github_client=self.github_client,
            pruning_funnel=self.pruning_funnel,
            scoring_engine=self.scoring_engine,
            repository=self.repository,
            presenter=self.ui_presenter,
            max_search_limit=self.settings.max_search_limit,
            finalist_limit=self.settings.finalist_limit,
        )
