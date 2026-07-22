import anndata as ad
import numpy as np
from scipy.sparse import csr_matrix

from bioml_workbench.single_cell.plots import (
    cluster_size_figure,
    embedding_figure,
    qc_scatter_figure,
)


def make_adata() -> ad.AnnData:
    adata = ad.AnnData(X=csr_matrix([[1, 0], [0, 2], [2, 1]]))
    adata.obs_names = ["cell_a", "cell_b", "cell_c"]
    adata.var_names = ["gene_a", "gene_b"]
    adata.obs["total_counts"] = [1, 2, 3]
    adata.obs["n_genes_by_counts"] = [1, 1, 2]
    adata.obs["pct_counts_mt"] = [0.0, 0.0, 0.0]
    adata.obs["leiden"] = ["0", "1", "0"]
    adata.obsm["X_umap"] = np.array([[0.0, 1.0], [1.0, 0.0], [2.0, 1.0]])
    return adata


def test_qc_scatter_figure_returns_plotly_figure() -> None:
    figure = qc_scatter_figure(make_adata())

    assert len(figure.data) == 1
    assert figure.layout.xaxis.title.text == "Total counts"


def test_embedding_and_cluster_size_figures_use_adata_metadata() -> None:
    adata = make_adata()

    embedding = embedding_figure(adata, color_by="leiden")
    cluster_sizes = cluster_size_figure(adata)

    assert len(embedding.data) >= 1
    assert list(cluster_sizes.data[0].y) == [2, 1]
