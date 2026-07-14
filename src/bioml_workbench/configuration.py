from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "default.yaml"


@dataclass(frozen=True)
class LoggingConfig:
    """Configuration for application logging."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    to_file: bool = False
    file_path: str = "logs/bioml_workbench.log"


@dataclass(frozen=True)
class AppConfig:
    """Top-level application configuration."""

    app_name: str = "bioml-workbench"
    logging: LoggingConfig = field(default_factory=LoggingConfig)


def _resolve_config_path(config_path: Path | None) -> Path:
    """Resolve a configuration path from either a relative path or the default."""

    if config_path is None:
        return DEFAULT_CONFIG_PATH

    if config_path.is_absolute():
        return config_path

    return (REPO_ROOT / config_path).resolve()


def _resolve_path(value: str, parent: Path) -> str:
    """Resolve a path relative to the config file location when needed."""

    candidate = Path(value)
    if candidate.is_absolute():
        return str(candidate)

    return str((parent / candidate).resolve())


def _load_yaml_data(config_path: Path) -> dict[str, Any]:
    """Load YAML data from disk."""

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    raw_config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw_config, dict):
        raise ValueError("Configuration data must be a YAML mapping.")

    return raw_config


def load_config(config_path: Path | None = None) -> AppConfig:
    """Load application configuration from YAML."""

    resolved_path = _resolve_config_path(config_path)
    raw_config = _load_yaml_data(resolved_path)

    logging_data = raw_config.get("logging", {})
    if not isinstance(logging_data, dict):
        raise ValueError("The logging section must be a mapping.")

    file_path = str(logging_data.get("file_path", "logs/bioml_workbench.log"))
    resolved_log_path = _resolve_path(file_path, resolved_path.parent)

    logging_config = LoggingConfig(
        level=str(logging_data.get("level", "INFO")),
        format=str(
            logging_data.get(
                "format",
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
        ),
        to_file=bool(logging_data.get("to_file", False)),
        file_path=resolved_log_path,
    )

    return AppConfig(
        app_name=str(raw_config.get("app_name", "bioml-workbench")),
        logging=logging_config,
    )
