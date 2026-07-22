# BioML Workbench

BioML Workbench is a production-oriented Python package for computational biology and MLOps workflows.
It provides a modular foundation for omics-style data processing, preprocessing, exploratory analysis, model training, experiment tracking, and interactive dashboards.

## Quick Start

Use the workspace virtual environment for all commands:

```powershell
# From the repository root
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
```

### Start the Streamlit dashboard

```powershell
.\.venv\Scripts\python.exe -m streamlit run ui/streamlit_app.py
```

The dashboard accepts a CSV file with a `sample` column followed by one or more numeric feature columns. After upload it will:

- show sample/feature summaries
- generate QC statistics
- run preprocessing steps
- display feature histograms and processed outputs
- train a baseline classifier and save metrics to the `artifacts/` folder

### Run the full test suite

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### Run linting and type checks

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m mypy src
```

## Example Python workflow

```python
from bioml_workbench.dashboard import build_dashboard_payload, load_tabular_data

payload = build_dashboard_payload(load_tabular_data("data/raw/example.csv"))
print(payload["summary"])
```

## Optional ML dependencies

To enable optional experiment tracking and model wrappers, install the extras:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit mlflow xgboost
```

## Project layout

- configs/: YAML configuration files
- src/bioml_workbench/: package implementation
- tests/: unit tests
- docs/: project documentation
- ui/: Streamlit dashboard
- reports/: generated reports and artifacts
