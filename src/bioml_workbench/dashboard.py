from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .analysis import AnalysisModule, VisualizationModule
from .data import DatasetMetadata, DatasetRegistry, DownloadManager, load_tenx_matrix
from .preprocessing import PreprocessingPipeline


def _sample_dense_matrix(
    matrix: Any, max_rows: int = 200, max_cols: int = 80
) -> list[list[float]]:
    if hasattr(matrix, "toarray"):
        if matrix.shape[0] > max_rows:
            matrix = matrix[:max_rows, :]
        if matrix.shape[1] > max_cols:
            matrix = matrix[:, :max_cols]
        return [list(row) for row in matrix.toarray().tolist()]
    return [list(row) for row in matrix]


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


def register_pbmc68k_dataset(cache_dir: str | Path | None = None) -> DatasetRegistry:
    """Register the PBMC68k sample dataset and its metadata."""
    registry = DatasetRegistry()
    metadata = DatasetMetadata(
        name="pbmc68k",
        description="Fresh 68k PBMCs Donor A sample from 10x Genomics",
        source="https://www.10xgenomics.com/datasets/fresh-68-k-pbm-cs-donor-a-1-standard-1-1-0",
        checksum=None,
        archive=True,
        expected_files=("barcodes.tsv", "genes.tsv", "matrix.mtx"),
        metadata={
            "license": "CC BY 4.0",
            "attribution": "10x Genomics",
            "format": "10x Gene Expression Matrix",
            "download_url": "https://cf.10xgenomics.com/samples/cell-exp/1.1.0/fresh_68k_pbmc_donor_a/fresh_68k_pbmc_donor_a_filtered_gene_bc_matrices.tar.gz",
        },
    )
    registry.register(metadata)
    return registry


def _resolve_tenx_matrix_dir(destination: Path) -> Path:
    candidates = [
        destination,
        destination / "filtered_gene_bc_matrices" / "hg19",
        destination / "filtered_gene_bc_matrices",
        destination / "hg19",
    ]
    for candidate in candidates:
        if (candidate / "barcodes.tsv").exists() and (candidate / "genes.tsv").exists():
            return candidate
    raise FileNotFoundError(f"Could not locate a 10x matrix directory under {destination}")


def load_pbmc68k_dataset(cache_dir: str | Path | None = None) -> dict[str, Any]:
    """Download or reuse the PBMC68k sample data and load it through the 10x loader."""
    registry = register_pbmc68k_dataset(cache_dir=cache_dir)
    metadata = registry.get("pbmc68k")
    manager = DownloadManager(cache_dir=cache_dir or "data/cache")
    destination = manager.download(
        metadata,
        destination=Path(cache_dir or "data/cache") / "pbmc68k" / "extracted",
    )
    return load_tenx_matrix(_resolve_tenx_matrix_dir(destination))


def build_dashboard_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Create the data payload consumed by the Streamlit dashboard."""
    matrix = data["matrix"]
    sample_matrix = _sample_dense_matrix(matrix)
    analysis = AnalysisModule()
    visualization = VisualizationModule()
    summaries = analysis.summarize_features(
        sample_matrix, feature_names=data["feature_names"][: len(sample_matrix[0])]
    )
    qc_report = analysis.generate_qc_report(sample_matrix)
    histograms = {
        feature_name: visualization.histogram(
            [row[index] for row in sample_matrix],
            bins=5,
        )
        for index, feature_name in enumerate(data["feature_names"][: len(sample_matrix[0])])
    }

    pipeline = PreprocessingPipeline()
    processed = pipeline.run(
        sample_matrix,
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
