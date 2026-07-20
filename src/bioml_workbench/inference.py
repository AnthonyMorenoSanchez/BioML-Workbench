from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Sequence


class InferenceService:
    """Load a trained model from disk and serve predictions."""

    def __init__(self, model_path: str | Path | None = None) -> None:
        self.model_path = Path(model_path or "artifacts/model.pkl")
        self._model: Any | None = None

    def load(self) -> Any:
        if self._model is None:
            with open(self.model_path, "rb") as handle:
                self._model = pickle.load(handle)
        return self._model

    def predict(self, X: Sequence[Sequence[float]]) -> list[int]:
        model = self.load()
        return list(map(int, model.predict(X)))
