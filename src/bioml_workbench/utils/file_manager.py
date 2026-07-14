from __future__ import annotations

from pathlib import Path
from typing import Iterator


class FileManager:
    """Utility class for file system operations."""

    def __init__(self, base_path: Path | str) -> None:
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def resolve_path(self, *path_parts: str) -> Path:
        """Resolve a path relative to the base directory."""

        target = self.base_path.joinpath(*path_parts)
        return target.resolve()

    def ensure_directory(self, *path_parts: str) -> Path:
        """Create and return a directory relative to the base directory."""

        directory = self.resolve_path(*path_parts)
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def write_text(
        self, relative_path: str, content: str, encoding: str = "utf-8"
    ) -> Path:
        """Write text to a file located under the base directory."""

        file_path = self.resolve_path(relative_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding=encoding)
        return file_path

    def read_text(self, relative_path: str, encoding: str = "utf-8") -> str:
        """Read a text file located under the base directory."""

        file_path = self.resolve_path(relative_path)
        return file_path.read_text(encoding=encoding)

    def list_files(self, pattern: str = "*", recursive: bool = False) -> Iterator[Path]:
        """List files under the base directory matching the pattern."""

        if recursive:
            yield from self.base_path.rglob(pattern)
        else:
            yield from self.base_path.glob(pattern)

    def exists(self, relative_path: str) -> bool:
        """Return whether a path exists under the base directory."""

        return self.resolve_path(relative_path).exists()

    def delete(self, relative_path: str) -> None:
        """Delete a file or directory under the base directory."""

        target = self.resolve_path(relative_path)
        if target.is_dir():
            for child in target.iterdir():
                if child.is_dir():
                    self.delete(str(child.relative_to(self.base_path)))
                else:
                    child.unlink()
            target.rmdir()
        elif target.exists():
            target.unlink()

    def read_bytes(self, relative_path: str) -> bytes:
        """Read a binary file located under the base directory."""

        return self.resolve_path(relative_path).read_bytes()

    def write_bytes(self, relative_path: str, content: bytes) -> Path:
        """Write binary content to a file located under the base directory."""

        file_path = self.resolve_path(relative_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)
        return file_path
