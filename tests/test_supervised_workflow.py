from pathlib import Path

import anndata as ad
from scipy.sparse import csr_matrix

from bioml_workbench.single_cell.supervised import train_classifier


def make_labeled_adata() -> ad.AnnData:
    adata = ad.AnnData(
        X=csr_matrix(
            [
                [5, 0, 0],
                [4, 1, 0],
                [3, 0, 1],
                [0, 5, 0],
                [1, 4, 0],
                [0, 3, 1],
                [0, 0, 5],
                [1, 0, 4],
                [0, 1, 3],
            ]
        )
    )
    adata.obs_names = [f"cell_{index}" for index in range(adata.n_obs)]
    adata.var_names = ["gene_a", "gene_b", "gene_c"]
    adata.obs["cell_type"] = ["T"] * 3 + ["B"] * 3 + ["NK"] * 3
    return adata


def test_train_classifier_uses_held_out_cells_and_writes_artifacts(
    tmp_path: Path,
) -> None:
    result = train_classifier(
        make_labeled_adata(),
        label_column="cell_type",
        output_dir=tmp_path,
        test_size=1 / 3,
        random_state=42,
    )

    assert result["metrics"]["test_sample_count"] == 3
    assert len(result["predictions"]) == 3
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "predictions.csv").exists()
    assert (tmp_path / "model.joblib").exists()


def test_train_classifier_rejects_unlabeled_cells_when_no_labels_remain() -> None:
    adata = make_labeled_adata()
    adata.obs["cell_type"] = None

    try:
        train_classifier(adata, label_column="cell_type")
    except ValueError as exc:
        assert "No labeled cells" in str(exc)
    else:
        raise AssertionError("Expected unlabeled input to be rejected")
