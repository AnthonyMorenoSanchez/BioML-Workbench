from bioml_workbench.preprocessing import PreprocessingPipeline


def test_preprocessing_pipeline_runs_supported_steps() -> None:
    matrix = [[0.0, 1.0, 2.0], [1.0, 1.0, 2.0], [2.0, 3.0, 4.0]]
    pipeline = PreprocessingPipeline()

    filtered = pipeline.filter_low_quality(matrix, min_counts=4)
    assert len(filtered) == 2

    normalized = pipeline.normalize(filtered)
    assert abs(sum(normalized[0]) - 1.0) < 1e-9

    scaled = pipeline.scale(filtered)
    assert scaled[0][0] < 0.0

    selected = pipeline.select_highly_variable_features(filtered, top_k=1)
    assert len(selected["feature_names"]) == 1

    reduced = pipeline.reduce_dimensions(filtered, n_components=2)
    assert len(reduced[0]) == 2

    graph = pipeline.build_neighbor_graph(filtered, n_neighbors=1)
    assert len(graph[0]) >= 1

    umap = pipeline.run_umap_projection(filtered, n_components=2)
    assert len(umap[0]) == 2
