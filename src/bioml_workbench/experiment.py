from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4


class ExperimentRun:
    """Persist reproducible run artifacts in a unique local directory."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=False)

    @classmethod
    def create(cls, root: str | Path, dataset_name: str) -> "ExperimentRun":
        run_id = f"{dataset_name}-{uuid4().hex[:12]}"
        return cls(Path(root) / "runs" / run_id)

    def log_config(self, config: dict[str, Any]) -> Path:
        return self._write_json("config.json", config)

    def log_metrics(self, metrics: dict[str, Any]) -> Path:
        return self._write_json("metrics.json", metrics)

    def write_report(self, markdown: str) -> Path:
        report_path = self.path / "report.md"
        report_path.write_text(markdown, encoding="utf-8")
        return report_path

    def _write_json(self, filename: str, payload: dict[str, Any]) -> Path:
        output_path = self.path / filename
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return output_path


class ExperimentTracker:
    """
    Simple experiment tracker that uses MLflow when available, otherwise
    writes JSON artifacts.
    """

    def __init__(self, run_name: str | None = None, backend: str | None = None) -> None:
        self.run_name = run_name
        self.backend = backend
        try:
            import mlflow  # type: ignore[import-not-found]

            self._mlflow: Any | None = mlflow
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
