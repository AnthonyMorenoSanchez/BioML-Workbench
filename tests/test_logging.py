from pathlib import Path

from bioml_workbench.configuration import load_config
from bioml_workbench.logging import configure_logging, get_logger


def test_logging_configuration_writes_to_file(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "app_name: demo-app\n"
        "logging:\n"
        "  level: INFO\n"
        "  to_file: true\n"
        "  file_path: logs/demo.log\n",
        encoding="utf-8",
    )

    config = load_config(config_path)
    logger = configure_logging(config)
    logger.info("hello from the logger")

    log_file = tmp_path / "logs" / "demo.log"
    assert log_file.exists()
    assert "hello from the logger" in log_file.read_text(encoding="utf-8")


def test_get_logger_returns_logger() -> None:
    logger = get_logger("demo")
    assert logger.name == "demo"
