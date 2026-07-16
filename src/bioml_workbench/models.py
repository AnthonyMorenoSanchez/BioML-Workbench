from __future__ import annotations

from typing import Any, List, Sequence

from sklearn.ensemble import RandomForestClassifier  # type: ignore[import-untyped]
from sklearn.neural_network import MLPClassifier  # type: ignore[import-untyped]


class RandomForestWrapper:
    """Simple wrapper for RandomForestClassifier."""

    def __init__(self, **kwargs: Any) -> None:
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

    def __init__(self, **kwargs: Any) -> None:
        try:
            from xgboost import XGBClassifier  # type: ignore[import-not-found]

            self._cls: Any = XGBClassifier
        except Exception as exc:  # pragma: no cover - environment dependent
            raise ImportError("xgboost is required for XGBoostWrapper") from exc
        self.model: Any = None
        self.kwargs: dict[str, Any] = kwargs

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> None:
        self.model = self._cls(**self.kwargs)
        self.model.fit(X, y)

    def predict(self, X: Sequence[Sequence[float]]) -> List[int]:
        if self.model is None:
            raise RuntimeError("Model not fitted")
        return list(map(int, self.model.predict(X)))


class MLPWrapper:
    """Wrapper around scikit-learn's MLPClassifier."""

    def __init__(self, **kwargs: Any) -> None:
        self.model = MLPClassifier(**kwargs)

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> None:
        self.model.fit(X, y)

    def predict(self, X: Sequence[Sequence[float]]) -> List[int]:
        return list(map(int, self.model.predict(X)))
