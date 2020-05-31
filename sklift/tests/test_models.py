import pytest
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ..models import (
    SoloModel,
    ClassTransformation,
    TwoModels
)


@pytest.mark.parametrize(
    "model",
    [
        SoloModel(LogisticRegression(), method='dummy'),
        SoloModel(LogisticRegression(), method='treatment_interaction'),
        ClassTransformation(LogisticRegression()),
        TwoModels(LogisticRegression(), LogisticRegression(), method='vanilla'),
        TwoModels(LogisticRegression(), LogisticRegression(), method='ddr_control'),
        TwoModels(LogisticRegression(), LogisticRegression(), method='ddr_treatment'),
    ]
)
def test_shape_classification(model, random_xyt_dataset_clf):
    X, y, treat = random_xyt_dataset_clf
    assert model.fit(X, y, treat).predict(X).shape[0] == y.shape[0]
    pipe = Pipeline(steps=[("scaler", StandardScaler()), ("clf", model)])
    assert pipe.fit(X, y, clf__treatment=treat).predict(X).shape[0] == y.shape[0]


@pytest.mark.parametrize(
    "model",
    [
        SoloModel(LinearRegression(), method='dummy'),
        SoloModel(LinearRegression(), method='treatment_interaction'),
        TwoModels(LinearRegression(), LinearRegression(), method='vanilla'),
        TwoModels(LinearRegression(), LinearRegression(), method='ddr_control'),
        TwoModels(LinearRegression(), LinearRegression(), method='ddr_treatment'),
    ]
)
def test_shape_regression(model, random_xy_dataset_regr):
    X, y, treat = random_xy_dataset_regr
    assert model.fit(X, y, treat).predict(X).shape[0] == y.shape[0]
    pipe = Pipeline(steps=[("scaler", StandardScaler()), ("clf", model)])
    assert pipe.fit(X, y, clf__treatment=treat).predict(X).shape[0] == y.shape[0]
