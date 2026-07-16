from __future__ import annotations

from collections import Counter
from statistics import mean, pstdev
from typing import Any, Sequence


class AnalysisModule:
    """Provide reusable exploratory-analysis helpers for tabular biological data."""

    def summarize_features(
        self,
        matrix: Sequence[Sequence[float]],
        feature_names: Sequence[str] | None = None,
    ) -> dict[str, dict[str, float]]:
        if not matrix:
            return {}

        feature_names = list(
            feature_names
            or [f"feature_{index}" for index in range(len(matrix[0]))]
        )
        if len(feature_names) != len(matrix[0]):
            raise ValueError("feature_names length must match the number of columns")

        summaries: dict[str, dict[str, float]] = {}
        for index, feature_name in enumerate(feature_names):
            values = [row[index] for row in matrix]
            summaries[feature_name] = {
                "count": float(len(values)),
                "mean": float(mean(values)),
                "std": float(pstdev(values)) if len(values) > 1 else 0.0,
                "min": float(min(values)),
                "max": float(max(values)),
            }
        return summaries

    def summarize_cells(
        self, matrix: Sequence[Sequence[float]]
    ) -> list[dict[str, float]]:
        return [
            {
                "sum": float(sum(row)),
                "mean": float(mean(row)) if row else 0.0,
                "count": float(len(row)),
            }
            for row in matrix
        ]

    def summarize_metadata(
        self, records: Sequence[dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        summaries: dict[str, dict[str, Any]] = {}
        for record in records:
            for key, value in record.items():
                if key not in summaries:
                    summaries[key] = {"counts": Counter()}
                summaries[key]["counts"][value] += 1

        for _key, payload in summaries.items():
            payload["counts"] = dict(payload["counts"])
        return summaries

    def generate_qc_report(
        self,
        matrix: Sequence[Sequence[float]],
        min_total: float = 0.0,
    ) -> dict[str, Any]:
        sample_totals = [sum(row) for row in matrix]
        low_quality_samples = [
            index for index, total in enumerate(sample_totals) if total < min_total
        ]
        feature_count = len(matrix[0]) if matrix else 0
        return {
            "sample_count": len(matrix),
            "feature_count": feature_count,
            "low_quality_samples": low_quality_samples,
            "sample_totals": sample_totals,
        }


class VisualizationModule:
    """Create lightweight, dependency-free visualization summaries for reports."""

    def histogram(self, values: Sequence[float], bins: int = 5) -> dict[str, Any]:
        if not values:
            return {"counts": [], "bin_edges": []}

        sorted_values = sorted(values)
        if bins <= 1:
            return {
                "counts": [len(sorted_values)],
                "bin_edges": [sorted_values[0], sorted_values[-1]],
            }

        counts = [0] * bins
        for index in range(bins):
            start = index * len(sorted_values) // bins
            end = (index + 1) * len(sorted_values) // bins
            counts[index] = end - start
        return {"counts": counts, "bin_edges": [0, len(sorted_values)]}
