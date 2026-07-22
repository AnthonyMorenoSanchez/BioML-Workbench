from __future__ import annotations

from typing import Any, cast

import numpy as np
from scipy.sparse import issparse  # type: ignore[import-untyped]


def _row_sums(matrix: Any) -> np.ndarray:
    return cast(np.ndarray, np.asarray(matrix.sum(axis=1)).ravel())


def _detected_genes(matrix: Any) -> np.ndarray:
    if issparse(matrix):
        return cast(np.ndarray, np.asarray(matrix.getnnz(axis=1)).ravel())
    return cast(np.ndarray, np.count_nonzero(matrix, axis=1))


def calculate_qc_metrics(adata: Any, mitochondrial_prefix: str = "MT-") -> None:
    """Add sparse-aware per-cell count, detected-gene, and mitochondrial metrics."""
    if "counts" not in adata.layers:
        adata.layers["counts"] = adata.X.copy()

    counts = adata.layers["counts"]
    total_counts = _row_sums(counts)
    mitochondrial_mask = np.asarray(
        [
            str(name).upper().startswith(mitochondrial_prefix.upper())
            for name in adata.var_names
        ]
    )
    mitochondrial_counts = _row_sums(counts[:, mitochondrial_mask])
    adata.var["mt"] = mitochondrial_mask
    adata.obs["total_counts"] = total_counts
    adata.obs["n_genes_by_counts"] = _detected_genes(counts)
    adata.obs["pct_counts_mt"] = (
        np.divide(
            mitochondrial_counts,
            total_counts,
            out=np.zeros_like(total_counts, dtype=float),
            where=total_counts > 0,
        )
        * 100
    )
