"""Unit tests for MarkdownPresenter (TASK-026)."""
from typing import List
import pytest

from src.contracts.i_ui_presenter import IUIPresenter
from src.entities.candidate_repo import CandidateRepo
from src.entities.evaluation_score import EvaluationScore
from src.entities.host_profile import HostProfile
from src.ui.markdown_presenter import MarkdownPresenter


@pytest.fixture
def sample_repos() -> List[CandidateRepo]:
    return [
        CandidateRepo(
            name="fastapi-clean-template",
            full_name="example/fastapi-clean-template",
            stars=1200,
            forks=340,
            license_spdx="MIT",
            open_issues=12,
            description="Production ready clean architecture template",
        ),
        CandidateRepo(
            name="django-starter",
            full_name="example/django-starter",
            stars=800,
            forks=210,
            license_spdx="Apache-2.0",
            open_issues=5,
            description="Batteries-included web framework starter",
        ),
    ]


@pytest.fixture
def sample_scores(sample_repos: List[CandidateRepo]) -> List[EvaluationScore]:
    return [
        EvaluationScore(
            repo=sample_repos[0],
            architecture_score=92.0,
            cleanliness_score=88.5,
            community_score=85.0,
            popularity_score=75.0,
            hygiene_score=90.0,
            final_score=87.2,
            strengths=["Strict layer decoupling", "Comprehensive test suite"],
            weaknesses=["Few active maintainers"],
            vibe_analogy="Surgical instrument for modern microservices",
        ),
        EvaluationScore(
            repo=sample_repos[1],
            architecture_score=80.0,
            cleanliness_score=78.0,
            community_score=90.0,
            popularity_score=82.0,
            hygiene_score=70.0,
            final_score=80.4,
            strengths=["High community adoption"],
            weaknesses=["Tight ORM coupling"],
            vibe_analogy="Swiss army knife with heavy baggage",
        ),
    ]


@pytest.fixture
def sample_host_profile() -> HostProfile:
    return HostProfile(
        architecture_type="Strict Layered Architecture",
        active_skills=["interactive-architect-gatekeeper", "test-driven-development"],
        banned_libraries=["sqlalchemy-raw", "django"],
        required_layers=["contracts", "entities", "mechanics", "database", "ui"],
        strict_typing=True,
    )


# --- 1. Happy Path Tests ---

def test_markdown_presenter_implements_interface():
    """Verify MarkdownPresenter properly implements IUIPresenter contract."""
    presenter = MarkdownPresenter()
    assert isinstance(presenter, IUIPresenter)


def test_markdown_presenter_renders_report_happy_path(
    sample_scores: List[EvaluationScore], sample_host_profile: HostProfile
):
    """Verify full markdown report generation with badges, mermaid, table, and details."""
    presenter = MarkdownPresenter()
    report = presenter.render_evaluation_report(sample_scores, sample_host_profile)

    # Header and structure
    assert "# OSS Candidate Evaluation Report" in report

    # Shields.io badges
    assert "https://img.shields.io/badge/" in report
    assert "Top_Recommendation" in report or "Top_Recommendation" in report.replace(" ", "_")
    assert "Final_Score" in report or "Final_Score" in report.replace(" ", "_")

    # Host architecture section
    assert "Strict Layered Architecture" in report
    assert "interactive-architect-gatekeeper" in report

    # Mermaid diagram
    assert "```mermaid" in report
    assert "flowchart TD" in report
    assert "Top Recommended: example/fastapi-clean-template" in report

    # Comparison matrix table
    assert "Candidate Comparison Matrix" in report
    assert "| Rank | Repository | Final Score |" in report
    assert "example/fastapi-clean-template" in report
    assert "example/django-starter" in report

    # Details accordion
    assert "<details>" in report
    assert "</details>" in report
    assert "Surgical instrument for modern microservices" in report
    assert "Strict layer decoupling" in report
    assert "Tight ORM coupling" in report


