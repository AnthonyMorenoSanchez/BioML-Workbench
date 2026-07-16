# Phase 4 — Exploratory Analysis

Phase 4 introduces reusable exploratory-analysis helpers for biological datasets.

## Completed work

- Added a lightweight analysis module for summary statistics, cell summaries, metadata summaries, and QC reporting.
- Added a visualization helper that produces simple histogram summaries for reports and dashboards.
- Added tests covering summary generation and QC reporting.

## Usage

```python
from bioml_workbench.analysis import AnalysisModule, VisualizationModule

module = AnalysisModule()
summary = module.summarize_features([[1.0, 2.0], [3.0, 4.0]], feature_names=["gene_a", "gene_b"])
qc_report = module.generate_qc_report([[0.0, 1.0], [2.0, 3.0]], min_total=4.0)

visualization = VisualizationModule()
histogram = visualization.histogram([1, 2, 2, 3], bins=2)
```
