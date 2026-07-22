from __future__ import annotations

from pathlib import Path
from typing import Any

from scipy.io import mmread  # type: ignore[import-untyped]


def load_tenx_matrix(path: str | Path) -> dict[str, Any]:
    """Load a legacy 10x-style sparse matrix directory 
    into a simple in-memory structure."""
    matrix_dir = Path(path)
    barcodes_path = matrix_dir / "barcodes.tsv"
    genes_path = matrix_dir / "genes.tsv"
    matrix_path = matrix_dir / "matrix.mtx"

    if not all([barcodes_path.exists(), genes_path.exists(), matrix_path.exists()]):
        raise FileNotFoundError(f"Incomplete 10x directory: {matrix_dir}")

    with barcodes_path.open("r", encoding="utf-8") as handle:
        sample_names = [line.strip() for line in handle if line.strip()]

    with genes_path.open("r", encoding="utf-8") as handle:
        feature_rows = [line.rstrip("\n").split("\t") 
                        for line in handle if line.strip()]

    feature_names = [row[0] for row in feature_rows]
    feature_metadata = [
        {
            "gene_id": row[0],
            "gene_name": row[1] if len(row) > 1 else row[0],
            "feature_type": row[2] if len(row) > 2 else "Gene Expression",
        }
        for row in feature_rows
    ]

    matrix = mmread(matrix_path)
    matrix = matrix.tocsr()
    matrix = matrix.transpose().tocsr()

    return {
        "matrix": matrix,
        "sample_names": sample_names,
        "feature_names": feature_names,
        "feature_metadata": feature_metadata,
        "path": str(matrix_dir),
    }