def test_markdown_presenter_risk_confirmation_with_risks(sample_repos: List[CandidateRepo]):
    """Verify risk confirmation prompt renders warning block with risks."""
    presenter = MarkdownPresenter()
    risks = [
        "Incompatible copyleft license (GPL-3.0-only)",
        "Critical CVE-2024-9999 reported with CVSS 9.8",
    ]
    prompt = presenter.render_risk_confirmation(sample_repos[0], risks)

    assert "> [!WARNING]" in prompt
    assert "CRITICAL RISK CONFIRMATION REQUIRED" in prompt
    assert sample_repos[0].full_name in prompt
    assert "Incompatible copyleft license (GPL-3.0-only)" in prompt
    assert "Critical CVE-2024-9999" in prompt
    assert "Zero Confirmation Bias" in prompt


# --- 2. Edge Case Tests ---

def test_markdown_presenter_empty_scores():
    """Verify handling of empty candidate scores list."""
    presenter = MarkdownPresenter()
    report = presenter.render_evaluation_report([])
    assert "# OSS Candidate Evaluation Report" in report
    assert "No candidate repositories were found or evaluated." in report


def test_markdown_presenter_without_host_profile(sample_scores: List[EvaluationScore]):
    """Verify report rendering when host_profile is omitted."""
    presenter = MarkdownPresenter()
    report = presenter.render_evaluation_report(sample_scores)
    assert "# OSS Candidate Evaluation Report" in report
    assert "Candidate Comparison Matrix" in report
    assert "Target Architecture Constraints" not in report


def test_markdown_presenter_minimal_score_details(sample_repos: List[CandidateRepo]):
    """Verify candidate with empty strengths, weaknesses, and vibe analogy."""
    presenter = MarkdownPresenter()
    minimal_score = EvaluationScore(
        repo=sample_repos[0],
        architecture_score=50.0,
        cleanliness_score=50.0,
        community_score=50.0,
        popularity_score=50.0,
        hygiene_score=50.0,
        final_score=50.0,
        strengths=[],
        weaknesses=[],
        vibe_analogy="",
    )
    report = presenter.render_evaluation_report([minimal_score])
    assert "No specific strengths highlighted." in report
    assert "No notable weaknesses recorded." in report
    assert "<details>" in report


def test_markdown_presenter_risk_confirmation_no_risks(sample_repos: List[CandidateRepo]):
    """Verify risk confirmation when risks list is empty."""
    presenter = MarkdownPresenter()
    prompt = presenter.render_risk_confirmation(sample_repos[0], [])
    assert "No critical risks identified" in prompt
    assert "safe to adopt" in prompt


# --- 3. Failure State Tests ---

def test_markdown_presenter_none_scores_raises():
    """Verify render_evaluation_report raises ValueError if scores is None."""
    presenter = MarkdownPresenter()
    with pytest.raises(ValueError, match="scores list cannot be None"):
        presenter.render_evaluation_report(None)  # type: ignore


def test_markdown_presenter_invalid_score_elements_raises():
    """Verify render_evaluation_report raises ValueError on non-EvaluationScore items."""
    presenter = MarkdownPresenter()
    with pytest.raises(ValueError, match="not an EvaluationScore instance"):
        presenter.render_evaluation_report(["not_a_score"])  # type: ignore


def test_markdown_presenter_risk_confirmation_none_repo_raises():
    """Verify render_risk_confirmation raises ValueError when repo is None."""
    presenter = MarkdownPresenter()
    with pytest.raises(ValueError, match="repo must be an instance of CandidateRepo"):
        presenter.render_risk_confirmation(None, ["risk"])  # type: ignore


def test_markdown_presenter_risk_confirmation_invalid_risks_raises(sample_repos: List[CandidateRepo]):
    """Verify render_risk_confirmation raises ValueError when risks is not a list."""
    presenter = MarkdownPresenter()
    with pytest.raises(ValueError, match="risks must be a list"):
        presenter.render_risk_confirmation(sample_repos[0], "not-a-list")  # type: ignore
