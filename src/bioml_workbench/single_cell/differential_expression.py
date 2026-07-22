from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import mannwhitneyu

from .cohorts import _matrix_for_layer


def _adjust_p_values(p_values: np.ndarray) -> np.ndarray:
    order = np.argsort(p_values)
    ranked = p_values[order] * len(p_values) / (np.arange(len(p_values)) + 1)
    adjusted = np.minimum.accumulate(ranked[::-1])[::-1]
    output = np.empty_like(adjusted)
    output[order] = np.minimum(adjusted, 1.0)
    return output


def compare_cohorts(
    adata: Any,
    cohort_a_mask: np.ndarray,
    cohort_b_mask: np.ndarray,
    method: str = "wilcoxon",
    layer: str = "X",
    min_cells_per_group: int = 20,
    min_log2_fold_change: float = 0.25,
    adjusted_p_value_threshold: float = 0.05,
) -> pd.DataFrame:
    """Run exploratory cell-level Wilcoxon comparison between disjoint cohorts."""
    if method != "wilcoxon":
        raise ValueError("Only wilcoxon is currently supported")
    if len(cohort_a_mask) != adata.n_obs or len(cohort_b_mask) != adata.n_obs:
        raise ValueError("Cohort masks must align with adata.obs_names")
    if np.logical_and(cohort_a_mask, cohort_b_mask).any():
        raise ValueError("Comparison cohorts overlap; use disjoint groups")
    if (
        cohort_a_mask.sum() < min_cells_per_group
        or cohort_b_mask.sum() < min_cells_per_group
    ):
        raise ValueError("Each cohort must meet min_cells_per_group")
    matrix = _matrix_for_layer(adata, layer)
    rows: list[dict[str, Any]] = []
    for index, gene in enumerate(adata.var_names):
        values = matrix[:, index]
        dense_values = (
            np.asarray(values.toarray()).ravel()
            if hasattr(values, "toarray")
            else np.asarray(values).ravel()
        )
        values_a = dense_values[cohort_a_mask]
        values_b = dense_values[cohort_b_mask]
        statistic, p_value = mannwhitneyu(values_a, values_b, alternative="two-sided")
        mean_a = float(values_a.mean())
        mean_b = float(values_b.mean())
        fold_change = float(np.log2((mean_a + 1e-9) / (mean_b + 1e-9)))
        rows.append(
            {
                "gene": str(gene),
                "mean_expression_a": mean_a,
                "mean_expression_b": mean_b,
                "percent_expressing_a": float((values_a > 0).mean() * 100),
                "percent_expressing_b": float((values_b > 0).mean() * 100),
                "log2_fold_change": fold_change,
                "test_statistic": float(statistic),
                "p_value": float(p_value),
            }
        )
    results = pd.DataFrame(rows)
    results["adjusted_p_value"] = _adjust_p_values(results["p_value"].to_numpy())
    results["significant"] = (
        results["adjusted_p_value"] <= adjusted_p_value_threshold
    ) & (results["log2_fold_change"].abs() >= min_log2_fold_change)
    results["direction"] = np.where(
        results["log2_fold_change"] > 0, "cohort_a_higher", "cohort_b_higher"
    )
    return results.sort_values("adjusted_p_value", kind="stable").reset_index(drop=True)


def volcano_figure(
    results: pd.DataFrame, title: str = "Exploratory cohort differential expression"
) -> go.Figure:
    """Create a volcano plot for cohort-level exploratory DE results."""
    frame = results.copy()
    frame["negative_log10_adjusted_p"] = -np.log10(
        frame["adjusted_p_value"].clip(lower=1e-300)
    )
    return px.scatter(
        frame,
        x="log2_fold_change",
        y="negative_log10_adjusted_p",
        color="significant",
        hover_name="gene",
        title=title,
        labels={
            "log2_fold_change": "log2 fold change (A/B)",
            "negative_log10_adjusted_p": "-log10 adjusted p-value",
        },
    )
