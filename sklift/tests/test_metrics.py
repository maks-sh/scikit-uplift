import pytest

import numpy as np

from sklearn.tree import DecisionTreeClassifier
from ..models import SoloModel

from sklearn.utils._testing import assert_array_almost_equal

from ..metrics import make_uplift_scorer
from ..metrics import uplift_curve, uplift_auc_score, perfect_uplift_curve
from ..metrics import qini_curve, qini_auc_score, perfect_qini_curve
from ..metrics import (uplift_at_k, response_rate_by_percentile,
                       weighted_average_uplift, uplift_by_percentile, treatment_balance_curve, average_squared_deviation)


def make_predictions(binary):
    X_train, y_train, treat_train = (np.array([[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2]]),
                                     np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 1.0]))
    X_val, y_val, treat_val = (np.array([[5.1, 3.4, 1.5, 0.2], [5.0, 3.5, 1.3, 0.3], [4.5, 2.3, 1.3, 0.3]]),
                               np.array([0.0, 1.0, 0.0]), np.array([0.0, 1.0, 1.0]))

    if not binary:
        y_train, y_val = (np.array([2.0, 0.0, 1.0]), np.array([0.0, 1.0, 2.0]))

    model = DecisionTreeClassifier(random_state=0)

    s_model = SoloModel(model)
    s_model = s_model.fit(X_train, y_train, treat_train)
    uplift_preds = s_model.predict(X_val)

    return y_val, uplift_preds, treat_val


@pytest.mark.parametrize(
    "binary, test_x_actual, test_y_actual",
    [
        (True, np.array([0, 3]), np.array([0, 1.5, ])),
        (False, np.array([0, 2, 3]), np.array([0.0, 3, 4.5]))
    ]
)
def test_uplift_curve(binary, test_x_actual, test_y_actual):
    y_true, uplift, treatment = make_predictions(binary)

    if binary == False:
        with pytest.raises(Exception):
            x_actual, y_actual = uplift_curve(y_true, uplift, treatment)
    else:
        x_actual, y_actual = uplift_curve(y_true, uplift, treatment)

        assert_array_almost_equal(x_actual, test_x_actual)
        assert_array_almost_equal(y_actual, test_y_actual)
        assert x_actual.shape == y_actual.shape


def test_uplift_curve_hard():
    with pytest.raises(Exception):
        y_true, uplift, treatment = make_predictions(binary=True)
        y_true = np.zeros(y_true.shape)

        x_actual, y_actual = uplift_curve(y_true, uplift, treatment)

        assert_array_almost_equal(x_actual, np.array([0, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0]))

        y_true = np.ones(y_true.shape)

        x_actual, y_actual = uplift_curve(y_true, uplift, treatment)

        assert_array_almost_equal(x_actual, np.array([0, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0]))


@pytest.mark.parametrize(
    "binary, test_x_actual, test_y_actual",
    [
        (True, np.array([0, 1, 2, 3]), np.array([0., 1., 2., 1.5])),
        (False, np.array([0, 1, 2, 3]), np.array([0., 1., 2., 4.5]))
    ]
)
def test_perfect_uplift_curve(binary, test_x_actual, test_y_actual):
    y_true, uplift, treatment = make_predictions(binary)
    if binary == False:
        with pytest.raises(Exception):
            x_actual, y_actual = perfect_uplift_curve(y_true, treatment)
    else:
        x_actual, y_actual = perfect_uplift_curve(y_true, treatment)
        assert_array_almost_equal(x_actual, test_x_actual)
        assert_array_almost_equal(y_actual, test_y_actual)
        assert x_actual.shape == y_actual.shape


def test_perfect_uplift_curve_hard():
    with pytest.raises(Exception):
        y_true, uplift, treatment = make_predictions(binary=True)
        y_true = np.zeros(y_true.shape)

        x_actual, y_actual = perfect_uplift_curve(y_true, treatment)

        assert_array_almost_equal(x_actual, np.array([0, 1, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0, 0.0]))

        y_true = np.ones(y_true.shape)

        x_actual, y_actual = perfect_uplift_curve(y_true, treatment)

        assert_array_almost_equal(x_actual, np.array([0, 2, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 2.0, 0.0]))


