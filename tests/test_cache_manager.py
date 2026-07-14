from pathlib import Path

from bioml_workbench.utils.cache_manager import CacheManager


def test_cache_manager_save_load_clear(tmp_path: Path) -> None:
    cache_dir = tmp_path / "cache"
    manager = CacheManager(cache_dir)

    artifact_path = manager.save("metrics", {"accuracy": 0.92})
    assert artifact_path.exists()
    assert manager.exists("metrics")
    assert manager.load("metrics") == {"accuracy": 0.92}

    manager.clear("metrics")
    assert not manager.exists("metrics")

    manager.save("other", {"value": 1})
    manager.clear()
    assert not any(cache_dir.iterdir())
