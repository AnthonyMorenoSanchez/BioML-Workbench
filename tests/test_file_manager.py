from pathlib import Path

from bioml_workbench.utils.file_manager import FileManager


def test_file_manager_write_read(tmp_path: Path) -> None:
    base_path = tmp_path / "storage"
    manager = FileManager(base_path)
    manager.write_text("subdir/sample.txt", "hello world")
    assert manager.exists("subdir/sample.txt")
    assert manager.read_text("subdir/sample.txt") == "hello world"

    manager.write_bytes("subdir/binary.bin", b"abc")
    assert manager.read_bytes("subdir/binary.bin") == b"abc"

    all_files = list(manager.list_files("*", recursive=True))
    assert any(file.name == "sample.txt" for file in all_files)
