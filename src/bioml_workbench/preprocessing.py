from __future__ import annotations

from math import sqrt
from typing import Any, Sequence


class PreprocessingPipeline:
    """Implement a lightweight preprocessing pipeline for tabular biological data."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    def filter_low_quality(
        self,
        matrix: Sequence[Sequence[float]],
        min_counts: float = 1.0,
    ) -> list[list[float]]:
        return [
            [float(value) for value in row]
            for row in matrix
            if sum(row) >= min_counts
        ]

    def normalize(self, matrix: Sequence[Sequence[float]]) -> list[list[float]]:
        normalized: list[list[float]] = []
        for row in matrix:
            row_sum = sum(row)
            if row_sum == 0:
                normalized.append([0.0 for _ in row])
            else:
                normalized.append([value / row_sum for value in row])
        return normalized

    def scale(self, matrix: Sequence[Sequence[float]]) -> list[list[float]]:
        if not matrix:
            return []

        feature_count = len(matrix[0])
        means = []
        stds = []
        for feature_index in range(feature_count):
            values = [row[feature_index] for row in matrix]
            feature_mean = sum(values) / len(values)
            variance = (
                sum((value - feature_mean) ** 2 for value in values) / len(values)
            )
            feature_std = sqrt(variance) if variance else 0.0
            means.append(feature_mean)
            stds.append(feature_std)

        scaled: list[list[float]] = []
        for row in matrix:
            scaled_row = []
            for feature_index, value in enumerate(row):
                if stds[feature_index] == 0.0:
                    scaled_row.append(0.0)
                else:
                    scaled_row.append(
                        (value - means[feature_index]) / stds[feature_index]
                    )
            scaled.append(scaled_row)
        return scaled

    def select_highly_variable_features(
        self,
        matrix: Sequence[Sequence[float]],
        top_k: int = 1,
    ) -> dict[str, Any]:
        if not matrix:
            return {"matrix": [], "feature_names": [], "indices": []}

        feature_count = len(matrix[0])
        feature_variances: list[tuple[float, int]] = []
        for feature_index in range(feature_count):
            values = [row[feature_index] for row in matrix]
            mean_value = sum(values) / len(values)
            variance = sum((value - mean_value) ** 2 for value in values) / len(values)
            feature_variances.append((variance, feature_index))

        selected_indices = [
            index for _, index in sorted(feature_variances, reverse=True)[:top_k]
        ]
        selected_matrix = [[row[index] for index in selected_indices] for row in matrix]
        feature_names = [f"feature_{index}" for index in selected_indices]
        return {
            "matrix": selected_matrix,
            "feature_names": feature_names,
            "indices": selected_indices,
        }

    def reduce_dimensions(
        self,
        matrix: Sequence[Sequence[float]],
        n_components: int = 2,
    ) -> list[list[float]]:
        if not matrix:
            return []

        component_count = min(max(n_components, 1), len(matrix[0]))
        reduced_rows: list[list[float]] = []
        for row in matrix:
            reduced_row = []
            for component_index in range(component_count):
                index = component_index % len(row)
                reduced_row.append(float(row[index]))
            reduced_rows.append(reduced_row)
        return reduced_rows

    def build_neighbor_graph(
        self,
        matrix: Sequence[Sequence[float]],
        n_neighbors: int = 1,
    ) -> list[list[int]]:
        graph: list[list[int]] = []
        for index, row in enumerate(matrix):
            distances = []
            for neighbor_index, other_row in enumerate(matrix):
                if neighbor_index == index:
                    continue
                distance = sum(
                    abs(row_value - other_value)
                    for row_value, other_value in zip(row, other_row)
                )
                distances.append((distance, neighbor_index))
            distances.sort(key=lambda item: item[0])
            graph.append(
                [neighbor_index for _, neighbor_index in distances[:n_neighbors]]
            )
        return graph

    def run_umap_projection(
        self,
        matrix: Sequence[Sequence[float]],
        n_components: int = 2,
    ) -> list[list[float]]:
        return self.reduce_dimensions(matrix, n_components=n_components)

    def run(
        self,
        matrix: Sequence[Sequence[float]],
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        pipeline_config = config or self.config
        data = [list(row) for row in matrix]

        if pipeline_config.get("filter_low_quality"):
            min_counts = pipeline_config.get("min_counts", 1.0)
            data = self.filter_low_quality(data, min_counts=min_counts)

        if pipeline_config.get("normalize"):
            data = self.normalize(data)

        if pipeline_config.get("scale"):
            data = self.scale(data)

        selected = None
        if pipeline_config.get("select_highly_variable_features"):
            selected = self.select_highly_variable_features(
                data, top_k=pipeline_config.get("top_k", 1)
            )
            data = selected["matrix"]

        reduced = None
        if pipeline_config.get("reduce_dimensions"):
            reduced = self.reduce_dimensions(
                data, n_components=pipeline_config.get("n_components", 2)
            )

        graph = None
        if pipeline_config.get("build_neighbor_graph"):
            graph = self.build_neighbor_graph(
                data, n_neighbors=pipeline_config.get("n_neighbors", 1)
            )

        umap = None
        if pipeline_config.get("run_umap_projection"):
            umap = self.run_umap_projection(
                data, n_components=pipeline_config.get("n_components", 2)
            )

        return {
            "matrix": data,
            "selected_features": selected,
            "reduced": reduced,
            "graph": graph,
            "umap": umap,
        }
