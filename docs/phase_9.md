# Phase 9 — Continuous Benchmarking

Phase 9 adds CI-friendly benchmarking that records metrics, artifacts, and reports for every experiment.

## Completed work

- Added a lightweight benchmarking module (`src/bioml_workbench/benchmark.py`) that computes core classification metrics and saves CSV artifacts.
- Added a simple experiment tracker wrapper (`src/bioml_workbench/experiment.py`) that uses `mlflow` when available and falls back to JSON artifacts.

## Usage

```python
from bioml_workbench.benchmark import run_classification_benchmark, save_metrics_csv
from bioml_workbench.experiment import ExperimentTracker

metrics = run_classification_benchmark(y_true, y_pred)
save_metrics_csv(metrics, "artifacts/metrics.csv")

tracker = ExperimentTracker()
tracker.log_metrics(metrics)
```

## Notes

- For full CI integration, call benchmarking from your experiment runner and upload artifacts to your CI storage or dashboard.
- Optional integrations: MLflow, Weights & Biases (configured via extras in `pyproject.toml`).
