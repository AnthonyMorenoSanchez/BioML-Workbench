import anndata as ad
from scipy.sparse import csr_matrix

from bioml_workbench.single_cell.markers import rank_marker_genes


def test_rank_marker_genes_returns_cluster_specific_table() -> None:
    adata = ad.AnnData(X=csr_matrix([[5, 0], [4, 0], [0, 5], [0, 4]]))
    adata.obs["leiden"] = ["0", "0", "1", "1"]
    adata.var_names = ["marker_0", "marker_1"]

    markers = rank_marker_genes(adata, top_n=1)

    assert set(markers["cluster"]) == {"0", "1"}
    assert len(markers) == 2
