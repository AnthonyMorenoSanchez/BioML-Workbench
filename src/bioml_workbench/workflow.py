from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any, Sequence

from .benchmark import run_classification_benchmark, save_metrics_csv
from .ml import BaselineClassifier, SimpleLogisticRegression


class TrainingWorkflow:
    """Run a lightweight training workflow and persist artifacts."""

    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir or "artifacts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        X: Sequence[Sequence[float]],
        y: Sequence[int],
        model_name: str = "simple_logistic",
    ) -> dict[str, Any]:
        if model_name == "baseline":
            model = BaselineClassifier()
        elif model_name == "simple_logistic":
            model = SimpleLogisticRegression(n_iter=200)
        else:
            raise ValueError(f"Unsupported model name: {model_name}")

        model.fit(X, y)
        predictions = model.predict(X)
        metrics = run_classification_benchmark(list(y), predictions)

        metrics_path = self.output_dir / "metrics.csv"
        save_metrics_csv(metrics, metrics_path)

        model_path = self.output_dir / "model.pkl"
        with open(model_path, "wb") as handle:
            pickle.dump(model, handle)

        manifest = {
            "model_name": model_name,
            "sample_count": len(X),
            "feature_count": len(X[0]) if X else 0,
            "metrics": metrics,
        }
        manifest_path = self.output_dir / "training_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return {"model": model, "metrics": metrics, "artifacts": [str(metrics_path), str(model_path), str(manifest_path)]}
