from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def load_label_table(path: str | Path) -> pd.DataFrame:
    """Load a barcode-keyed label table from CSV or TSV."""
    label_path = Path(path)
    separator = "\t" if label_path.suffix.lower() == ".tsv" else ","
    return pd.read_csv(label_path, sep=separator)


def attach_labels(
    adata: Any,
    labels: pd.DataFrame,
    label_column: str,
    barcode_column: str = "barcode",
    provenance: str = "user_uploaded",
) -> dict[str, Any]:
    """Attach labels by barcode without reordering cells or silently dropping gaps."""
    required_columns = {barcode_column, label_column}
    missing_columns = required_columns.difference(labels.columns)
    if missing_columns:
        raise ValueError(f"Label table is missing columns: {sorted(missing_columns)}")
    if labels[barcode_column].duplicated().any():
        raise ValueError("Label table contains duplicate barcodes")

    barcode_to_label = labels.set_index(barcode_column)[label_column]
    aligned = [barcode_to_label.get(str(barcode)) for barcode in adata.obs_names]
    adata.obs[label_column] = pd.Series(aligned, index=adata.obs_names, dtype="object")
    matrix_barcodes = {str(barcode) for barcode in adata.obs_names}
    label_barcodes = {str(barcode) for barcode in labels[barcode_column]}
    unmatched_labels = sorted(label_barcodes.difference(matrix_barcodes))
    unlabeled_cells = sorted(matrix_barcodes.difference(label_barcodes))
    provenance_map = adata.uns.setdefault("label_provenance", {})
    provenance_map[label_column] = provenance

    return {
        "label_column": label_column,
        "provenance": provenance,
        "matched_labels": len(matrix_barcodes.intersection(label_barcodes)),
        "unlabeled_cells": unlabeled_cells,
        "unmatched_label_barcodes": unmatched_labels,
    }
