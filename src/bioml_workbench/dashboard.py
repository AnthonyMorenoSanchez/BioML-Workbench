from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Sequence

from .analysis import AnalysisModule, VisualizationModule
from .preprocessing import PreprocessingPipeline


def load_tabular_data(path: str | Path) -> dict[str, Any]:
    """Load a tabular matrix from a CSV file with a sample column and feature columns."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return {"sample_names": [], "feature_names": [], "matrix": []}

    feature_names = [name for name in rows[0].keys() if name != "sample"]
    sample_names = [row["sample"] for row in rows]
    matrix = [
        [float(row[feature_name]) for feature_name in feature_names]
        for row in rows
    ]
    return {
        "sample_names": sample_names,
        "feature_names": feature_names,
        "matrix": matrix,
    }


def build_dashboard_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Create the data payload consumed by the Streamlit dashboard."""
    matrix = data["matrix"]
    analysis = AnalysisModule()
    visualization = VisualizationModule()
    summaries = analysis.summarize_features(matrix, feature_names=data["feature_names"])
    qc_report = analysis.generate_qc_report(matrix)
    histograms = {
        feature_name: visualization.histogram(
            [row[index] for row in matrix],
            bins=5,
        )
        for index, feature_name in enumerate(data["feature_names"])
    }

    pipeline = PreprocessingPipeline()
    processed = pipeline.run(
        matrix,
        config={
            "filter_low_quality": True,
            "min_counts": 0.0,
            "normalize": True,
            "scale": True,
            "select_highly_variable_features": True,
            "top_k": 2,
            "reduce_dimensions": True,
            "n_components": 2,
        },
    )

    return {
        "summary": {
            "sample_count": len(matrix),
            "feature_count": len(data["feature_names"]),
            "qc_report": qc_report,
        },
        "summaries": summaries,
        "histograms": histograms,
        "processed": processed,
        "sample_names": data["sample_names"],
        "feature_names": data["feature_names"],
    }