def test_uplift_auc_score():
    y_true = [0, 1]
    uplift = [0.1, 0.3]
    treatment = [1, 0]
    assert_array_almost_equal(uplift_auc_score(y_true, uplift, treatment), 0.)

    y_true = [1, 0]
    uplift = [0.1, 0.3]
    treatment = [0, 1]
    assert_array_almost_equal(uplift_auc_score(y_true, uplift, treatment), 1.)

    with pytest.raises(Exception):
        y_true = [1, 1]
        uplift = [0.1, 0.3]
        treatment = [0, 1]
        assert_array_almost_equal(uplift_auc_score(y_true, uplift, treatment), 1.)

        y_true = [1, 1]
        uplift = [0.1, 0.3]
        treatment = [1, 0]
        assert_array_almost_equal(uplift_auc_score(y_true, uplift, treatment), -1.)

        y_true = [0, 1, 2]
        uplift = [0.1, 0.3, 0.9]
        treatment = [0, 1, 0]
        assert_array_almost_equal(uplift_auc_score(y_true, uplift, treatment), -1.333333)

        y_true = [0, 1, 2]
        uplift = [0.1, 0.3, 0.9]
        treatment = [1, 0, 1]
        assert_array_almost_equal(uplift_auc_score(y_true, uplift, treatment), 1.333333)


@pytest.mark.parametrize(
    "binary, test_x_actual, test_y_actual",
    [
        (True, np.array([0, 3]), np.array([0, 1., ])),
        (False, np.array([0, 2, 3]), np.array([0., 3, 3.]))
    ]
)
def test_qini_curve(binary, test_x_actual, test_y_actual):
    y_true, uplift, treatment = make_predictions(binary)

    if binary == False:
        with pytest.raises(Exception):    
            x_actual, y_actual = qini_curve(y_true, uplift, treatment)
    else:
        x_actual, y_actual = qini_curve(y_true, uplift, treatment)
        assert_array_almost_equal(x_actual, test_x_actual)
        assert_array_almost_equal(y_actual, test_y_actual)
        assert x_actual.shape == y_actual.shape


def test_qini_curve_hard():
    with pytest.raises(Exception):
        y_true, uplift, treatment = make_predictions(binary=True)
        y_true = np.zeros(y_true.shape)

        x_actual, y_actual = qini_curve(y_true, uplift, treatment)

        assert_array_almost_equal(x_actual, np.array([0, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0]))

        y_true = np.ones(y_true.shape)

        x_actual, y_actual = qini_curve(y_true, uplift, treatment)

        assert_array_almost_equal(x_actual, np.array([0, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0]))


@pytest.mark.parametrize(
    "binary, negative_effect, test_x_actual, test_y_actual",
    [
        (True, True, np.array([0, 1, 3]), np.array([0., 1., 1.])),
        (True, False, np.array([0., 1., 3.]), np.array([0., 1., 1.])),
    ]
)
def test_perfect_qini_curve(binary, negative_effect, test_x_actual, test_y_actual):
    y_true, uplift, treatment = make_predictions(binary)

    x_actual, y_actual = perfect_qini_curve(y_true, treatment, negative_effect=negative_effect)

    assert_array_almost_equal(x_actual, test_x_actual)
    assert_array_almost_equal(y_actual, test_y_actual)
    assert x_actual.shape == y_actual.shape


def test_perfect_qini_curve_hard():
    with pytest.raises(Exception):
        y_true, uplift, treatment = make_predictions(binary=True)
        y_true = np.zeros(y_true.shape)

        x_actual, y_actual = perfect_qini_curve(y_true, treatment, negative_effect=True)

        assert_array_almost_equal(x_actual, np.array([0, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0]))

        x_actual, y_actual = perfect_qini_curve(y_true, treatment, negative_effect=False)

        assert_array_almost_equal(x_actual, np.array([0., 0., 3.]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0, 0.0]))

        y_true = np.ones(y_true.shape)

        x_actual, y_actual = perfect_qini_curve(y_true, treatment, negative_effect=True)

        assert_array_almost_equal(x_actual, np.array([0, 2, 3]))
        assert_array_almost_equal(y_actual, np.array([0.0, 2.0, 0.0]))

        x_actual, y_actual = perfect_qini_curve(y_true, treatment, negative_effect=False)

        assert_array_almost_equal(x_actual, np.array([0., 0., 3.]))
        assert_array_almost_equal(y_actual, np.array([0.0, 0.0, 0.0]))
 
