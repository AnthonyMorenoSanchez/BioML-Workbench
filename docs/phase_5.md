# Phase 5 — Tabular Preprocessing Pipeline

Phase 5 introduces a configurable preprocessing pipeline for tabular data.

## Completed work

- Added a preprocessing pipeline with configurable quality filtering, normalization, scaling, feature selection, and neighbor-graph construction for small tabular inputs.
- Added tests covering filtering, normalization, scaling, feature selection, and dimensionality reduction.

## Scope

This module remains the generic tabular path. Its legacy dimensionality-reduction and UMAP-style helpers are not biological PCA or UMAP implementations. Real sparse single-cell preprocessing is implemented separately in `bioml_workbench.single_cell.preprocessing` and documented in `phase_d_single_cell_analysis.md`.

## Usage

```python
from bioml_workbench.preprocessing import PreprocessingPipeline

pipeline = PreprocessingPipeline()
result = pipeline.run(
    [[0.0, 1.0, 2.0], [1.0, 1.0, 2.0]],
    config={"filter_low_quality": True, "min_counts": 2, "normalize": True},
)
```
