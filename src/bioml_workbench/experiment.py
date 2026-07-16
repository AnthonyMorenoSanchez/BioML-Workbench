from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ExperimentTracker:
    """
    Simple experiment tracker that uses MLflow when available, otherwise
    writes JSON artifacts.
    """

    def __init__(self, run_name: str | None = None, backend: str | None = None) -> None:
        self.run_name = run_name
        self.backend = backend
        try:
            import mlflow

            self._mlflow = mlflow
        except Exception:  # pragma: no cover - optional dependency
            self._mlflow = None

    def log_metrics(self, metrics: dict[str, Any]) -> None:
        if self._mlflow is not None:
            self._mlflow.log_metrics(metrics)
            return
        # fallback: write to artifacts/run_metrics.json
        artifacts = Path("artifacts")
        artifacts.mkdir(parents=True, exist_ok=True)
        out = artifacts / "run_metrics.json"
        out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    def log_params(self, params: dict[str, Any]) -> None:
        if self._mlflow is not None:
            self._mlflow.log_params(params)
            return
        artifacts = Path("artifacts")
        artifacts.mkdir(parents=True, exist_ok=True)
        out = artifacts / "run_params.json"
        out.write_text(json.dumps(params, indent=2), encoding="utf-8")
