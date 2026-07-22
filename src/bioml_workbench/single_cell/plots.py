from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .expression import expression_summary, extract_expression


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


def cohort_umap_figure(
    adata: Any,
    cohort_a_mask: Any,
    cohort_b_mask: Any,
    cohort_a_name: str = "Cohort A",
    cohort_b_name: str = "Cohort B",
) -> go.Figure:
    """Highlight two cohorts over muted background cells on an existing UMAP."""
    if "X_umap" not in adata.obsm:
        raise ValueError("Run preprocess_adata before creating an embedding figure")
    labels = ["Other"] * adata.n_obs
    for index in range(adata.n_obs):
        if cohort_a_mask[index]:
            labels[index] = cohort_a_name
        elif cohort_b_mask[index]:
            labels[index] = cohort_b_name
    frame = {
        "UMAP 1": adata.obsm["X_umap"][:, 0],
        "UMAP 2": adata.obsm["X_umap"][:, 1],
        "Cohort": labels,
    }
    return px.scatter(
        frame,
        x="UMAP 1",
        y="UMAP 2",
        color="Cohort",
        color_discrete_map={
            "Other": "lightgray",
            cohort_a_name: "#157a6e",
            cohort_b_name: "#d1495b",
        },
        title=f"UMAP: {cohort_a_name} vs {cohort_b_name}",
    )


def gene_feature_umap_figure(adata: Any, gene: str, layer: str = "X") -> go.Figure:
    """Color UMAP points by a selected gene's expression in the declared layer."""
    if "X_umap" not in adata.obsm:
        raise ValueError("Run preprocess_adata before creating an embedding figure")
    table = extract_expression(adata, [gene], layer=layer)
    return px.scatter(
        {
            "UMAP 1": adata.obsm["X_umap"][:, 0],
            "UMAP 2": adata.obsm["X_umap"][:, 1],
            gene: table[gene].to_numpy(),
        },
        x="UMAP 1",
        y="UMAP 2",
        color=gene,
        title=f"{gene} expression on UMAP ({layer})",
    )


def expression_distribution_figure(
    adata: Any,
    gene: str,
    cohort_masks: dict[str, Any],
    layer: str = "X",
    kind: str = "violin",
    seed: int = 42,
    max_cells: int = 2_000,
) -> go.Figure:
    """Show sampled per-cohort expression distributions with deterministic sampling."""
    rows: list[dict[str, Any]] = []
    rng = np.random.default_rng(seed)
    for cohort, mask in cohort_masks.items():
        values = extract_expression(adata, [gene], mask=mask, layer=layer)[
            gene
        ].to_numpy()
        if len(values) > max_cells:
            values = rng.choice(values, size=max_cells, replace=False)
        rows.extend(
            {"cohort": cohort, "expression": value, "layer": layer} for value in values
        )
    frame = pd.DataFrame(rows)
    if kind == "box":
        return px.box(
            frame, x="cohort", y="expression", title=f"{gene} expression ({layer})"
        )
    if kind == "ecdf":
        return px.ecdf(
            frame, x="expression", color="cohort", title=f"{gene} ECDF ({layer})"
        )
    if kind == "strip":
        return px.strip(
            frame,
            x="cohort",
            y="expression",
            color="cohort",
            title=f"{gene} expression ({layer})",
        )
    return px.violin(
        frame,
        x="cohort",
        y="expression",
        color="cohort",
        box=True,
        points=False,
        title=f"{gene} expression ({layer})",
    )


def multi_gene_dotplot_figure(
    adata: Any, genes: list[str], cohort_masks: dict[str, Any], layer: str = "X"
) -> go.Figure:
    """Plot mean expression and percent-expressing dot sizes across cohorts."""
    summary = expression_summary(adata, genes, cohort_masks, layer=layer)
    return px.scatter(
        summary,
        x="gene",
        y="cohort",
        size="percent_expressing",
        color="mean_expression",
        title=f"Mean expression and percent expressing ({layer})",
    )


def gene_pair_scatter_figure(
    adata: Any, gene_x: str, gene_y: str, mask: Any = None, layer: str = "X"
) -> go.Figure:
    """Scatter two selected gene columns without densifying other features."""
    table = extract_expression(adata, [gene_x, gene_y], mask=mask, layer=layer)
    return px.scatter(
        table, x=gene_x, y=gene_y, title=f"{gene_x} vs {gene_y} ({layer})"
    )


def qc_comparison_figure(
    adata: Any, cohort_masks: dict[str, Any], column: str = "pct_counts_mt"
) -> go.Figure:
    """Compare a selected QC column across cohorts."""
    rows = [
        {"cohort": name, "value": value}
        for name, mask in cohort_masks.items()
        for value in adata.obs.loc[mask, column]
    ]
    return px.box(rows, x="cohort", y="value", title=f"{column} by cohort")


def metadata_composition_figure(
    adata: Any, cohort_masks: dict[str, Any], column: str
) -> go.Figure:
    """Show categorical metadata composition for each cohort."""
    rows = [
        {"cohort": name, "value": value}
        for name, mask in cohort_masks.items()
        for value in adata.obs.loc[mask, column].astype(str)
    ]
    return px.histogram(
        rows,
        x="cohort",
        color="value",
        barmode="stack",
        title=f"{column} composition by cohort",
    )
