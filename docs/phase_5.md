# Phase 5 — Preprocessing Pipeline

Phase 5 introduces a configurable preprocessing pipeline for tabular data.

## Completed work

- Added a preprocessing pipeline with configurable quality filtering, normalization, scaling, feature selection, dimensionality reduction, and neighbor-graph construction.
- Added support for a lightweight UMAP-style projection helper based on dimensionality reduction.
- Added tests covering filtering, normalization, scaling, feature selection, and dimensionality reduction.

## Usage

```python
from bioml_workbench.preprocessing import PreprocessingPipeline

pipeline = PreprocessingPipeline()
result = pipeline.run(
    [[0.0, 1.0, 2.0], [1.0, 1.0, 2.0]],
    config={"filter_low_quality": True, "min_counts": 2, "normalize": True},
)
```
