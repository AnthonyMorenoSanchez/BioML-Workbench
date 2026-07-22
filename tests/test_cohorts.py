from pathlib import Path

import anndata as ad
from scipy.sparse import csr_matrix

from bioml_workbench.single_cell.cohorts import (
    create_cohort_definition,
    load_cohort_definition,
    resolve_cohort,
    save_cohort_definition,
    summarize_cohort,
)
from bioml_workbench.single_cell.expression import expression_summary


def make_adata() -> ad.AnnData:
    adata = ad.AnnData(X=csr_matrix([[0, 2], [3, 0], [2, 1], [0, 0]]))
    adata.obs_names = ["cell_a", "cell_b", "cell_c", "cell_d"]
    adata.var_names = ["NKG7", "MS4A1"]
    adata.obs["leiden"] = ["0", "1", "1", "0"]
    adata.obs["pct_counts_mt"] = [5.0, 12.0, 25.0, 2.0]
    return adata


def test_resolve_cohort_combines_sparse_gene_metadata_and_qc_filters() -> None:
    definition = create_cohort_definition(
        "NK-like",
        filters=[
            {"type": "metadata", "column": "leiden", "operator": "in", "values": ["1"]},
            {"type": "gene", "gene": "NKG7", "operator": ">=", "value": 2},
            {"type": "qc", "column": "pct_counts_mt", "operator": "<", "value": 20},
        ],
    )

    mask, report = resolve_cohort(make_adata(), definition)

    assert mask.tolist() == [False, True, False, False]
    assert report["cell_count"] == 1
    assert report["layer"] == "X"


def test_resolve_cohort_supports_barcode_and_not_logic() -> None:
    definition = create_cohort_definition(
        "Exclude cell b",
        filters=[
            {"type": "barcode", "operator": "in", "values": ["cell_a", "cell_b"]},
            {"type": "barcode", "operator": "not_in", "values": ["cell_b"]},
        ],
        logic="AND",
    )

    mask, _ = resolve_cohort(make_adata(), definition)

    assert mask.tolist() == [True, False, False, False]


def test_cohort_save_load_and_expression_summary(tmp_path: Path) -> None:
    definition = create_cohort_definition(
        "Cluster one",
        filters=[
            {
                "type": "metadata",
                "column": "leiden",
                "operator": "in",
                "values": ["1"],
            }
        ],
    )
    path = save_cohort_definition(definition, tmp_path / "cohort.json")
    restored = load_cohort_definition(path)
    adata = make_adata()
    mask, _ = resolve_cohort(adata, restored)
    summary = summarize_cohort(adata, mask)
    expression = expression_summary(adata, ["NKG7"], {"cluster_one": mask})

    assert restored == definition
    assert summary["cell_count"] == 2
    assert expression.loc[0, "mean_expression"] == 2.5


def test_unknown_gene_reports_suggestion() -> None:
    definition = create_cohort_definition(
        "bad gene",
        filters=[{"type": "gene", "gene": "NKG8", "operator": ">", "value": 0}],
    )

    try:
        resolve_cohort(make_adata(), definition)
    except ValueError as exc:
        assert "NKG7" in str(exc)
    else:
        raise AssertionError("Unknown genes must be rejected")
