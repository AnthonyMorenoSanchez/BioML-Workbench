import anndata as ad
import numpy as np
from scipy.sparse import csr_matrix

from bioml_workbench.single_cell.clustering import cluster_cells
from bioml_workbench.single_cell.preprocessing import preprocess_adata
from bioml_workbench.single_cell.qc import calculate_qc_metrics


def make_adata() -> ad.AnnData:
    """Return a small, sparse cell-by-gene fixture for single-cell tests."""
    adata = ad.AnnData(
        X=csr_matrix(
            [
                [1, 0, 3, 0],
                [0, 2, 1, 0],
                [4, 0, 0, 1],
                [1, 1, 1, 1],
                [0, 3, 0, 2],
                [2, 0, 2, 1],
            ]
        )
    )
    adata.obs_names = [f"cell_{index}" for index in range(adata.n_obs)]
    adata.var_names = ["MT-CO1", "gene_b", "gene_c", "gene_d"]
    return adata


def test_calculate_qc_metrics_preserves_sparse_counts() -> None:
    adata = make_adata()

    calculate_qc_metrics(adata)

    assert "total_counts" in adata.obs
    assert "n_genes_by_counts" in adata.obs
    assert "pct_counts_mt" in adata.obs
    assert adata.obs.loc["cell_0", "total_counts"] == 4
    assert adata.layers["counts"].format == "csr"


def test_preprocess_adata_creates_standard_analysis_slots() -> None:
    adata = make_adata()

    processed = preprocess_adata(
        adata,
        min_genes=1,
        min_cells_per_gene=1,
        n_top_genes=3,
        n_pcs=2,
        n_neighbors=2,
        random_state=42,
    )

    assert processed.layers["counts"].format == "csr"
    assert "highly_variable" in processed.var
    assert processed.obsm["X_pca"].shape == (processed.n_obs, 2)
    assert "connectivities" in processed.obsp
    assert processed.obsm["X_umap"].shape == (processed.n_obs, 2)
    assert np.isfinite(processed.obsm["X_umap"]).all()


def test_cluster_cells_adds_unsupervised_cluster_metadata() -> None:
    adata = make_adata()
    processed = preprocess_adata(
        adata,
        min_genes=1,
        min_cells_per_gene=1,
        n_top_genes=3,
        n_pcs=2,
        n_neighbors=2,
        random_state=42,
    )

    cluster_cells(processed, resolution=0.5, random_state=42)

    assert "leiden" in processed.obs
    assert processed.obs["leiden"].notna().all()
    assert processed.uns["label_provenance"]["leiden"] == "unsupervised_cluster"
