import sys
from pathlib import Path
from types import SimpleNamespace

from bioml_workbench import dashboard
from bioml_workbench.dashboard import build_dashboard_payload, load_tabular_data


def test_load_tabular_data_parses_csv(tmp_path: Path) -> None:
    data_path = tmp_path / "matrix.csv"
    data_path.write_text(
        "sample,gene_a,gene_b\ncell_1,1.5,0.7\ncell_2,2.0,1.3\n",
        encoding="utf-8",
    )

    payload = load_tabular_data(data_path)

    assert payload["sample_names"] == ["cell_1", "cell_2"]
    assert payload["feature_names"] == ["gene_a", "gene_b"]
    assert payload["matrix"][0][0] == 1.5
    assert payload["matrix"][1][1] == 1.3


def test_load_pbmc68k_dataset_reuses_h5ad_cache(
    monkeypatch, tmp_path: Path
) -> None:
    cache_path = tmp_path / "pbmc68k" / "pbmc68k.h5ad"
    cache_path.parent.mkdir(parents=True)
    cache_path.touch()
    expected = SimpleNamespace(
        X=[[1.0]],
        obs_names=["cell_1"],
        var_names=["gene_1"],
        var=SimpleNamespace(
            reset_index=lambda: SimpleNamespace(to_dict=lambda orient: [])
        ),
    )
    read_calls: list[Path] = []
    fake_anndata = SimpleNamespace(
        read_h5ad=lambda path: read_calls.append(Path(path)) or expected
    )
    fake_scvelo = SimpleNamespace(
        datasets=SimpleNamespace(
            pbmc68k=lambda: (_ for _ in ()).throw(AssertionError()))
    )
    monkeypatch.setitem(sys.modules, "anndata", fake_anndata)
    monkeypatch.setitem(sys.modules, "scvelo", fake_scvelo)

    payload = dashboard.load_pbmc68k_dataset(tmp_path)

    assert read_calls == [cache_path]
    assert payload["sample_names"] == ["cell_1"]


def test_build_dashboard_payload_returns_summary_and_figures(tmp_path: Path) -> None:
    data_path = tmp_path / "matrix.csv"
    data_path.write_text(
        "sample,gene_a,gene_b\ncell_1,1.5,0.7\ncell_2,2.0,1.3\ncell_3,3.0,2.1\n",
        encoding="utf-8",
    )

    payload = build_dashboard_payload(load_tabular_data(data_path))

    assert payload["summary"]["sample_count"] == 3
    assert payload["summary"]["feature_count"] == 2
    assert "histograms" in payload
    assert payload["histograms"]["gene_a"]["counts"]
