import anndata as ad
import numpy as np
import pytest
from scipy.sparse import csr_matrix

from bioml_workbench.single_cell.differential_expression import (
    compare_cohorts,
    volcano_figure,
)


def make_adata() -> ad.AnnData:
    adata = ad.AnnData(X=csr_matrix([[8, 0], [7, 0], [6, 1], [0, 8], [0, 7], [1, 6]]))
    adata.var_names = ["A_HIGH", "B_HIGH"]
    return adata


def test_compare_cohorts_detects_known_expression_direction() -> None:
    adata = make_adata()
    results = compare_cohorts(
        adata,
        np.array([True, True, True, False, False, False]),
        np.array([False, False, False, True, True, True]),
        min_cells_per_group=3,
        min_log2_fold_change=0.1,
    )

    a_high = results.loc[results["gene"] == "A_HIGH"].iloc[0]

    assert a_high["direction"] == "cohort_a_higher"
    assert a_high["log2_fold_change"] > 0
    assert volcano_figure(results).data


def test_compare_cohorts_rejects_overlap() -> None:
    with pytest.raises(ValueError, match="overlap"):
        compare_cohorts(
            make_adata(),
            np.array([True, True, True, False, False, False]),
            np.array([False, False, True, True, True, False]),
            min_cells_per_group=3,
        )
