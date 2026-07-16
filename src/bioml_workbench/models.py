from __future__ import annotations

from typing import List, Sequence

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier


class RandomForestWrapper:
    """Simple wrapper for RandomForestClassifier."""

    def __init__(self, **kwargs) -> None:
        self.model = RandomForestClassifier(**kwargs)

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> None:
        self.model.fit(X, y)

    def predict(self, X: Sequence[Sequence[float]]) -> List[int]:
        return list(map(int, self.model.predict(X)))


class XGBoostWrapper:
    """
    Wrapper for XGBoost classifier; raises informative error if xgboost
    is not installed.
    """

    def __init__(self, **kwargs) -> None:
        try:
            from xgboost import XGBClassifier

            self._cls = XGBClassifier
        except Exception as exc:  # pragma: no cover - environment dependent
            raise ImportError("xgboost is required for XGBoostWrapper") from exc
        self.model = None
        self.kwargs = kwargs

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> None:
        self.model = self._cls(**self.kwargs)
        self.model.fit(X, y)

    def predict(self, X: Sequence[Sequence[float]]) -> List[int]:
        if self.model is None:
            raise RuntimeError("Model not fitted")
        return list(map(int, self.model.predict(X)))


class MLPWrapper:
    """Wrapper around scikit-learn's MLPClassifier."""

    def __init__(self, **kwargs) -> None:
        self.model = MLPClassifier(**kwargs)

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> None:
        self.model.fit(X, y)

    def predict(self, X: Sequence[Sequence[float]]) -> List[int]:
        return list(map(int, self.model.predict(X)))
