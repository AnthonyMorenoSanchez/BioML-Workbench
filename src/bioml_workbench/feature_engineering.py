from __future__ import annotations

from typing import List, Sequence, cast

import numpy as np
from sklearn.decomposition import PCA  # type: ignore[import-untyped]


def compute_feature_variances(matrix: Sequence[Sequence[float]]) -> List[float]:
    if not matrix:
        return []
    arr = np.asarray(matrix, dtype=float)
    return list(np.var(arr, axis=0).tolist())


def select_top_k_features(matrix: Sequence[Sequence[float]], k: int = 1) -> dict:
    arr = np.asarray(matrix, dtype=float)
    variances = np.var(arr, axis=0)
    selected_indices = list(np.argsort(variances)[-k:][::-1].tolist())
    selected_matrix = arr[:, selected_indices].tolist()
    return {"matrix": selected_matrix, "indices": selected_indices}


def simple_pca(
    matrix: Sequence[Sequence[float]], n_components: int = 2
) -> List[List[float]]:
    if not matrix:
        return []
    arr = np.asarray(matrix, dtype=float)
    pca = PCA(n_components=min(n_components, arr.shape[1]))
    transformed = pca.fit_transform(arr)
    return cast(List[List[float]], transformed.tolist())


def incremental_pca(
    matrix: Sequence[Sequence[float]], n_components: int = 2, batch_size: int = 100
) -> List[List[float]]:
    """Incremental PCA using sklearn.IncrementalPCA for large datasets."""
    from sklearn.decomposition import IncrementalPCA

    if not matrix:
        return []
    import numpy as np

    arr = np.asarray(matrix, dtype=float)
    ipca = IncrementalPCA(n_components=min(n_components, arr.shape[1]))
    for start in range(0, arr.shape[0], batch_size):
        ipca.partial_fit(arr[start : start + batch_size])
    transformed = ipca.transform(arr)
    return cast(List[List[float]], transformed.tolist())
