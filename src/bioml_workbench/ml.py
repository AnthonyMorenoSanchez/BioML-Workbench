from __future__ import annotations

from typing import List, Sequence

from sklearn.linear_model import LogisticRegression  # type: ignore[import-untyped]


class BaselineClassifier:
    """Simple majority-class predictor."""

    def __init__(self) -> None:
        self._majority: int | None = None

    def fit(self, X: Sequence[Sequence[float]] | None, y: Sequence[int]) -> None:
        counts: dict[int, int] = {}
        for label in y:
            counts[label] = counts.get(label, 0) + 1
        self._majority = max(counts.items(), key=lambda kv: kv[1])[0]

    def predict(self, X: Sequence[Sequence[float]] | None) -> List[int]:
        if self._majority is None:
            raise RuntimeError("Model not fitted")
        n = len(X) if X is not None else 0
        return [self._majority for _ in range(n)]


class SimpleLogisticRegression:
    """Wrapper around scikit-learn LogisticRegression for binary classification."""

    def __init__(self, learning_rate: float = 0.1, n_iter: int = 1000) -> None:
        # learning_rate is retained for API compatibility but not used directly
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self._model: LogisticRegression | None = None

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> None:
        self._model = LogisticRegression(max_iter=self.n_iter)
        self._model.fit(X, y)

    def predict_proba(self, X: Sequence[Sequence[float]]) -> List[float]:
        if self._model is None:
            raise RuntimeError("Model not fitted")
        probs = self._model.predict_proba(X)
        # return probability for positive class
        return [float(p[1]) for p in probs]

    def predict(self, X: Sequence[Sequence[float]]) -> List[int]:
        if self._model is None:
            raise RuntimeError("Model not fitted")
        return list(map(int, self._model.predict(X)))
