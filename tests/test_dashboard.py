from pathlib import Path

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
