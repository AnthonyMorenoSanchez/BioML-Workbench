from __future__ import annotations

from typing import Any

import scanpy as sc


def cluster_cells(adata: Any, resolution: float = 1.0, random_state: int = 42) -> None:
    """Assign Leiden clusters from an existing AnnData neighbor graph."""
    if "connectivities" not in adata.obsp:
        raise ValueError("Run preprocess_adata before clustering cells")
    sc.tl.leiden(adata, resolution=resolution, random_state=random_state)
    adata.uns.setdefault("label_provenance", {})["leiden"] = "unsupervised_cluster"
