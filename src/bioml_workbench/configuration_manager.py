from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .configuration import AppConfig, load_config
from .logging import get_logger


@dataclass
class ConfigurationManager:
    """Manager for lifecycle and access of application configuration."""

    config_path: Path | None = None
    env_prefix: str = "BIOML_"
    config: AppConfig = field(init=False)

    def __post_init__(self) -> None:
        self.reload()

    def reload(self) -> AppConfig:
        """Reload configuration from disk and environment variables."""

        self.config = load_config(self.config_path, self.env_prefix)
        get_logger("configuration").debug(
            "Configuration reloaded", extra={"config": self.config.to_dict()}
        )
        return self.config

    def get(self) -> AppConfig:
        """Return the active configuration."""

        return self.config

    def get_section(self, section: str) -> object:
        """Return a named configuration section."""

        if hasattr(self.config, section):
            return getattr(self.config, section)
        raise AttributeError(f"Unknown configuration section: {section}")
