"""Abstract contracts package defining boundary interfaces."""

from src.contracts.i_github_client import IGitHubClient
from src.contracts.i_architecture_profiler import IArchitectureProfiler
from src.contracts.i_pruning_funnel import IPruningFunnel
from src.contracts.i_scoring_engine import IScoringEngine
from src.contracts.i_scout_repository import IScoutRepository
from src.contracts.i_ui_presenter import IUIPresenter

__all__ = [
    "IGitHubClient",
    "IArchitectureProfiler",
    "IPruningFunnel",
    "IScoringEngine",
    "IScoutRepository",
    "IUIPresenter",
]
