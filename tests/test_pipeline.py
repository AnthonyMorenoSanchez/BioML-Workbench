from __future__ import annotations

from pathlib import Path

from bioml_workbench.pipeline import EndToEndPipeline


def test_end_to_end_pipeline_generates_artifacts(tmp_path: Path) -> None:
    X = [
        [0.0, 0.0],
        [0.1, 0.0],
        [0.0, 0.1],
        [0.2, 0.1],
        [1.0, 1.0],
        [1.1, 1.0],
        [1.0, 1.1],
        [1.2, 1.1],
        [2.0, 2.0],
        [2.1, 2.0],
    ]
    y = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

    pipeline = EndToEndPipeline(output_dir=tmp_path)
    result = pipeline.run(X, y, model_name="simple_logistic")

    assert result["metrics"]["accuracy"] >= 0.8
    assert (tmp_path / "metrics.csv").exists()
    assert (tmp_path / "model.pkl").exists()
    assert (tmp_path / "summary.json").exists()
    assert result["processed_matrix"]
