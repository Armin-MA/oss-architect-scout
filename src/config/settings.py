"""Static configuration and environment constants for OSS Architect Scout."""
from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Any, Dict, Mapping

# Default Constants
GITHUB_API_URL: str = "https://api.github.com"

DEFAULT_WEIGHTS: Dict[str, float] = {
    "architecture": 0.25,
    "cleanliness": 0.25,
    "community": 0.25,
    "popularity": 0.15,
    "hygiene": 0.10,
}

TIMEOUT: int = 30
MAX_SEARCH_LIMIT: int = 50
FINALIST_LIMIT: int = 3

DB_CONFIG: Dict[str, Any] = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "oss_architect_scout",
}


@dataclass(frozen=True)
class Settings:
    """Immutable application settings dataclass."""

    github_api_url: str = GITHUB_API_URL
    default_weights: Dict[str, float] = field(default_factory=lambda: dict(DEFAULT_WEIGHTS))
    timeout: int = TIMEOUT
    db_config: Dict[str, Any] = field(default_factory=lambda: dict(DB_CONFIG))
    max_search_limit: int = MAX_SEARCH_LIMIT
    finalist_limit: int = FINALIST_LIMIT

    @property
    def GITHUB_API_URL(self) -> str:
        return self.github_api_url

    @property
    def DEFAULT_WEIGHTS(self) -> Dict[str, float]:
        return self.default_weights

    @property
    def TIMEOUT(self) -> int:
        return self.timeout

    @property
    def DB_CONFIG(self) -> Dict[str, Any]:
        return self.db_config

    @property
    def MAX_SEARCH_LIMIT(self) -> int:
        return self.max_search_limit

    @property
    def FINALIST_LIMIT(self) -> int:
        return self.finalist_limit

    def __post_init__(self) -> None:
        # Validate GITHUB_API_URL
        if not self.github_api_url or not isinstance(self.github_api_url, str):
            raise ValueError("GITHUB_API_URL must be a non-empty string")
        if not (self.github_api_url.startswith("http://") or self.github_api_url.startswith("https://")):
            raise ValueError(f"GITHUB_API_URL must start with http:// or https://: {self.github_api_url}")

        # Validate timeout
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            raise ValueError(f"TIMEOUT must be a positive integer, got: {self.timeout}")

        # Validate limits
        if not isinstance(self.max_search_limit, int) or self.max_search_limit <= 0:
            raise ValueError(f"MAX_SEARCH_LIMIT must be a positive integer, got: {self.max_search_limit}")
        if not isinstance(self.finalist_limit, int) or self.finalist_limit <= 0:
            raise ValueError(f"FINALIST_LIMIT must be a positive integer, got: {self.finalist_limit}")

        # Validate weights
        if not isinstance(self.default_weights, (dict, Mapping)) or not self.default_weights:
            raise ValueError("DEFAULT_WEIGHTS must be a non-empty mapping")
        for k, v in self.default_weights.items():
            if not isinstance(v, (int, float)) or v < 0:
                raise ValueError(f"Weight value for '{k}' must be non-negative, got: {v}")
        weight_sum = sum(self.default_weights.values())
        if not (abs(weight_sum - 1.0) < 1e-4 or abs(weight_sum - 100.0) < 1e-2):
            raise ValueError(f"Weights must sum to 1.0 or 100.0, got: {weight_sum}")

        # Validate DB_CONFIG
        if not isinstance(self.db_config, (dict, Mapping)):
            raise ValueError("DB_CONFIG must be a dictionary")
        port = self.db_config.get("port")
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError(f"DB port must be an integer between 1 and 65535, got: {port}")
        host = self.db_config.get("host")
        if not host or not isinstance(host, str):
            raise ValueError(f"DB host must be a non-empty string, got: {host}")

    @classmethod
    def from_env(cls) -> "Settings":
        """Instantiate Settings by reading system environment variables with fallback defaults."""
        api_url = os.getenv("GITHUB_API_URL", GITHUB_API_URL)

        timeout_raw = os.getenv("TIMEOUT")
        if timeout_raw is not None:
            try:
                timeout = int(timeout_raw)
            except ValueError:
                raise ValueError(f"TIMEOUT environment variable must be an integer, got: '{timeout_raw}'")
        else:
            timeout = TIMEOUT

        db_port_raw = os.getenv("DB_PORT")
        if db_port_raw is not None:
            try:
                db_port = int(db_port_raw)
            except ValueError:
                raise ValueError(f"DB_PORT environment variable must be an integer, got: '{db_port_raw}'")
        else:
            db_port = 3306

        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "")
        db_name = os.getenv("DB_NAME", os.getenv("DB_DATABASE", "oss_architect_scout"))

        custom_db_config = {
            "host": db_host,
            "port": db_port,
            "user": db_user,
            "password": db_password,
            "database": db_name,
        }

        return cls(
            github_api_url=api_url,
            timeout=timeout,
            db_config=custom_db_config,
        )


def get_settings() -> Settings:
    """Return an active Settings instance initialized from environment."""
    return Settings.from_env()
