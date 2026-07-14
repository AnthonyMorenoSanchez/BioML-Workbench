from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Generator


class BioMLException(Exception):
    """Base exception for BioML Workbench."""


class ConfigurationError(BioMLException):
    """Raised when configuration loading or validation fails."""


class CacheError(BioMLException):
    """Raised when a cache operation fails."""


class DataError(BioMLException):
    """Raised for dataset or data processing failures."""


@contextmanager
def handle_exceptions(
    logger: logging.Logger, message: str
) -> Generator[None, None, None]:
    """Context manager that logs and re-raises exceptions."""

    try:
        yield
    except Exception:
        logger.exception(message)
        raise
