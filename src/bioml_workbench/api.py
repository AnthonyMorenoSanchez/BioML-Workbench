from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from .inference import InferenceService

app = FastAPI(title="BioML Workbench API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "BioML Workbench API is running"}


@app.post("/predict")
def predict(payload: dict[str, Any]) -> dict[str, Any]:
    features = payload.get("features", [])
    service = InferenceService()
    predictions = service.predict(features)
    return {"predictions": predictions}
