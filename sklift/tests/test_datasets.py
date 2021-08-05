import pytest
import sklearn

from functools import partial

from ..datasets import (fetch_lenta, fetch_x5,
                        fetch_criteo, fetch_hillstrom)


fetch_criteo10 = partial(fetch_criteo, percent10=True)


def check_return_X_y_t(bunch, dataset_func):
    X_y_t_tuple = dataset_func(return_X_y_t=True)
    assert isinstance(X_y_t_tuple, tuple)
    assert X_y_t_tuple[0].shape == bunch.data.shape
    assert X_y_t_tuple[1].shape == bunch.target.shape
    assert X_y_t_tuple[2].shape == bunch.treatment.shape


@pytest.fixture
def lenta_dataset() -> dict:
    data = {'keys': ['data', 'target', 'treatment', 'DESCR', 'feature_names', 'target_name', 'treatment_name'],
            'data.shape': (687029, 193), 'target.shape': (687029,), 'treatment.shape': (687029,)}
    return data


def test_fetch_lenta(lenta_dataset):
    data = fetch_lenta()
    assert isinstance(data, sklearn.utils.Bunch)
    assert set(data.keys()) == set(lenta_dataset['keys'])
    assert data.data.shape == lenta_dataset['data.shape']
    assert data.target.shape == lenta_dataset['target.shape']
    assert data.treatment.shape == lenta_dataset['treatment.shape']


@pytest.fixture
def x5_dataset() -> dict:
    data = {'keys': ['data', 'target', 'treatment', 'DESCR', 'feature_names', 'target_name', 'treatment_name'],
            'data.keys': ['clients', 'train', 'purchases'], 'clients.shape': (400162, 5),
            'train.shape': (200039, 1), 'target.shape': (200039,), 'treatment.shape': (200039,)}
    return data


def test_fetch_x5(x5_dataset):
    data = fetch_x5()
    assert isinstance(data, sklearn.utils.Bunch)
    assert set(data.keys()) == set(x5_dataset['keys'])
    assert set(data.data.keys()) == set(x5_dataset['data.keys'])
    assert data.data.clients.shape == x5_dataset['clients.shape']
    assert data.data.train.shape == x5_dataset['train.shape']
    assert data.target.shape == x5_dataset['target.shape']
    assert data.treatment.shape == x5_dataset['treatment.shape']


@pytest.mark.parametrize(
    'target_col, target_shape',
    [('visit', (64_000,)),
     ('conversion', (64_000,)),
     ('spend', (64_000,)),
     ('all', (64_000, 3))]
)
def test_fetch_hillstrom(
    target_col, target_shape
):
    data = fetch_hillstrom(target_col=target_col)
    assert data.data.shape == (64_000, 8)
    assert data.target.shape == target_shape
    assert data.treatment.shape == (64_000,)


@pytest.mark.parametrize(
    'target_col, target_shape',
    [('visit', (1397960,)),
     ('conversion', (1397960,)),
     ('all', (1397960, 2))]
)
@pytest.mark.parametrize(
    'treatment_col, treatment_shape',
    [('exposure', (1397960,)),
     ('treatment', (1397960,)),
     ('all', (1397960, 2))]
)
def test_fetch_criteo10(
    target_col, target_shape, treatment_col, treatment_shape
):
    data = fetch_criteo10(target_col=target_col, treatment_col=treatment_col)
    assert data.data.shape == (1397960, 12)
    assert data.target.shape == target_shape
    assert data.treatment.shape == treatment_shape


@pytest.mark.parametrize("fetch_func", [fetch_hillstrom, fetch_criteo10, fetch_lenta])
def test_return_X_y_t(fetch_func):
    data = fetch_func()
    check_return_X_y_t(data, fetch_func)
