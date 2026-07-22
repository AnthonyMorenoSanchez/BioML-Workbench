from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression  # type: ignore[import-untyped]
from sklearn.metrics import (  # type: ignore[import-untyped]
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split  # type: ignore[import-untyped]


def train_classifier(
    adata: Any,
    label_column: str,
    output_dir: str | Path = "artifacts/runs/latest",
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train a sparse logistic classifier and evaluate it on held-out labeled cells."""
    if label_column not in adata.obs:
        raise ValueError(f"Unknown label column: {label_column}")
    labeled_mask = adata.obs[label_column].notna().to_numpy()
    if not labeled_mask.any():
        raise ValueError("No labeled cells are available for supervised training")

    labels = adata.obs.loc[labeled_mask, label_column].astype(str).to_numpy()
    class_counts = pd.Series(labels).value_counts()
    if class_counts.min() < 2:
        raise ValueError(
            "Each label class needs at least two cells for a stratified split"
        )

    matrix = adata.X[labeled_mask]
    barcode_values = adata.obs_names[labeled_mask].astype(str).to_numpy()
    train_indices, test_indices = train_test_split(
        range(len(labels)),
        test_size=test_size,
        random_state=random_state,
        stratify=labels,
    )
    train_indices = list(train_indices)
    test_indices = list(test_indices)
    model = LogisticRegression(max_iter=1_000, random_state=random_state)
    model.fit(matrix[train_indices], labels[train_indices])
    predictions = model.predict(matrix[test_indices])
    probabilities = model.predict_proba(matrix[test_indices]).max(axis=1)
    y_test = labels[test_indices]
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "f1_macro": float(f1_score(y_test, predictions, average="macro")),
        "precision_macro": float(
            precision_score(y_test, predictions, average="macro", zero_division=0)
        ),
        "recall_macro": float(
            recall_score(y_test, predictions, average="macro", zero_division=0)
        ),
        "test_sample_count": len(test_indices),
    }
    prediction_table = pd.DataFrame(
        {
            "barcode": barcode_values[test_indices],
            "actual_label": y_test,
            "predicted_label": predictions,
            "max_probability": probabilities,
        }
    )
    run_dir = Path(output_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    model_path = run_dir / "model.joblib"
    metrics_path = run_dir / "metrics.json"
    predictions_path = run_dir / "predictions.csv"
    manifest_path = run_dir / "manifest.json"
    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    prediction_table.to_csv(predictions_path, index=False)
    manifest_path.write_text(
        json.dumps(
            {
                "model": "logistic_regression",
                "label_column": label_column,
                "label_provenance": adata.uns.get("label_provenance", {}).get(
                    label_column, "unknown"
                ),
                "feature_names": [str(name) for name in adata.var_names],
                "random_state": random_state,
                "test_size": test_size,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return {
        "model": model,
        "metrics": metrics,
        "predictions": prediction_table.to_dict(orient="records"),
        "artifacts": [
            str(model_path),
            str(metrics_path),
            str(predictions_path),
            str(manifest_path),
        ],
    }
