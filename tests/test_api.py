from __future__ import annotations

from types import SimpleNamespace

from fastapi.testclient import TestClient

from bioml_workbench.api import app
from bioml_workbench.inference import InferenceService


def test_api_root_and_predict(monkeypatch) -> None:
    fake_model = SimpleNamespace(predict=lambda X: [0 for _ in X])
    monkeypatch.setattr(InferenceService, "load", lambda self: fake_model)

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "BioML Workbench API is running"

    response = client.post(
        "/predict",
        json={"features": [[0.1, 0.1], [0.9, 0.9]]},
    )
    assert response.status_code == 200
    assert response.json()["predictions"] == [0, 0]
