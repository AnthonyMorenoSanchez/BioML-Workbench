from pathlib import Path

from bioml_workbench.configuration import AppConfig, load_config


def test_load_config_from_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app_name: demo-app\n"
        "logging:\n"
        "  level: DEBUG\n"
        "  to_file: false\n"
        "  file_path: logs/demo.log\n",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert isinstance(config, AppConfig)
    assert config.app_name == "demo-app"
    assert config.logging.level == "DEBUG"
    assert config.logging.to_file is False
