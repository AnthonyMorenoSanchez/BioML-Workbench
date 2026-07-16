from bioml_workbench.feature_engineering import (
    compute_feature_variances,
    select_top_k_features,
    simple_pca,
)


def test_feature_variances_and_selection() -> None:
    matrix = [[1, 2, 3], [2, 3, 4], [10, 11, 12]]
    variances = compute_feature_variances(matrix)
    assert len(variances) == 3
    top = select_top_k_features(matrix, k=1)
    assert top["indices"] == [2]


def test_simple_pca_reduces_dimensions() -> None:
    matrix = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    reduced = simple_pca(matrix, n_components=1)
    assert len(reduced) == 3
    assert len(reduced[0]) == 1
