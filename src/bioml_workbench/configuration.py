from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "default.yaml"
CONFIG_PATH_ENV_VAR = "BIOML_CONFIG_PATH"
ENV_PREFIX = "BIOML_"


@dataclass(frozen=True)
class LoggingConfig:
    """Configuration for application logging."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    to_file: bool = False
    file_path: str = "logs/bioml_workbench.log"


@dataclass(frozen=True)
class DatasetConfig:
    """Configuration for dataset loading and persistence."""

    name: str = "pbmc68k"
    source: str = "pbmc68k"
    raw_data_path: str = "data/raw"
    processed_data_path: str = "data/processed"
    cache_path: str = "data/cache"
    download_url: str = ""
    checksum: str = ""


@dataclass(frozen=True)
class TrainingConfig:
    """Configuration for model training and experiment tracking."""

    random_seed: int = 42
    model_type: str = "random_forest"
    batch_size: int = 128
    learning_rate: float = 0.001
    max_epochs: int = 10
    checkpoint_path: str = "artifacts/checkpoints"
    experiment_name: str = "default"


@dataclass(frozen=True)
class DashboardConfig:
    """Configuration for dashboard runtime behavior."""

    enabled: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    title: str = "BioML Workbench Dashboard"


@dataclass(frozen=True)
class AppConfig:
    """Top-level application configuration."""

    app_name: str = "bioml-workbench"
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _resolve_config_path(config_path: Path | None = None) -> Path:
    """Resolve a configuration path from CLI arguments, env vars, or defaults."""

    if config_path is None:
        env_path = os.getenv(CONFIG_PATH_ENV_VAR)
        if env_path:
            candidate = Path(env_path)
            return (
                candidate
                if candidate.is_absolute()
                else (REPO_ROOT / candidate).resolve()
            )
        return DEFAULT_CONFIG_PATH

    return (
        config_path
        if config_path.is_absolute()
        else (REPO_ROOT / config_path).resolve()
    )


def _load_yaml_data(config_path: Path) -> dict[str, Any]:
    """Load YAML data from disk."""

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    raw_config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw_config, dict):
        raise ValueError("Configuration data must be a YAML mapping.")

    return raw_config


def _parse_env_value(value: str) -> Any:
    """Parse an environment variable string into a native Python value."""

    normalized = value.strip()
    lowered = normalized.lower()
    if lowered in {"true", "yes", "1"}:
        return True
    if lowered in {"false", "no", "0"}:
        return False

    try:
        if "." in normalized:
            return float(normalized)
        return int(normalized)
    except ValueError:
        return normalized


def _set_nested_value(config_data: dict[str, Any], keys: list[str], value: Any) -> None:
    """Set a nested value into a configuration dictionary."""

    current = config_data
    for key in keys[:-1]:
        current = current.setdefault(key, {})
        if not isinstance(current, dict):
            raise ValueError("Cannot override non-mapping configuration value.")

    current[keys[-1]] = value


def _collect_environment_overrides(prefix: str = ENV_PREFIX) -> dict[str, Any]:
    """Collect configuration overrides from environment variables."""

    overrides: dict[str, Any] = {}
    for name, value in os.environ.items():
        if not name.startswith(prefix) or name == CONFIG_PATH_ENV_VAR:
            continue

        path = name[len(prefix) :]
        if not path:
            continue

        keys = [key.lower() for key in path.split("__") if key]
        if not keys:
            continue

        _set_nested_value(overrides, keys, _parse_env_value(value))

    return overrides


def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge two configuration dictionaries recursively."""

    merged = base.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def _resolve_path(value: str, config_path: Path) -> str:
    """Resolve a path using repository root for built-in configs.

    For custom config files outside of configs/, resolve paths relative to the
    config file location.
    """

    candidate = Path(value)
    if candidate.is_absolute():
        return str(candidate)

    config_root = config_path.parent
    configs_dir = REPO_ROOT / "configs"
    if config_root == configs_dir or config_root.is_relative_to(configs_dir):
        return str((REPO_ROOT / candidate).resolve())

    return str((config_root / candidate).resolve())


def load_config(
    config_path: Path | None = None, env_prefix: str = ENV_PREFIX
) -> AppConfig:
    """Load the application configuration from YAML and environment variables."""

    resolved_path = _resolve_config_path(config_path)
    base_config = _load_yaml_data(resolved_path)
    overrides = _collect_environment_overrides(env_prefix)
    effective_config = _merge_dicts(base_config, overrides)

    logging_data = effective_config.get("logging", {})
    if not isinstance(logging_data, dict):
        raise ValueError("The logging section must be a mapping.")

    dataset_data = effective_config.get("dataset", {})
    if not isinstance(dataset_data, dict):
        raise ValueError("The dataset section must be a mapping.")

    training_data = effective_config.get("training", {})
    if not isinstance(training_data, dict):
        raise ValueError("The training section must be a mapping.")

    dashboard_data = effective_config.get("dashboard", {})
    if not isinstance(dashboard_data, dict):
        raise ValueError("The dashboard section must be a mapping.")

    logging_config = LoggingConfig(
        level=str(logging_data.get("level", LoggingConfig.level)),
        format=str(logging_data.get("format", LoggingConfig.format)),
        to_file=bool(logging_data.get("to_file", LoggingConfig.to_file)),
        file_path=_resolve_path(
            str(logging_data.get("file_path", LoggingConfig.file_path)),
            resolved_path,
        ),
    )

    dataset_config = DatasetConfig(
        name=str(dataset_data.get("name", DatasetConfig.name)),
        source=str(dataset_data.get("source", DatasetConfig.source)),
        raw_data_path=_resolve_path(
            str(dataset_data.get("raw_data_path", DatasetConfig.raw_data_path)),
            resolved_path,
        ),
        processed_data_path=_resolve_path(
            str(
                dataset_data.get(
                    "processed_data_path", DatasetConfig.processed_data_path
                )
            ),
            resolved_path,
        ),
        cache_path=_resolve_path(
            str(dataset_data.get("cache_path", DatasetConfig.cache_path)),
            resolved_path,
        ),
        download_url=str(dataset_data.get("download_url", DatasetConfig.download_url)),
        checksum=str(dataset_data.get("checksum", DatasetConfig.checksum)),
    )

    training_config = TrainingConfig(
        random_seed=int(training_data.get("random_seed", TrainingConfig.random_seed)),
        model_type=str(training_data.get("model_type", TrainingConfig.model_type)),
        batch_size=int(training_data.get("batch_size", TrainingConfig.batch_size)),
        learning_rate=float(
            training_data.get("learning_rate", TrainingConfig.learning_rate)
        ),
        max_epochs=int(training_data.get("max_epochs", TrainingConfig.max_epochs)),
        checkpoint_path=_resolve_path(
            str(training_data.get("checkpoint_path", TrainingConfig.checkpoint_path)),
            resolved_path,
        ),
        experiment_name=str(
            training_data.get("experiment_name", TrainingConfig.experiment_name)
        ),
    )

    dashboard_config = DashboardConfig(
        enabled=bool(dashboard_data.get("enabled", DashboardConfig.enabled)),
        host=str(dashboard_data.get("host", DashboardConfig.host)),
        port=int(dashboard_data.get("port", DashboardConfig.port)),
        title=str(dashboard_data.get("title", DashboardConfig.title)),
    )

    return AppConfig(
        app_name=str(effective_config.get("app_name", AppConfig.app_name)),
        logging=logging_config,
        dataset=dataset_config,
        training=training_config,
        dashboard=dashboard_config,
    )
