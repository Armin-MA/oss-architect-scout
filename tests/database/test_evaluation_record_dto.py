"""Unit tests for EvaluationRecordDTO (TASK-023)."""

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
import pytest

from src.database.dto.evaluation_record_dto import EvaluationRecordDTO


def test_happy_path_instantiation() -> None:
    """Verify expected deterministic behavior with valid input data."""
    now = datetime(2026, 10, 16, 20, 0, 0, tzinfo=timezone.utc)
    dto = EvaluationRecordDTO(
        run_id="run-12345",
        repo_full_name="fastapi/fastapi",
        stars=75000,
        license_type="MIT",
        final_score=94.5,
        created_at=now,
    )

    assert dto.run_id == "run-12345"
    assert dto.repo_full_name == "fastapi/fastapi"
    assert dto.stars == 75000
    assert dto.license_type == "MIT"
    assert dto.final_score == 94.5
    assert dto.created_at == now


def test_happy_path_to_dict_and_from_dict() -> None:
    """Verify bidirectional conversion between DTO and dictionary."""
    dto = EvaluationRecordDTO(
        run_id="run-abc",
        repo_full_name="psf/requests",
        stars=50000,
        license_type="Apache-2.0",
        final_score=88.2,
        created_at="2026-10-16T20:00:00",
    )

    d = dto.to_dict()
    assert d["run_id"] == "run-abc"
    assert d["repo_full_name"] == "psf/requests"
    assert d["stars"] == 50000
    assert d["license_type"] == "Apache-2.0"
    assert d["final_score"] == 88.2
    assert d["created_at"] == "2026-10-16T20:00:00"

    restored = EvaluationRecordDTO.from_dict(d)
    assert restored == dto


def test_happy_path_immutability() -> None:
    """Verify that dataclass is frozen and prevents mutation."""
    dto = EvaluationRecordDTO(
        run_id="run-immutable",
        repo_full_name="org/repo",
        stars=100,
        license_type="MIT",
        final_score=50.0,
    )

    with pytest.raises(FrozenInstanceError):
        dto.stars = 200  # type: ignore

    with pytest.raises(FrozenInstanceError):
        dto.run_id = "new-id"  # type: ignore


def test_edge_case_zero_stars_and_extreme_scores() -> None:
    """Verify proper boundary condition handling (zero stars, 0.0 and 100.0 score)."""
    dto_min = EvaluationRecordDTO(
        run_id="run-min",
        repo_full_name="newbie/project",
        stars=0,
        license_type="None",
        final_score=0.0,
        created_at=None,
    )
    assert dto_min.stars == 0
    assert dto_min.final_score == 0.0
    assert dto_min.created_at is None

    dto_max = EvaluationRecordDTO(
        run_id="run-max",
        repo_full_name="legendary/framework",
        stars=500000,
        license_type="BSD-3-Clause",
        final_score=100.0,
    )
    assert dto_max.final_score == 100.0
    assert dto_max.stars == 500000


def test_edge_case_unicode_and_date_handling() -> None:
    """Verify DTO handles unicode repo names and ISO string dates."""
    now = datetime.now()
    dto = EvaluationRecordDTO(
        run_id="run-unicode-🚀",
        repo_full_name="tést/repo-ñame_✨",
        stars=10,
        license_type="GPL-3.0-only",
        final_score=72.0,
        created_at=now,
    )

    d = dto.to_dict()
    assert d["run_id"] == "run-unicode-🚀"
    assert d["created_at"] == now.isoformat()


@pytest.mark.parametrize(
    "invalid_kwargs,error_match",
    [
        ({"run_id": "", "repo_full_name": "a/b", "stars": 1, "license_type": "MIT", "final_score": 10.0}, "run_id must be a non-empty string"),
        ({"run_id": None, "repo_full_name": "a/b", "stars": 1, "license_type": "MIT", "final_score": 10.0}, "run_id must be a non-empty string"),
        ({"run_id": "r1", "repo_full_name": "", "stars": 1, "license_type": "MIT", "final_score": 10.0}, "repo_full_name must be a non-empty string"),
        ({"run_id": "r1", "repo_full_name": None, "stars": 1, "license_type": "MIT", "final_score": 10.0}, "repo_full_name must be a non-empty string"),
        ({"run_id": "r1", "repo_full_name": "a/b", "stars": -1, "license_type": "MIT", "final_score": 10.0}, "stars must be a non-negative integer"),
        ({"run_id": "r1", "repo_full_name": "a/b", "stars": "five", "license_type": "MIT", "final_score": 10.0}, "stars must be a non-negative integer"),
        ({"run_id": "r1", "repo_full_name": "a/b", "stars": 1, "license_type": 123, "final_score": 10.0}, "license_type must be a string"),
        ({"run_id": "r1", "repo_full_name": "a/b", "stars": 1, "license_type": "MIT", "final_score": -0.1}, "final_score must be between 0.0 and 100.0"),
        ({"run_id": "r1", "repo_full_name": "a/b", "stars": 1, "license_type": "MIT", "final_score": 100.1}, "final_score must be between 0.0 and 100.0"),
        ({"run_id": "r1", "repo_full_name": "a/b", "stars": 1, "license_type": "MIT", "final_score": "high"}, "final_score must be a numeric value"),
    ],
)
def test_failure_state_validation(invalid_kwargs, error_match) -> None:
    """Verify explicit exception raising on invalid inputs."""
    with pytest.raises(ValueError, match=error_match):
        EvaluationRecordDTO(**invalid_kwargs)
