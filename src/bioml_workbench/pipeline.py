from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

from .benchmark import run_classification_benchmark, save_metrics_csv
from .preprocessing import PreprocessingPipeline
from .workflow import TrainingWorkflow


class EndToEndPipeline:
    """Coordinate preprocessing, training, and artifact generation."""

    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir or "artifacts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        X: Sequence[Sequence[float]],
        y: Sequence[int],
        model_name: str = "simple_logistic",
    ) -> dict[str, Any]:
        preprocessing = PreprocessingPipeline()
        preprocessed = preprocessing.run(
            X,
            config={
                "filter_low_quality": False,
                "normalize": False,
                "scale": False,
                "select_highly_variable_features": False,
                "reduce_dimensions": False,
            },
        )

        workflow = TrainingWorkflow(output_dir=self.output_dir)
        training_result = workflow.run(
            preprocessed["matrix"],
            y,
            model_name=model_name,
        )

        prediction_matrix = preprocessed["matrix"]
        metrics = run_classification_benchmark(
            list(y),
            training_result["model"].predict(prediction_matrix),
        )
        save_metrics_csv(metrics, self.output_dir / "metrics.csv")

        summary = {
            "model_name": model_name,
            "sample_count": len(X),
            "feature_count": len(X[0]) if X else 0,
            "metrics": metrics,
            "processed_matrix_shape": [
                len(prediction_matrix),
                len(prediction_matrix[0]) if prediction_matrix else 0,
            ],
        }
        (self.output_dir / "summary.json").write_text(
            json.dumps(summary, indent=2),
            encoding="utf-8",
        )

        return {
            "processed_matrix": preprocessed["matrix"],
            "metrics": metrics,
            "artifacts": training_result["artifacts"] + [str(self.output_dir / "summary.json")],
        }
