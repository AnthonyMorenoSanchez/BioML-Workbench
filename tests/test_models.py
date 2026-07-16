from bioml_workbench.models import RandomForestWrapper, MLPWrapper


def test_random_forest_wrapper_basic():
    X = [[0.0], [1.0], [2.0], [3.0]]
    y = [0, 0, 1, 1]
    clf = RandomForestWrapper(n_estimators=10, random_state=0)
    clf.fit(X, y)
    preds = clf.predict(X)
    assert len(preds) == 4


def test_mlp_wrapper_basic():
    X = [[0.0], [1.0], [2.0], [3.0]]
    y = [0, 0, 1, 1]
    clf = MLPWrapper(max_iter=200)
    clf.fit(X, y)
    preds = clf.predict(X)
    assert len(preds) == 4
