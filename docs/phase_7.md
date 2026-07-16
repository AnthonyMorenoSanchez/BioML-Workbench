# Phase 7 — Machine Learning

Phase 7 provides baseline machine learning models and wrappers around common scikit-learn estimators.

## Completed work

- Replaced the pure-Python logistic regression with a scikit-learn-backed `SimpleLogisticRegression` wrapper.
- Added `BaselineClassifier` for majority-class baselines.
- Added tests for baseline and logistic regression behaviors.

## Usage

```python
from bioml_workbench.ml import BaselineClassifier, SimpleLogisticRegression

clf = SimpleLogisticRegression(n_iter=200)
clf.fit(X, y)
preds = clf.predict(X)
```

## Notes

- These implementations require `scikit-learn` in the workspace virtual environment.
- Future work: add wrapper classes for RandomForest, XGBoost, and neural network baselines using `scikit-learn` and `xgboost`.
