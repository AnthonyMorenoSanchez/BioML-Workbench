from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .exceptions import CacheError
from .file_manager import FileManager


@dataclass
class CacheManager:
    """Simple cache manager for disk-backed artifacts."""

    base_path: Path | str
    file_manager: FileManager = field(init=False)

    def __post_init__(self) -> None:
        self.file_manager = FileManager(self.base_path)

    def get_cache_path(self, name: str, extension: str = "json") -> Path:
        """Get the resolved cache path for a named artifact."""

        safe_name = name.replace(" ", "_").lower()
        return self.file_manager.resolve_path(f"{safe_name}.{extension}")

    def exists(self, name: str, extension: str = "json") -> bool:
        """Return whether a cache artifact exists."""

        return self.get_cache_path(name, extension).exists()

    def save(self, name: str, value: Any, extension: str = "json") -> Path:
        """Save a cache artifact to disk."""

        target = self.get_cache_path(name, extension)
        target.parent.mkdir(parents=True, exist_ok=True)
        if extension == "json":
            try:
                target.write_text(json.dumps(value, indent=2), encoding="utf-8")
            except TypeError as exc:
                raise CacheError("Unable to serialize cache value to JSON") from exc
        else:
            raise CacheError(f"Unsupported cache extension: {extension}")
        return target

    def load(self, name: str, extension: str = "json") -> Any:
        """Load a cache artifact from disk."""

        target = self.get_cache_path(name, extension)
        if not target.exists():
            raise CacheError(f"Cache artifact not found: {target}")
        if extension == "json":
            return json.loads(target.read_text(encoding="utf-8"))
        raise CacheError(f"Unsupported cache extension: {extension}")

    def clear(self, name: str | None = None, extension: str = "json") -> None:
        """Clear a named artifact or the entire cache directory."""

        if name is not None:
            target = self.get_cache_path(name, extension)
            if target.exists():
                target.unlink()
            return

        for file_path in self.file_manager.list_files("*", recursive=True):
            if file_path.is_file():
                file_path.unlink()
