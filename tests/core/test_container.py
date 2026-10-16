"""Unit tests for Dependency Injection Container (TASK-027)."""
import pytest

from src.config.settings import Settings
from src.contracts.i_architecture_profiler import IArchitectureProfiler
from src.contracts.i_github_client import IGitHubClient
from src.contracts.i_pruning_funnel import IPruningFunnel
from src.contracts.i_scoring_engine import IScoringEngine
from src.contracts.i_scout_repository import IScoutRepository
from src.contracts.i_ui_presenter import IUIPresenter
from src.core.container import Container
from src.core.scout_orchestrator import ScoutOrchestrator


class MockProfiler(IArchitectureProfiler):
    def profile_host(self, project_path: str):
        pass


class MockFunnel(IPruningFunnel):
    def prune_stage1_metadata(self, repos):
        return repos

    def prune_stage2_heuristics(self, repos, client):
        return repos

    def prune_stage3_deep(self, repos, host):
        return repos


# --- 1. Happy Path Tests ---

def test_container_default_resolution():
    """Verify container initializes and resolves standard default contracts."""
    container = Container()

    # Settings
    assert isinstance(container.settings, Settings)
    assert container.resolve(Settings) is container.settings

    # Contracts
    assert isinstance(container.github_client, IGitHubClient)
    assert isinstance(container.repository, IScoutRepository)
    assert isinstance(container.ui_presenter, IUIPresenter)
    assert isinstance(container.profiler, IArchitectureProfiler)
    assert isinstance(container.pruning_funnel, IPruningFunnel)
    assert isinstance(container.scoring_engine, IScoringEngine)


def test_container_custom_registration_instance():
    """Verify registering a custom mock instance overrides default."""
    container = Container()
    custom_profiler = MockProfiler()

    container.register_instance(IArchitectureProfiler, custom_profiler)
    assert container.resolve(IArchitectureProfiler) is custom_profiler
    assert container.profiler is custom_profiler


def test_container_custom_registration_factory():
    """Verify registering a custom factory function."""
    container = Container()
    invoked = False

    def funnel_factory(c: Container) -> IPruningFunnel:
        nonlocal invoked
        invoked = True
        return MockFunnel()

    container.register_factory(IPruningFunnel, funnel_factory)
    resolved = container.resolve(IPruningFunnel)

    assert invoked is True
    assert isinstance(resolved, MockFunnel)
    # Subsequent resolve returns cached instance
    assert container.resolve(IPruningFunnel) is resolved


def test_container_create_orchestrator():
    """Verify container wires dependencies and creates ScoutOrchestrator."""
    container = Container()
    orchestrator = container.create_orchestrator()

    assert isinstance(orchestrator, ScoutOrchestrator)
    assert orchestrator.profiler is container.profiler
    assert orchestrator.github_client is container.github_client
    assert orchestrator.pruning_funnel is container.pruning_funnel
    assert orchestrator.scoring_engine is container.scoring_engine
    assert orchestrator.repository is container.repository
    assert orchestrator.presenter is container.ui_presenter


# --- 2. Edge Case Tests ---

def test_container_custom_settings():
    """Verify container initialized with custom Settings instance."""
    custom_settings = Settings(
        github_api_url="https://custom.api.github.com",
        timeout=45,
        max_search_limit=25,
        finalist_limit=2,
    )
    container = Container(settings=custom_settings)

    assert container.settings.github_api_url == "https://custom.api.github.com"
    assert container.settings.timeout == 45
    assert container.settings.max_search_limit == 25
    assert container.settings.finalist_limit == 2


def test_container_overwrite_registration():
    """Verify re-registering an existing contract safely invalidates previous singleton."""
    container = Container()
    mock1 = MockProfiler()
    mock2 = MockProfiler()

    container.register_instance(IArchitectureProfiler, mock1)
    assert container.resolve(IArchitectureProfiler) is mock1

    container.register_instance(IArchitectureProfiler, mock2)
    assert container.resolve(IArchitectureProfiler) is mock2


# --- 3. Failure State Tests ---

def test_container_invalid_settings_raises():
    """Verify passing non-Settings object raises ValueError."""
    with pytest.raises(ValueError, match="settings must be an instance of Settings"):
        Container(settings="not-a-settings")  # type: ignore


def test_container_unresolved_contract_raises():
    """Verify resolving an unregistered type raises RuntimeError."""
    container = Container()

    class UnregisteredContract:
        pass

    with pytest.raises(RuntimeError, match="Required dependency could not be resolved"):
        container.resolve(UnregisteredContract)


def test_container_resolve_none_raises():
    """Verify resolving None raises RuntimeError."""
    container = Container()
    with pytest.raises(RuntimeError, match="Cannot resolve None contract"):
        container.resolve(None)  # type: ignore


def test_container_register_none_contract_raises():
    """Verify register_instance with None contract raises ValueError."""
    container = Container()
    with pytest.raises(ValueError, match="contract type cannot be None"):
        container.register_instance(None, MockProfiler())  # type: ignore


def test_container_register_none_instance_raises():
    """Verify register_instance with None instance raises ValueError."""
    container = Container()
    with pytest.raises(ValueError, match="instance cannot be None"):
        container.register_instance(IArchitectureProfiler, None)  # type: ignore


def test_container_register_invalid_factory_raises():
    """Verify register_factory with non-callable raises ValueError."""
    container = Container()
    with pytest.raises(ValueError, match="factory must be callable"):
        container.register_factory(IArchitectureProfiler, "not-a-callable")  # type: ignore
