import pytest

import numpy as np

from sklearn.tree import DecisionTreeClassifier
from ..models import SoloModel

from sklearn.utils._testing import assert_array_almost_equal

from ..metrics import uplift_curve, uplift_auc_score

from sklearn.metrics import auc

def make_predictions(binary):
    X_train, y_train, treat_train = (np.array([[5.1, 3.5, 1.4, 0.2],[4.9, 3.0, 1.4, 0.2],[4.7, 3.2, 1.3, 0.2]]),
                                        np.array([0.0,0.0,1.0]), np.array([0.0,1.0,1.0]))
    X_val, y_val, treat_val = (np.array([[5.1, 3.4, 1.5, 0.2],[5.0, 3.5, 1.3, 0.3],[4.5, 2.3, 1.3, 0.3]]), 
                                np.array([0.0,1.0,0.0]), np.array([0.0,1.0,1.0]))

    if binary == False:
        y_train, y_val = (np.array([2.0,0.0,1.0]),np.array([0.0,1.0,2.0]))

    model = DecisionTreeClassifier(random_state=0)

    tm = SoloModel(model)

    tm = tm.fit(X_train, y_train, treat_train)

    uplift_preds = tm.predict(X_val)

    return y_val, uplift_preds, treat_val


@pytest.mark.parametrize(
    "binary, test_x_actual, test_y_actual",
    [
        (True, np.array([0, 3]), np.array([0, 1.5,])),
        (False, np.array([0, 2, 3]), np.array([0.0, 3, 4.5]))
    ]
)
def test_uplift_curve(binary, test_x_actual, test_y_actual):
    
    y_true, uplift, treatment = make_predictions(binary)

    x_actual, y_actual = uplift_curve(y_true, uplift, treatment)

    assert_array_almost_equal(x_actual, test_x_actual)
    assert_array_almost_equal(y_actual, test_y_actual)
    assert x_actual.shape == y_actual.shape

