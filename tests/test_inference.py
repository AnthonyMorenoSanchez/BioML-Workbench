from __future__ import annotations

import pickle
from pathlib import Path

from bioml_workbench.inference import InferenceService
from bioml_workbench.ml import SimpleLogisticRegression


def test_inference_service_loads_model_and_predicts(tmp_path: Path) -> None:
    model = SimpleLogisticRegression(n_iter=200)
    model.fit([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]], [0, 0, 1, 1])

    model_path = tmp_path / "model.pkl"
    with open(model_path, "wb") as handle:
        pickle.dump(model, handle)

    service = InferenceService(model_path=model_path)
    predictions = service.predict([[0.1, 0.0], [0.9, 0.9]])

    assert predictions == [0, 1]
