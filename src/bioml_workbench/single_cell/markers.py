from __future__ import annotations

from typing import Any

import pandas as pd
import scanpy as sc


def rank_marker_genes(
    adata: Any, cluster_column: str = "leiden", top_n: int = 10
) -> pd.DataFrame:
    """Rank cluster-enriched genes and return the requested top genes per cluster."""
    if cluster_column not in adata.obs:
        raise ValueError(f"Unknown cluster column: {cluster_column}")
    sc.tl.rank_genes_groups(adata, groupby=cluster_column, method="t-test")
    groups = [str(group) for group in adata.obs[cluster_column].cat.categories]
    frames = []
    for group in groups:
        frame = sc.get.rank_genes_groups_df(adata, group=group).head(top_n)
        frame["cluster"] = group
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)
