from pathlib import Path

import anndata as ad
from scipy.sparse import csr_matrix

from bioml_workbench.single_cell.cohorts import create_cohort_definition, resolve_cohort
from bioml_workbench.single_cell.comparison import export_comparison
from bioml_workbench.single_cell.plots import cluster_size_figure


def make_adata() -> ad.AnnData:
    adata = ad.AnnData(X=csr_matrix([[0, 2], [3, 0], [2, 1], [0, 0]]))
    adata.obs_names = ["cell_a", "cell_b", "cell_c", "cell_d"]
    adata.var_names = ["NKG7", "MS4A1"]
    adata.obs["leiden"] = ["0", "1", "1", "0"]
    return adata


def test_export_comparison_writes_rules_tables_figures_and_report(
    tmp_path: Path,
) -> None:
    adata = make_adata()
    adata.obs["leiden"] = adata.obs["leiden"].astype("category")
    cohort_a = create_cohort_definition(
        "A",
        [{"type": "metadata", "column": "leiden", "operator": "in", "values": ["0"]}],
    )
    cohort_b = create_cohort_definition(
        "B",
        [{"type": "metadata", "column": "leiden", "operator": "in", "values": ["1"]}],
    )
    mask_a, _ = resolve_cohort(adata, cohort_a)
    mask_b, _ = resolve_cohort(adata, cohort_b)

    paths = export_comparison(
        tmp_path,
        adata,
        cohort_a,
        cohort_b,
        mask_a,
        mask_b,
        ["NKG7"],
        "X",
        {"clusters": cluster_size_figure(adata)},
    )

    assert Path(paths["expression_summary"]).exists()
    assert Path(paths["report"]).read_text(encoding="utf-8").startswith("# Cohort")
    assert (tmp_path / "figures" / "clusters.html").exists()
