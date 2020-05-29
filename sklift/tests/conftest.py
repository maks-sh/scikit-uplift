import itertools
from collections import defaultdict

import numpy as np
import pandas as pd
import pytest

n_vals = (100, 1000)
k_vals = (1, 5)
np_types = (np.int32, np.float32, np.float64)
dataset_types = ('numpy', 'pandas')


@pytest.fixture
def sensitive_classification_dataset():
    df = pd.DataFrame(
        {
            "x1": [1, 0, 1, 0, 1, 0, 1, 1],
            "x2": [0, 0, 0, 0, 0, 1, 1, 1],
            "y": [1, 1, 1, 0, 1, 0, 0, 0],
            "treat": [1, 1, 1, 1, 0, 0, 0, 1]
        }
    )

    return df[["x1", "x2"]], df["y"], df["treat"]


@pytest.fixture(
    scope="module", params=[_ for _ in itertools.product(n_vals, k_vals, np_types, dataset_types)]
)
def random_xy_dataset_regr(request):
    n, k, np_type, dataset_type = request.param
    np.random.seed(42)
    X = np.random.normal(0, 2, (n, k)).astype(np_type)
    y = np.random.normal(0, 2, (n,))
    treat = (np.random.normal(0, 2, (n,)) > 0.0).astype(int)
    if dataset_type == 'numpy':
        return X, y, treat
    return pd.DataFrame(X), pd.Series(y), pd.Series(treat)


@pytest.fixture(
    scope="module", params=[_ for _ in itertools.product(n_vals, k_vals, np_types, dataset_types)]
)
def random_xyt_dataset_clf(request):
    n, k, np_type, dataset_type = request.param
    X, y, treat = None, None, None
    mean_target_ctrl, mean_target_trmnt = 0, 0
    """
    The main rule for creating a random dataset is that 
    the average conversions in the control and experimental groups 
    should not be equal to 0 or 1.
    """
    while ((mean_target_ctrl == 0) or (mean_target_ctrl == 1) or
            (mean_target_trmnt == 0) or (mean_target_trmnt == 1)):
        np.random.seed(42)
        X = np.random.normal(0, 2, (n, k)).astype(np_type)
        y = (np.random.normal(0, 2, (n,)) > 0.0).astype(int)
        treat = (np.random.normal(0, 2, (n,)) > 0.0).astype(int)
        dd = defaultdict(list)
        for key, val in zip(treat, y):
            dd[key].append(val)
        mean_target_ctrl = np.mean(dd[0])
        mean_target_trmnt = np.mean(dd[1])

    if dataset_type == 'numpy':
        return X, y, treat
    return pd.DataFrame(X), pd.Series(y), pd.Series(treat)

