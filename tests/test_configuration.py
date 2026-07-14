from pathlib import Path

from bioml_workbench.configuration import AppConfig, load_config


def test_load_config_from_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app_name: demo-app\n"
        "logging:\n"
        "  level: DEBUG\n"
        "  to_file: false\n"
        "  file_path: logs/demo.log\n"
        "dataset:\n"
        "  name: test-dataset\n"
        "training:\n"
        "  batch_size: 64\n"
        "dashboard:\n"
        "  enabled: false\n",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert isinstance(config, AppConfig)
    assert config.app_name == "demo-app"
    assert config.logging.level == "DEBUG"
    assert config.logging.to_file is False
    assert config.dataset.name == "test-dataset"
    assert config.training.batch_size == 64
    assert config.dashboard.enabled is False


def test_load_config_overrides_with_environment(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app_name: demo-app\n"
        "dataset:\n"
        "  name: base-dataset\n"
        "training:\n"
        "  batch_size: 64\n"
        "dashboard:\n"
        "  enabled: true\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("BIOML_DATASET__NAME", "env-dataset")
    monkeypatch.setenv("BIOML_TRAINING__BATCH_SIZE", "256")
    monkeypatch.setenv("BIOML_DASHBOARD__ENABLED", "false")

    config = load_config(config_path)

    assert config.dataset.name == "env-dataset"
    assert config.training.batch_size == 256
    assert config.dashboard.enabled is False


def test_load_config_path_from_environment(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app_name: env-config-app\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("BIOML_CONFIG_PATH", str(config_path))

    config = load_config()

    assert config.app_name == "env-config-app"
