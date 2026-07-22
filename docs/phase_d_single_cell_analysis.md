# Phase D - Sparse Single-Cell Analysis

Phase D provides the first real single-cell analysis workflow for `anndata.AnnData` datasets, including PBMC68k loaded through the dashboard data layer.

## Included

- Sparse-aware quality-control metrics for total counts, detected genes, and mitochondrial percentage.
- Preservation of immutable raw counts in `adata.layers["counts"]`.
- Configurable cell and gene filtering.
- Library-size normalization and `log1p` transformation.
- Highly variable gene selection, PCA, nearest-neighbor graph construction, and UMAP through Scanpy.
- Leiden clustering with cluster provenance recorded as `unsupervised_cluster`.

## Usage

```python
from bioml_workbench.single_cell import (
    calculate_qc_metrics,
    cluster_cells,
    preprocess_adata,
)

calculate_qc_metrics(adata)
preprocess_adata(
    adata,
    min_genes=200,
    min_cells_per_gene=3,
    n_top_genes=2000,
    n_pcs=50,
    n_neighbors=15,
)
cluster_cells(adata, resolution=1.0)
```

The workflow writes QC metrics to `adata.obs`, highly variable gene flags to `adata.var`, PCA and UMAP embeddings to `adata.obsm`, and graph connectivities to `adata.obsp`.

## Deliberate Limits

This phase does not implement reference-label alignment, marker-gene ranking, plotting, held-out supervised training, or dashboard controls for these operations. Those are separate upcoming phases.