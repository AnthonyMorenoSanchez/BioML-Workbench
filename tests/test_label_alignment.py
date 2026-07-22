import anndata as ad
import pandas as pd
import pytest
from scipy.sparse import csr_matrix

from bioml_workbench.data.annotations import attach_labels


def make_adata() -> ad.AnnData:
    adata = ad.AnnData(X=csr_matrix([[1, 0], [0, 1], [1, 1]]))
    adata.obs_names = ["cell_a", "cell_b", "cell_c"]
    adata.var_names = ["gene_a", "gene_b"]
    return adata


def test_attach_labels_aligns_by_barcode_and_records_provenance() -> None:
    adata = make_adata()
    labels = pd.DataFrame(
        {"barcode": ["cell_c", "cell_a", "other"], "cell_type": ["NK", "T", "B"]}
    )

    report = attach_labels(
        adata,
        labels,
        label_column="cell_type",
        provenance="published_10x_reference",
    )

    assert adata.obs.loc["cell_a", "cell_type"] == "T"
    assert adata.obs.loc["cell_b", "cell_type"] is None
    assert report["matched_labels"] == 2
    assert report["unmatched_label_barcodes"] == ["other"]
    assert adata.uns["label_provenance"]["cell_type"] == "published_10x_reference"


def test_attach_labels_rejects_duplicate_barcodes() -> None:
    labels = pd.DataFrame({"barcode": ["cell_a", "cell_a"], "cell_type": ["T", "B"]})

    with pytest.raises(ValueError, match="duplicate barcodes"):
        attach_labels(make_adata(), labels, label_column="cell_type")
