from bioml_workbench.ml import BaselineClassifier, SimpleLogisticRegression


def test_baseline_classifier_majority_predicts() -> None:
    y = [0, 0, 1, 0]
    clf = BaselineClassifier()
    clf.fit(None, y)
    preds = clf.predict(None)
    assert all(p == 0 for p in preds)


def test_simple_logistic_regression_learns_linear_boundary() -> None:
    X = [[0.0], [1.0], [2.0], [3.0]]
    y = [0, 0, 1, 1]
    model = SimpleLogisticRegression(learning_rate=0.5, n_iter=200)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds[0] == 0
    assert preds[-1] == 1
