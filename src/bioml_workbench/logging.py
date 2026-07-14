from __future__ import annotations

import logging
from pathlib import Path

from .configuration import AppConfig, load_config


def configure_logging(config: AppConfig | None = None) -> logging.Logger:
    """Configure application logging using the supplied configuration."""

    resolved_config = config or load_config()
    logger = logging.getLogger(resolved_config.app_name)
    logger.handlers.clear()
    logger.setLevel(
        getattr(logging, resolved_config.logging.level.upper(), logging.INFO)
    )
    logger.propagate = False

    formatter = logging.Formatter(resolved_config.logging.format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if resolved_config.logging.to_file:
        log_path = Path(resolved_config.logging.file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str, config: AppConfig | None = None) -> logging.Logger:
    """Retrieve a named logger for application components."""

    logger_name = name if config is None else f"{config.app_name}.{name}"
    return logging.getLogger(logger_name)
