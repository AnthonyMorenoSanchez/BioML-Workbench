from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Sequence

from sklearn.metrics import (  # type: ignore[import-untyped]
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)


def run_classification_benchmark(
    y_true: Sequence[int], y_pred: Sequence[int]
) -> dict[str, Any]:
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
        "precision": float(
            precision_score(y_true, y_pred, average="macro", zero_division=0)
        ),
        "recall": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
    }
    return metrics


def save_metrics_csv(metrics: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        for k, v in metrics.items():
            writer.writerow([k, v])
