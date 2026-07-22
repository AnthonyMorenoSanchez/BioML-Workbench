from pathlib import Path

from bioml_workbench.data.tenx import load_tenx_matrix


def test_load_tenx_matrix_reads_sparse_matrix_and_metadata(tmp_path: Path) -> None:
    matrix_dir = tmp_path / "filtered_gene_bc_matrices" / "hg19"
    matrix_dir.mkdir(parents=True)

    (matrix_dir / "barcodes.tsv").write_text("cell_1\ncell_2\n", encoding="utf-8")
    (matrix_dir / "genes.tsv").write_text(
        "gene_1\tGene 1\tGeneType\n"
        "gene_2\tGene 2\tGeneType\n",
        encoding="utf-8",
    )
    (matrix_dir / "matrix.mtx").write_text(
        "%%MatrixMarket matrix coordinate integer general\n"
        "%\n"
        "2 2 2\n"
        "1 1 1\n"
        "2 2 2\n",
        encoding="utf-8",
    )

    payload = load_tenx_matrix(matrix_dir)

    assert payload["sample_names"] == ["cell_1", "cell_2"]
    assert payload["feature_names"] == ["gene_1", "gene_2"]
    assert payload["matrix"].shape == (2, 2)
    assert payload["matrix"][0, 0] == 1
    assert payload["matrix"][1, 1] == 2
