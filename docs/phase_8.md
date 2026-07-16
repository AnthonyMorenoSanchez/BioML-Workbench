# Phase 8 — Interactive Dashboard

Phase 8 adds an interactive Streamlit-based dashboard for exploring datasets, QC, preprocessing, training, and benchmarking.

## Completed work

- Added a minimal Streamlit app skeleton at `ui/streamlit_app.py` with independent pages for Home, Dataset Explorer, QC, Preprocessing, Training, Experiment Browser, and Benchmark.
- Dashboard is intentionally lightweight and designed to be extended with real data connectors and CLI hooks.

## Usage

Run the dashboard from the workspace venv:

```bash
# From repository root
.venv\Scripts\python.exe -m streamlit run ui/streamlit_app.py
```

## Notes

- Streamlit is optional and available via the `ui` extra in `pyproject.toml`.
- The app currently provides placeholders for functionality; integrate dataset and pipeline hooks to enable full interactivity.
