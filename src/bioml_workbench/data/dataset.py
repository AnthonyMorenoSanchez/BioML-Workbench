from __future__ import annotations

import hashlib
import shutil
import tarfile
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


@dataclass(frozen=True)
class DatasetMetadata:
    """Describes a dataset artifact and its retrieval metadata."""

    name: str
    description: str
    source: str
    checksum: str | None = None
    archive: bool = False
    expected_files: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_local(self) -> bool:
        return Path(self.source).exists()

    def is_remote(self) -> bool:
        parsed = urlparse(self.source)
        return parsed.scheme in {"http", "https"}


class DatasetRegistry:
    """Registers known datasets and exposes metadata lookup helpers."""

    def __init__(self) -> None:
        self._datasets: dict[str, DatasetMetadata] = {}

    def register(self, dataset: DatasetMetadata) -> None:
        self._datasets[dataset.name] = dataset

    def get(self, name: str) -> DatasetMetadata:
        if name not in self._datasets:
            raise KeyError(f"Unknown dataset: {name}")
        return self._datasets[name]

    def list_names(self) -> list[str]:
        return sorted(self._datasets.keys())

    def list(self) -> list[DatasetMetadata]:
        return [self._datasets[name] for name in self.list_names()]


class DownloadManager:
    """Downloads datasets into a cache and optionally extracts archives."""

    def __init__(self, cache_dir: str | Path | None = None) -> None:
        self.cache_dir = Path(cache_dir or "data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download(
        self,
        dataset: DatasetMetadata | str,
        destination: str | Path | None = None,
        overwrite: bool = False,
        verify_checksum: bool = True,
    ) -> Path:
        metadata = (
            dataset
            if isinstance(dataset, DatasetMetadata)
            else DatasetMetadata(
                name=dataset,
                description=dataset,
                source=dataset,
            )
        )

        cache_path = self._resolve_cache_path(metadata)
        if not cache_path.exists() or overwrite:
            self._fetch_to_cache(metadata, cache_path)

        if verify_checksum and metadata.checksum:
            self._validate_checksum(cache_path, metadata.checksum)

        target_path = self._resolve_target_path(destination, metadata)
        if metadata.archive:
            self._extract_archive(cache_path, target_path)
            return target_path

        target_path.parent.mkdir(parents=True, exist_ok=True)
        if target_path.exists() and target_path.is_dir():
            target_path = target_path / cache_path.name
        shutil.copy2(cache_path, target_path)
        return target_path

    def _resolve_cache_path(self, metadata: DatasetMetadata) -> Path:
        source_name = Path(metadata.source).name or metadata.name
        if metadata.is_remote():
            source_name = metadata.name
        cache_dir = self.cache_dir / metadata.name
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / source_name

    def _resolve_target_path(
        self, destination: str | Path | None, metadata: DatasetMetadata
    ) -> Path:
        if destination is not None:
            return Path(destination)
        if metadata.archive:
            return self.cache_dir / metadata.name / "extracted"
        return self.cache_dir / metadata.name / f"{metadata.name}.bin"

    def _fetch_to_cache(self, metadata: DatasetMetadata, cache_path: Path) -> None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        if metadata.is_local():
            shutil.copy2(metadata.source, cache_path)
            return
        if metadata.is_remote():
            with (
                urllib.request.urlopen(metadata.source) as response,
                open(cache_path, "wb") as handle,
            ):
                shutil.copyfileobj(response, handle)
            return
        raise ValueError(f"Unsupported dataset source: {metadata.source}")

    def _validate_checksum(self, path: Path, checksum: str) -> None:
        file_checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        if file_checksum != checksum:
            raise ValueError(
                "Checksum mismatch for "
                f"{path}: expected {checksum}, got {file_checksum}"
            )

    def _extract_archive(self, archive_path: Path, destination: Path) -> Path:
        destination.mkdir(parents=True, exist_ok=True)
        if archive_path.suffix == ".zip" or archive_path.name.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as archive_file:
                archive_file.extractall(destination)
            return destination
        if archive_path.name.endswith(".tar.gz") or archive_path.name.endswith(".tgz"):
            with tarfile.open(archive_path, "r:gz") as archive_file:
                archive_file.extractall(destination)
            return destination
        raise ValueError(f"Unsupported archive type: {archive_path}")
