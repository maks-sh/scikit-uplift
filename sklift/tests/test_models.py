import warnings

import pytest
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ..models import (
    SoloModel,
    ClassTransformation,
    ClassTransformationReg,
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

@pytest.mark.parametrize(
    "model",
    [
        SoloModel(LogisticRegression(), method='dummy'),
        SoloModel(LogisticRegression(), method='treatment_interaction'),
    ]
)    		            	
def test_solomodel_fit_error(model):
	X, y, treatment = [[1., 0., 0.],[1., 0., 0.],[1., 0., 0.]], [1., 2., 3.], [0., 1., 0.]
	with pytest.raises(TypeError):
		model.fit(X, y, treatment)	

@pytest.mark.parametrize(
    "model",
    [
        SoloModel(LogisticRegression(), method='dummy'),
        SoloModel(LogisticRegression(), method='treatment_interaction'),
    ]
)    		            	
def test_solomodel_pred_error(model):
	X_train, y_train, treat_train = (np.array([[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2]]),
                                     np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 1.0]))
	model.fit(X_train, y_train, treat_train)	
	with pytest.raises(TypeError):			
		model.predict(1)		
		
@pytest.mark.parametrize("method", ['method'])
def test_solomodel_method_error(method):
	with pytest.raises(ValueError):
		SoloModel(LogisticRegression(), method=method)	

def test_classtransformation_fit_error():
	X, y, treatment = [[1., 0., 0.],[1., 0., 0.],[1., 0., 0.]], [1., 2., 3.], [0., 1., 0.]
	with pytest.raises(ValueError):
		ClassTransformation(LogisticRegression()).fit(X, y, treatment)			
		
@pytest.mark.parametrize("method", ['method'])
def test_twomodels_method_error(method):
	with pytest.raises(ValueError):
		TwoModels(LinearRegression(), LinearRegression(), method=method)					
		
def test_same_estimator_error():
	est = LinearRegression()
	with pytest.raises(ValueError):
		TwoModels(est, est)

@pytest.mark.parametrize(
    "X, y, treatment",
    [
        (pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),columns=['a', 'b', 'c'], index=[0,1,2]), 
            pd.Series(np.array([1, 0, 1]),index=[0,2,3]), pd.Series(np.array([0, 0, 1]),index=[0,1,2])),
        (pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),columns=['a', 'b', 'c'], index=[0,1,2]), 
            pd.Series(np.array([1, 0, 1]),index=[0,1,2]), pd.Series(np.array([0, 0, 1]),index=[1,2,3]))
    ]
)
def test_input_data(X, y, treatment):
    model = TwoModels(LinearRegression(), LinearRegression())
    with pytest.warns(UserWarning):
        model.fit(X, y, treatment)


@pytest.mark.parametrize("propensity", ['constant', 'estimated'])
@pytest.mark.parametrize("array_type", ['list', 'tuple', 'series'])
def test_classtransformation_reg_array_like(propensity, array_type):
    X = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.],
                  [2., 0.], [2., 1.], [3., 0.], [3., 1.]])
    y = np.array([1., 3., 2., 5., 4., 7., 6., 9.])
    treatment = np.array([0, 1, 0, 1, 1, 0, 1, 0])
    if propensity == 'constant':
        kwargs = {'propensity_val': 0.4}
        p = 0.4
    else:
        kwargs = {'propensity_estimator': LogisticRegression()}
        p = LogisticRegression().fit(X, treatment).predict_proba(X)[:, 1]
    expected = LinearRegression().fit(X, y * (treatment - p) / (p * (1 - p)))

    if array_type == 'series':
        y_input = pd.Series(y, index=np.arange(8) + 20)
        treatment_input = pd.Series(treatment, index=np.arange(8) + 40)
    else:
        constructor = list if array_type == 'list' else tuple
        y_input, treatment_input = constructor(y), constructor(treatment)
    model = ClassTransformationReg(LinearRegression(), **kwargs)
    result = model.fit(X, y_input, treatment_input).predict(X)

    np.testing.assert_allclose(result, expected.predict(X))
    np.testing.assert_array_equal(y_input, y)
    np.testing.assert_array_equal(treatment_input, treatment)
