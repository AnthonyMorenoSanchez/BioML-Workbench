"""Sparse AnnData-based single-cell analysis workflows."""

from .clustering import cluster_cells
from .cohorts import create_cohort_definition, resolve_cohort
from .differential_expression import compare_cohorts, volcano_figure
from .expression import expression_summary, extract_expression, resolve_gene
from .markers import rank_marker_genes
from .plots import (
    cluster_size_figure,
    cohort_umap_figure,
    embedding_figure,
    expression_distribution_figure,
    gene_feature_umap_figure,
    gene_pair_scatter_figure,
    metadata_composition_figure,
    multi_gene_dotplot_figure,
    qc_comparison_figure,
    qc_scatter_figure,
)
from .preprocessing import preprocess_adata
from .qc import calculate_qc_metrics
from .supervised import train_classifier

__all__ = [
    "calculate_qc_metrics",
    "cluster_cells",
    "cluster_size_figure",
    "compare_cohorts",
    "cohort_umap_figure",
    "create_cohort_definition",
    "embedding_figure",
    "expression_distribution_figure",
    "expression_summary",
    "extract_expression",
    "gene_feature_umap_figure",
    "gene_pair_scatter_figure",
    "metadata_composition_figure",
    "multi_gene_dotplot_figure",
    "preprocess_adata",
    "qc_comparison_figure",
    "qc_scatter_figure",
    "rank_marker_genes",
    "resolve_cohort",
    "resolve_gene",
    "train_classifier",
    "volcano_figure",
]
