# Phase 8 — Interactive Dashboard

Phase 8 adds an interactive Streamlit-based dashboard for CSV datasets and the cached PBMC68k AnnData dataset.

## Completed work

- Added explicit PBMC68k loading through `scvelo.datasets.pbmc68k()` with local AnnData caching.
- Added barcode-keyed CSV/TSV label upload with provenance and overlap reporting.
- Added explicit controls for sparse QC, preprocessing, UMAP, Leiden clustering, marker genes, and held-out logistic-regression evaluation.
- Added interactive QC, UMAP, and cluster-size figures plus held-out prediction inspection.

## Usage

Run the dashboard from the workspace venv:

```bash
# From repository root
.venv\Scripts\python.exe -m streamlit run ui/streamlit_app.py
```

## Notes

- Streamlit is optional and available via the `ui` extra in `pyproject.toml`.
- The dashboard does not fabricate biological labels. Supervised training requires a user-provided or published barcode-keyed label column.
- PBMC68k is a single-donor dataset; held-out cell metrics are not donor-level generalization estimates.
