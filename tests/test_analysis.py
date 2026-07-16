from bioml_workbench.analysis import AnalysisModule, VisualizationModule


def test_analysis_module_summarizes_features_and_metadata() -> None:
    matrix = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
    module = AnalysisModule()

    feature_summary = module.summarize_features(
        matrix, feature_names=["gene_a", "gene_b", "gene_c"]
    )
    assert feature_summary["gene_a"]["mean"] == 4.0
    assert feature_summary["gene_c"]["max"] == 9.0

    cell_summary = module.summarize_cells(matrix)
    assert cell_summary[0]["sum"] == 6.0
    assert cell_summary[2]["mean"] == 8.0

    metadata_summary = module.summarize_metadata(
        [{"cell_type": "T-cell"}, {"cell_type": "B-cell"}, {"cell_type": "T-cell"}]
    )
    assert metadata_summary["cell_type"]["counts"]["T-cell"] == 2


def test_qc_and_visualization_helpers_produce_reports() -> None:
    module = AnalysisModule()
    visualization = VisualizationModule()

    report = module.generate_qc_report([[0.0, 1.0], [2.0, 3.0]], min_total=4.0)
    assert report["sample_count"] == 2
    assert report["low_quality_samples"] == [0]

    histogram = visualization.histogram([1, 2, 2, 3], bins=2)
    assert histogram["counts"] == [2, 2]
