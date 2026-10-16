"""Unit tests for src/contracts/i_ui_presenter.py."""
import pytest
from typing import Any, List
from src.contracts.i_ui_presenter import IUIPresenter


class DummyUIPresenter(IUIPresenter):
    """Concrete implementation of IUIPresenter for testing."""

    def render_evaluation_report(self, scores: List[Any]) -> str:
        if not scores:
            return "No candidates evaluated."
        lines = ["# Evaluation Report"]
        for s in scores:
            lines.append(f"- Repo: {s.get('name', 'unknown')} Score: {s.get('score', 0)}")
        return "\n".join(lines)

    def render_risk_confirmation(self, repo: Any, risks: List[str]) -> str:
        if not risks:
            return "No risks identified."
        return f"WARNING: Repo {repo.get('name', 'unknown')} has {len(risks)} critical risks."


class IncompleteUIPresenter(IUIPresenter):
    """Subclass without implementing required abstract methods."""

    def render_evaluation_report(self, scores: List[Any]) -> str:
        return ""


def test_i_ui_presenter_happy_path():
    """Verify concrete subclass successfully renders report and risk prompt."""
    presenter = DummyUIPresenter()
    assert isinstance(presenter, IUIPresenter)

    scores = [{"name": "repo1", "score": 90.0}, {"name": "repo2", "score": 80.0}]
    report = presenter.render_evaluation_report(scores)
    assert "# Evaluation Report" in report
    assert "repo1" in report

    risks = ["Critical CVE", "GPL Viral License"]
    prompt = presenter.render_risk_confirmation({"name": "risky-repo"}, risks)
    assert "WARNING" in prompt
    assert "risky-repo" in prompt


def test_i_ui_presenter_edge_cases():
    """Verify boundary handling for empty scores and empty risks."""
    presenter = DummyUIPresenter()
    assert presenter.render_evaluation_report([]) == "No candidates evaluated."
    assert presenter.render_risk_confirmation({"name": "safe-repo"}, []) == "No risks identified."


def test_i_ui_presenter_failure_states():
    """Verify abstract class cannot be instantiated directly or with missing methods."""
    with pytest.raises(TypeError):
        IUIPresenter()  # type: ignore

    with pytest.raises(TypeError):
        IncompleteUIPresenter()  # type: ignore
