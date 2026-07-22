from pathlib import Path

from bioml_workbench.experiment import ExperimentRun


def test_experiment_run_writes_unique_reproducible_artifacts(tmp_path: Path) -> None:
    run = ExperimentRun.create(tmp_path, "pbmc68k")

    run.log_config({"random_state": 42})
    run.log_metrics({"accuracy": 0.9})
    report_path = run.write_report("# Result\n\nAccuracy: 0.9")

    assert run.path.name.startswith("pbmc68k-")
    assert (run.path / "config.json").exists()
    assert (run.path / "metrics.json").exists()
    assert report_path.read_text(encoding="utf-8").startswith("# Result")
