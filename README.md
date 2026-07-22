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

Install the dashboard dependencies before starting the dashboard:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[ui]"
```

The dashboard accepts a CSV file with a `sample` column followed by one or more numeric feature columns. After upload it will:

- show sample/feature summaries
- align barcode-keyed reference or user-uploaded labels with provenance
- calculate QC metrics, normalize, select highly variable genes, run PCA, neighbors, UMAP, and Leiden clustering
- display QC scatter plots, UMAP embeddings, cluster sizes, and marker-gene tables
- train a sparse logistic classifier with a stratified held-out test split when labels are available
- save models, predictions, metrics, and manifests under a unique `artifacts/runs/` directory

### PBMC68k sample dataset

In the sidebar, enable **Use PBMC68k sample dataset**, then select **Load PBMC68k**. The application uses `scvelo.datasets.pbmc68k()` rather than trying to download the protected 10x dataset landing page directly. The sparse AnnData object is saved after its first load at `data/cache/pbmc68k/pbmc68k.h5ad`; later loads reuse that local cache.

Disable the PBMC68k option to switch back to independently uploaded CSV datasets. The app does not download or reload PBMC68k merely because the checkbox is selected.

PBMC68k comes from a single donor. A random cell-level held-out split measures within-dataset interpolation, not performance across donors, experiments, chemistries, or disease states. Published 10x labels should be treated as reference annotations rather than definitive biological ground truth.

### Label format

Upload a CSV or TSV table with a `barcode` column and a label column, then choose its provenance in the **Labels** page. Labels are aligned strictly by barcode, duplicate barcodes are rejected, and unmatched barcodes are reported.

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
