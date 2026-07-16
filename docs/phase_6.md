# Phase 6 — Feature Engineering

Phase 6 implements feature-selection and dimensionality-reduction primitives using established scientific Python libraries.

## Completed work

- Replaced pure-Python variance computation and PCA with numpy and scikit-learn backed implementations.
- Added `compute_feature_variances`, `select_top_k_features`, and `simple_pca` using `numpy` and `sklearn.decomposition.PCA`.
- Added tests covering variance computation, feature selection, and PCA reduction.

## Usage

```python
from bioml_workbench.feature_engineering import compute_feature_variances, select_top_k_features, simple_pca

variances = compute_feature_variances(matrix)
selected = select_top_k_features(matrix, k=10)
reduced = simple_pca(matrix, n_components=10)
```

## Notes

- These implementations require `numpy` and `scikit-learn` installed in the workspace virtual environment.
- For large datasets, prefer incremental or out-of-core implementations (not yet implemented).
