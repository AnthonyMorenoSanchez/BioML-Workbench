from __future__ import annotations

from typing import Any

import scanpy as sc

from .qc import calculate_qc_metrics


def preprocess_adata(
    adata: Any,
    min_genes: int = 200,
    min_cells_per_gene: int = 3,
    target_sum: float = 10_000,
    n_top_genes: int = 2_000,
    n_pcs: int = 50,
    n_neighbors: int = 15,
    random_state: int = 42,
) -> None:
    """Run a sparse-aware QC, normalization, PCA, neighbors, and UMAP workflow."""
    calculate_qc_metrics(adata)
    sc.pp.filter_cells(adata, min_genes=min_genes)
    sc.pp.filter_genes(adata, min_cells=min_cells_per_gene)
    sc.pp.normalize_total(adata, target_sum=target_sum)
    sc.pp.log1p(adata)

    max_features = min(n_top_genes, adata.n_vars)
    sc.pp.highly_variable_genes(adata, n_top_genes=max_features, subset=True)
    max_components = min(n_pcs, adata.n_obs - 1, adata.n_vars - 1)
    if max_components < 1:
        raise ValueError("PCA requires at least two cells and two retained genes")
    sc.pp.pca(adata, n_comps=max_components, random_state=random_state)
    max_neighbors = min(n_neighbors, adata.n_obs - 1)
    if max_neighbors < 1:
        raise ValueError("Neighbor graph requires at least two retained cells")
    sc.pp.neighbors(adata, n_neighbors=max_neighbors, n_pcs=max_components)
    sc.tl.umap(adata, random_state=random_state)
    adata.uns["preprocessing"] = {
        "min_genes": min_genes,
        "min_cells_per_gene": min_cells_per_gene,
        "target_sum": target_sum,
        "n_top_genes": max_features,
        "n_pcs": max_components,
        "n_neighbors": max_neighbors,
        "random_state": random_state,
    }
