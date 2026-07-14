from pathlib import Path

from bioml_workbench.configuration_manager import ConfigurationManager


def test_configuration_manager_can_reload(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("app_name: config-manager-test\n", encoding="utf-8")

    manager = ConfigurationManager(config_path=config_path)
    assert manager.get().app_name == "config-manager-test"

    config_path.write_text("app_name: updated-config\n", encoding="utf-8")
    manager.reload()
    assert manager.get().app_name == "updated-config"
