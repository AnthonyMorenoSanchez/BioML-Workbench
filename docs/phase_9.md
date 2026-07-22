# Phase 9 — Continuous Benchmarking

Phase 9 adds local, reproducible run artifacts alongside lightweight classification benchmarking.

## Completed work

- Added a lightweight benchmarking module (`src/bioml_workbench/benchmark.py`) that computes core classification metrics and saves CSV artifacts.
- Added a simple experiment tracker wrapper (`src/bioml_workbench/experiment.py`) that uses `mlflow` when available and falls back to JSON artifacts.
- Added `ExperimentRun`, which creates a unique `artifacts/runs/<dataset>-<run-id>/` directory and persists configuration, metrics, and Markdown reports.
- Held-out single-cell training also saves a model, predictions, metrics, and a feature/label manifest.

## Usage

```python
from bioml_workbench.benchmark import run_classification_benchmark, save_metrics_csv
from bioml_workbench.experiment import ExperimentTracker

metrics = run_classification_benchmark(y_true, y_pred)
save_metrics_csv(metrics, "artifacts/metrics.csv")

run = ExperimentRun.create("artifacts", "pbmc68k")
run.log_config({"random_state": 42})
run.log_metrics(metrics)
```

## Notes

- ROC/precision-recall curves, calibration, and cross-donor validation remain future extensions.
- Optional integrations: MLflow, Weights & Biases (configured via extras in `pyproject.toml`).
