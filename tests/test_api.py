from __future__ import annotations

from bioml_workbench.api import app


def test_api_root_and_predict() -> None:
    from fastapi.testclient import TestClient

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "BioML Workbench API is running"

    response = client.post(
        "/predict",
        json={"features": [[0.1, 0.1], [0.9, 0.9]]},
    )
    assert response.status_code == 200
    assert isinstance(response.json()["predictions"], list)