def test_perfect_qini_curve_error():
	y_true, uplift, treatment = make_predictions(binary=True)
	with pytest.raises(TypeError):
		perfect_qini_curve(y_true, treatment, negative_effect=5)
        


def test_qini_auc_score():
    y_true = [0, 1]
    uplift = [0.1, 0.3]
    treatment = [1, 0]
    assert_array_almost_equal(qini_auc_score(y_true, uplift, treatment), 1.)

    y_true = [1, 0]
    uplift = [0.1, 0.3]
    treatment = [0, 1]
    assert_array_almost_equal(qini_auc_score(y_true, uplift, treatment), 1.)

    with pytest.raises(Exception):
        y_true = [1, 1]
        uplift = [0.1, 0.3]
        treatment = [0, 1]
        assert_array_almost_equal(qini_auc_score(y_true, uplift, treatment), 1.)

        y_true = [1, 1]
        uplift = [0.1, 0.3]
        treatment = [1, 0]
        assert_array_almost_equal(qini_auc_score(y_true, uplift, treatment), 0.)

        y_true = [0, 1, 2]
        uplift = [0.1, 0.3, 0.9]
        treatment = [0, 1, 0]
        assert_array_almost_equal(qini_auc_score(y_true, uplift, treatment), -0.5)

        y_true = [0, 1, 2]
        uplift = [0.1, 0.3, 0.9]
        treatment = [1, 0, 1]
        assert_array_almost_equal(qini_auc_score(y_true, uplift, treatment), 0.75)

def test_qini_auc_score_error():
	y_true = [1, 0]
	uplift = [0.1, 0.3]
	treatment = [0, 1]
	with pytest.raises(TypeError):
		qini_auc_score(y_true, uplift, treatment, negative_effect=5)        


def test_uplift_at_k():
    y_true, uplift, treatment = make_predictions(binary=True)

    assert_array_almost_equal(uplift_at_k(y_true, uplift, treatment, strategy='by_group', k=1), np.array([0.]))
    #assert_array_almost_equal(uplift_at_k(y_true, uplift, treatment, strategy='overall', k=2), np.array([0.]))

@pytest.mark.parametrize(
    "strategy, k",
    [
        ('new_strategy', 1),
        ('by_group', -0.5),
        ('by_group', '1'),
        ('by_group', 2)
    ]
)
def test_uplift_at_k_errors(strategy, k):
	y_true, uplift, treatment = make_predictions(binary=True)
	with pytest.raises(ValueError):
		uplift_at_k(y_true, uplift, treatment, strategy, k)


@pytest.mark.parametrize(
    "strategy, group, response_rate",
    [
        ('overall', 'treatment', np.array([[0.5], [0.125], [2.]])),
        ('by_group', 'treatment', np.array([[0.5], [0.125], [2.]])),
        ('overall', 'control', np.array([[0.], [0.], [1.]])),
        ('by_group', 'control', np.array([[0.], [0.], [1.]]))
    ]
)
def test_response_rate_by_percentile(strategy, group, response_rate):
    y_true, uplift, treatment = make_predictions(binary=True)

    assert_array_almost_equal(response_rate_by_percentile(y_true, uplift, treatment, group, strategy, bins=1),
                              response_rate)

@pytest.mark.parametrize(
    "strategy, group, bins",
    [
        ('new_strategy', 'control', 1),
        ('by_group', 'ctrl', 1),
        ('by_group', 'control', 0.5),
        ('by_group', 'control', 9999)
    ]
)
def test_response_rate_by_percentile_errors(strategy, group, bins):
    y_true, uplift, treatment = make_predictions(binary=True)
    with pytest.raises(ValueError):
    	response_rate_by_percentile(y_true, uplift, treatment, group=group, strategy=strategy, bins=bins)

