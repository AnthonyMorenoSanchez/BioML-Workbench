from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy.sparse import issparse  # type: ignore[import-untyped]

from .cohorts import _matrix_for_layer


def resolve_gene(adata: Any, gene: str) -> str:
    """Resolve a declared gene name against AnnData features."""
    if gene not in adata.var_names:
        raise ValueError(f"Unknown gene: {gene}")
    return str(gene)


def extract_expression(
    adata: Any, genes: list[str], mask: Any = None, layer: str = "X"
) -> pd.DataFrame:
    """Extract only selected gene columns into a compact cell-indexed table."""
    for gene in genes:
        resolve_gene(adata, gene)
    selection = (
        np.ones(adata.n_obs, dtype=bool)
        if mask is None
        else np.asarray(mask, dtype=bool)
    )
    gene_indices = [adata.var_names.get_loc(gene) for gene in genes]
    matrix = _matrix_for_layer(adata, layer)[selection, :][:, gene_indices]
    values = matrix.toarray() if issparse(matrix) else np.asarray(matrix)
    return pd.DataFrame(values, index=adata.obs_names[selection], columns=genes)


def expression_summary(
    adata: Any, genes: list[str], cohort_masks: dict[str, Any], layer: str = "X"
) -> pd.DataFrame:
    """Compute per-gene per-cohort expression metrics from selected sparse columns."""
    rows: list[dict[str, Any]] = []
    for cohort_name, mask in cohort_masks.items():
        table = extract_expression(adata, genes, mask=mask, layer=layer)
        for gene in genes:
            values = table[gene].to_numpy()
            rows.append(
                {
                    "cohort": cohort_name,
                    "gene": gene,
                    "cell_count": len(values),
                    "mean_expression": float(values.mean()) if len(values) else 0.0,
                    "median_expression": (
                        float(np.median(values)) if len(values) else 0.0
                    ),
                    "percent_expressing": (
                        float((values > 0).mean() * 100) if len(values) else 0.0
                    ),
                    "min_expression": float(values.min()) if len(values) else 0.0,
                    "max_expression": float(values.max()) if len(values) else 0.0,
                    "display_sample_size": len(values),
                    "layer": layer,
                }
            )
    return pd.DataFrame(rows)
