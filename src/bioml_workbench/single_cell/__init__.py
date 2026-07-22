"""Sparse AnnData-based single-cell analysis workflows."""

from .clustering import cluster_cells
from .markers import rank_marker_genes
from .plots import cluster_size_figure, embedding_figure, qc_scatter_figure
from .preprocessing import preprocess_adata
from .qc import calculate_qc_metrics
from .supervised import train_classifier

__all__ = [
    "calculate_qc_metrics",
    "cluster_cells",
    "cluster_size_figure",
    "embedding_figure",
    "preprocess_adata",
    "qc_scatter_figure",
    "rank_marker_genes",
    "train_classifier",
]