@pytest.mark.parametrize(
    "strategy, weighted_average",
    [
        ('overall', 0.5),
        ('by_group', 0.5)
    ]
)
def test_weighted_average_uplift(strategy, weighted_average):
    y_true, uplift, treatment = make_predictions(binary=True)

    assert_array_almost_equal(weighted_average_uplift(y_true, uplift, treatment, strategy, bins=1), weighted_average)
    

@pytest.mark.parametrize(
    "strategy, bins",
    [
        ('new_strategy', 1),
        ('by_group', 0.5),
        ('by_group', 9999)
    ]
)
def test_weighted_average_uplift_errors(strategy, bins):
	y_true, uplift, treatment = make_predictions(binary=True)
	with pytest.raises(ValueError):
		weighted_average_uplift(y_true, uplift, treatment, strategy=strategy, bins=bins)
    

@pytest.mark.parametrize(
    "strategy, bins, std, total, string_percentiles, data",
    [
        ('overall', 1, False, False, False, np.array([[2., 1., 0.5, 0., 0.5]])),
        ('overall', 1, True, True, True, np.array([[2., 1., 0.5, 0., 0.5, 0.353553, 0., 0.353553],
                                                   [2., 1., 0.5, 0., 0.5, 0.353553, 0., 0.353553]])),
        ('by_group', 1, False, False, False, np.array([[2., 1., 0.5, 0., 0.5]])),
        ('by_group', 1, True, True, True, np.array([[2., 1., 0.5, 0., 0.5, 0.353553, 0., 0.353553],
                                                    [2., 1., 0.5, 0., 0.5, 0.353553, 0., 0.353553]]))
    ]
)
def test_uplift_by_percentile(strategy, bins, std, total, string_percentiles, data):
    y_true, uplift, treatment = make_predictions(binary=True)

    assert_array_almost_equal(
        uplift_by_percentile(y_true, uplift, treatment, strategy, bins, std, total, string_percentiles), data)
        
@pytest.mark.parametrize(
    "strategy, bins, std, total, string_percentiles",
    [
        ('new_strategy', 1, True, True, True),
        ('by_group', 0.5, True, True, True),
        ('by_group', 9999, True, True, True),
        ('by_group', 1, 2, True, True),
        ('by_group', 1, True, True, 2),
        ('by_group', 1, True, 2, True)
    ]
)
def test_uplift_by_percentile_errors(strategy, bins, std, total, string_percentiles):
	y_true, uplift, treatment = make_predictions(binary=True)
	with pytest.raises(ValueError):
		uplift_by_percentile(y_true, uplift, treatment, strategy, bins, std, total, string_percentiles)        


def test_treatment_balance_curve():
    y_true, uplift, treatment = make_predictions(binary=True)

    idx, balance = treatment_balance_curve(uplift, treatment, winsize=2)
    assert_array_almost_equal(idx, np.array([1., 100.]))
    assert_array_almost_equal(balance, np.array([1., 0.5]))

@pytest.mark.parametrize(
    "strategy",
    [
        ('overall'),
        ('by_group')
    ]
)    
def test_average_squared_deviation(strategy):
	y_true, uplift, treatment = make_predictions(binary=True)
	assert (average_squared_deviation(y_true, uplift, treatment, y_true, uplift, treatment, strategy, bins=1) == 0)

@pytest.mark.parametrize(
    "strategy, bins",
    [
        ('new_strategy', 1),
        ('by_group', 0.5),
        ('by_group', 9999)
    ]
)    
def test_average_squared_deviation_errors(strategy, bins):
	y_true, uplift, treatment = make_predictions(binary=True)
	with pytest.raises(ValueError):
		average_squared_deviation(y_true, uplift, treatment, y_true, uplift, treatment, strategy=strategy, bins=bins)
 	
def test_metric_name_error():
	with pytest.raises(ValueError):
		make_uplift_scorer('new_scorer', [0, 1])
		
def test_make_scorer_error():
	with pytest.raises(TypeError):
		make_uplift_scorer('qini_auc_score', [])	

    
 

	    


			
			  