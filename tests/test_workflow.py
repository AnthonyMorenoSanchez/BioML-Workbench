from __future__ import annotations

import pickle
from pathlib import Path

from bioml_workbench.workflow import TrainingWorkflow


def test_training_workflow_runs_and_saves_artifacts(tmp_path: Path) -> None:
    X = [
        [0.0, 0.0],
        [0.1, 0.0],
        [0.0, 0.1],
        [0.2, 0.1],
        [1.0, 1.0],
        [1.1, 1.0],
        [1.0, 1.1],
        [1.2, 1.1],
    ]
    y = [0, 0, 0, 0, 1, 1, 1, 1]

    workflow = TrainingWorkflow(output_dir=tmp_path)
    result = workflow.run(X, y, model_name="simple_logistic")

    assert result["metrics"]["accuracy"] >= 0.8
    assert (tmp_path / "metrics.csv").exists()
    assert (tmp_path / "training_manifest.json").exists()
    assert (tmp_path / "model.pkl").exists()

    with open(tmp_path / "model.pkl", "rb") as handle:
        loaded_model = pickle.load(handle)
    assert loaded_model is not None
