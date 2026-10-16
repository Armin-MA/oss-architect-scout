"""Unit tests for src/config/settings.py."""
import os
import pytest
from dataclasses import FrozenInstanceError

from src.config.settings import (
    Settings,
    get_settings,
    GITHUB_API_URL,
    DEFAULT_WEIGHTS,
    TIMEOUT,
    MAX_SEARCH_LIMIT,
    FINALIST_LIMIT,
    DB_CONFIG,
)


def test_settings_happy_path_defaults():
    """Verify expected deterministic default settings behavior and immutability."""
    settings = Settings()

    # Check attribute defaults
    assert settings.github_api_url == "https://api.github.com"
    assert settings.timeout == 30
    assert settings.max_search_limit == 50
    assert settings.finalist_limit == 3
    assert settings.db_config["port"] == 3306
    assert settings.db_config["host"] == "localhost"

    # Check uppercase property aliases
    assert settings.GITHUB_API_URL == settings.github_api_url
    assert settings.DEFAULT_WEIGHTS == settings.default_weights
    assert settings.TIMEOUT == settings.timeout
    assert settings.DB_CONFIG == settings.db_config
    assert settings.MAX_SEARCH_LIMIT == settings.max_search_limit
    assert settings.FINALIST_LIMIT == settings.finalist_limit

    # Verify immutability
    with pytest.raises((FrozenInstanceError, AttributeError)):
        settings.timeout = 100  # type: ignore

    # Verify module constants
    assert GITHUB_API_URL == "https://api.github.com"
    assert TIMEOUT == 30
    assert MAX_SEARCH_LIMIT == 50
    assert FINALIST_LIMIT == 3
    assert "architecture" in DEFAULT_WEIGHTS
    assert DB_CONFIG["port"] == 3306


def test_settings_from_env_happy_path(monkeypatch):
    """Verify Settings.from_env and get_settings read valid environment variables."""
    monkeypatch.setenv("GITHUB_API_URL", "https://api.github.enterprise.local")
    monkeypatch.setenv("TIMEOUT", "45")
    monkeypatch.setenv("DB_HOST", "db.example.com")
    monkeypatch.setenv("DB_PORT", "3307")
    monkeypatch.setenv("DB_USER", "scout_user")
    monkeypatch.setenv("DB_PASSWORD", "secret123")
    monkeypatch.setenv("DB_NAME", "custom_scout_db")

    settings = get_settings()
    assert settings.github_api_url == "https://api.github.enterprise.local"
    assert settings.timeout == 45
    assert settings.db_config["host"] == "db.example.com"
    assert settings.db_config["port"] == 3307
    assert settings.db_config["user"] == "scout_user"
    assert settings.db_config["password"] == "secret123"
    assert settings.db_config["database"] == "custom_scout_db"


def test_settings_edge_cases():
    """Verify boundary condition handling for port, timeout, and weights."""
    # Min port 1
    s_min_port = Settings(db_config={"host": "localhost", "port": 1})
    assert s_min_port.db_config["port"] == 1

    # Max port 65535
    s_max_port = Settings(db_config={"host": "localhost", "port": 65535})
    assert s_max_port.db_config["port"] == 65535

    # Min timeout 1
    s_min_timeout = Settings(timeout=1)
    assert s_min_timeout.timeout == 1

    # Weights summing to 100.0 instead of 1.0
    weights_100 = {
        "architecture": 25.0,
        "cleanliness": 25.0,
        "community": 25.0,
        "popularity": 15.0,
        "hygiene": 10.0,
    }
    s_weights_100 = Settings(default_weights=weights_100)
    assert sum(s_weights_100.default_weights.values()) == 100.0


def test_settings_failure_invalid_values():
    """Verify explicit exception raising on invalid input data."""
    # Invalid URL scheme
    with pytest.raises(ValueError, match="GITHUB_API_URL"):
        Settings(github_api_url="ftp://api.github.com")

    # Empty URL
    with pytest.raises(ValueError, match="GITHUB_API_URL"):
        Settings(github_api_url="")

    # Non-positive timeout
    with pytest.raises(ValueError, match="TIMEOUT"):
        Settings(timeout=0)
    with pytest.raises(ValueError, match="TIMEOUT"):
        Settings(timeout=-5)

    # Invalid port numbers
    with pytest.raises(ValueError, match="DB port"):
        Settings(db_config={"host": "localhost", "port": 0})
    with pytest.raises(ValueError, match="DB port"):
        Settings(db_config={"host": "localhost", "port": 70000})

    # Empty DB host
    with pytest.raises(ValueError, match="DB host"):
        Settings(db_config={"host": "", "port": 3306})

    # Invalid weights sum
    with pytest.raises(ValueError, match="Weights must sum to 1.0 or 100"):
        Settings(default_weights={"a": 0.5, "b": 0.2})

    # Negative weight value
    with pytest.raises(ValueError, match="non-negative"):
        Settings(default_weights={"a": 1.2, "b": -0.2})


def test_settings_failure_from_env(monkeypatch):
    """Verify ValueError when environment variables contain invalid formats."""
    monkeypatch.setenv("TIMEOUT", "not_a_number")
    with pytest.raises(ValueError, match="TIMEOUT environment variable must be an integer"):
        Settings.from_env()

    monkeypatch.setenv("TIMEOUT", "20")
    monkeypatch.setenv("DB_PORT", "invalid_port")
    with pytest.raises(ValueError, match="DB_PORT environment variable must be an integer"):
        Settings.from_env()
