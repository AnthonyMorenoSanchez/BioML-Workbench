from __future__ import annotations

from typing import Any

import plotly.express as px
import plotly.graph_objects as go


def qc_scatter_figure(adata: Any) -> go.Figure:
    """Plot total counts against detected genes for each cell."""
    frame = adata.obs[["total_counts", "n_genes_by_counts", "pct_counts_mt"]]
    return px.scatter(
        frame,
        x="total_counts",
        y="n_genes_by_counts",
        color="pct_counts_mt",
        labels={
            "total_counts": "Total counts",
            "n_genes_by_counts": "Detected genes",
            "pct_counts_mt": "Mitochondrial percent",
        },
        title="Single-Cell QC",
    )


def embedding_figure(adata: Any, color_by: str = "leiden") -> go.Figure:
    """Plot a UMAP embedding colored by cluster, label, or QC metadata."""
    if "X_umap" not in adata.obsm:
        raise ValueError("Run preprocess_adata before creating an embedding figure")
    if color_by not in adata.obs:
        raise ValueError(f"Unknown observation column: {color_by}")
    frame = adata.obs[[color_by]].copy()
    frame["UMAP 1"] = adata.obsm["X_umap"][:, 0]
    frame["UMAP 2"] = adata.obsm["X_umap"][:, 1]
    return px.scatter(
        frame,
        x="UMAP 1",
        y="UMAP 2",
        color=color_by,
        title=f"UMAP colored by {color_by}",
    )


def cluster_size_figure(adata: Any, cluster_column: str = "leiden") -> go.Figure:
    """Plot cell counts per unsupervised cluster."""
    if cluster_column not in adata.obs:
        raise ValueError(f"Unknown cluster column: {cluster_column}")
    counts = adata.obs[cluster_column].value_counts().sort_index()
    return go.Figure(
        data=[go.Bar(x=counts.index.astype(str).tolist(), y=counts.tolist())],
        layout=go.Layout(
            title="Cluster sizes",
            xaxis_title="Cluster",
            yaxis_title="Cells",
        ),
    )
