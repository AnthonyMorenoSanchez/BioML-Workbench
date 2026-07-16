from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

from bioml_workbench.data import DatasetMetadata, DatasetRegistry, DownloadManager


def test_dataset_registry_registers_and_lists_datasets() -> None:
    registry = DatasetRegistry()
    metadata = DatasetMetadata(
        name="pbmc68k",
        description="PBMC68k sample dataset",
        source="https://example.com/pbmc68k.csv",
        checksum="abc123",
    )

    registry.register(metadata)

    assert registry.get("pbmc68k") == metadata
    assert registry.list_names() == ["pbmc68k"]


def test_download_manager_copies_local_files_and_validates_checksum(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.txt"
    source.write_text("dataset payload", encoding="utf-8")
    expected_checksum = hashlib.sha256(b"dataset payload").hexdigest()

    metadata = DatasetMetadata(
        name="local-sample",
        description="Local sample dataset",
        source=str(source),
        checksum=expected_checksum,
    )

    manager = DownloadManager(cache_dir=tmp_path / "cache")
    destination = manager.download(metadata, destination=tmp_path / "downloaded.txt")

    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "dataset payload"


def test_download_manager_extracts_archives(tmp_path: Path) -> None:
    archive_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive_path, "w") as archive_file:
        archive_file.writestr("sample.txt", "extracted payload")

    metadata = DatasetMetadata(
        name="zip-sample",
        description="Archive sample dataset",
        source=str(archive_path),
        archive=True,
    )

    manager = DownloadManager(cache_dir=tmp_path / "cache")
    destination = manager.download(metadata, destination=tmp_path / "extracted")

    assert (destination / "sample.txt").exists()
    assert (
        (destination / "sample.txt").read_text(encoding="utf-8")
        == "extracted payload"
    )
