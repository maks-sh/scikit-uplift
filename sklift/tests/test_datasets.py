import pytest
import sklearn

from functools import partial

from ..datasets import (
    clear_data_dir,
    fetch_lenta, fetch_x5,
    fetch_criteo, fetch_hillstrom,
    fetch_megafon
)


fetch_criteo10 = partial(fetch_criteo, percent10=True)

@pytest.fixture(scope="session", autouse=True)
def clear():
    # prepare something ahead of all tests
    clear_data_dir()


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

#@pytest.fixture
#def x5_dataset() -> dict:
#	data = {'keys': ['data', 'target', 'treatment', 'DESCR', 'feature_names', 'target_name', 'treatment_name'],
#             'data.keys': ['clients', 'train', 'purchases'], 'clients.shape': (400162, 5),
#            'train.shape': (200039, 1), 'target.shape': (200039,), 'treatment.shape': (200039,)}
#	return data

#
#def test_fetch_x5(x5_dataset):
#	data = fetch_x5()
#	assert isinstance(data, sklearn.utils.Bunch)
#	assert set(data.keys()) == set(x5_dataset['keys'])
#	assert set(data.data.keys()) == set(x5_dataset['data.keys'])
#	assert data.data.clients.shape == x5_dataset['clients.shape']
#	assert data.data.train.shape == x5_dataset['train.shape']
#	assert data.target.shape == x5_dataset['target.shape']
#	assert data.treatment.shape == x5_dataset['treatment.shape']


@pytest.fixture
def criteo10_dataset() -> dict:
    data = {'keys': ['data', 'target', 'treatment', 'DESCR', 'feature_names', 'target_name', 'treatment_name'],
            'data.shape': (1397960, 12)}
    return data


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
        criteo10_dataset,
        target_col, target_shape,
        treatment_col, treatment_shape
):
    data = fetch_criteo10(target_col=target_col, treatment_col=treatment_col)
    assert isinstance(data, sklearn.utils.Bunch)
    assert set(data.keys()) == set(criteo10_dataset['keys'])
    assert data.data.shape == criteo10_dataset['data.shape']
    assert data.target.shape == target_shape
    assert data.treatment.shape == treatment_shape

@pytest.mark.parametrize(
    'target_col, treatment_col',
    [('visit','new_trmnt'), ('new_target','treatment')]
    )    
def test_fetch_criteo_errors(target_col, treatment_col):
	with pytest.raises(ValueError):
		 fetch_criteo(target_col=target_col, treatment_col=treatment_col) 


@pytest.fixture
def hillstrom_dataset() -> dict:
    data = {'keys': ['data', 'target', 'treatment', 'DESCR', 'feature_names', 'target_name', 'treatment_name'],
            'data.shape': (64000, 8), 'treatment.shape': (64000,)}
    return data


@pytest.mark.parametrize(
    'target_col, target_shape',
    [('visit', (64_000,)),
     ('conversion', (64_000,)),
     ('spend', (64_000,)),
     ('all', (64_000, 3))]
)
def test_fetch_hillstrom(
        hillstrom_dataset,
        target_col, target_shape
):
    data = fetch_hillstrom(target_col=target_col)
    assert isinstance(data, sklearn.utils.Bunch)
    assert set(data.keys()) == set(hillstrom_dataset['keys'])
    assert data.data.shape == hillstrom_dataset['data.shape']
    assert data.target.shape == target_shape
    assert data.treatment.shape == hillstrom_dataset['treatment.shape']

def test_fetch_hillstrom_error():
	with pytest.raises(ValueError):
		 fetch_hillstrom(target_col='new_target')   


@pytest.fixture
def megafon_dataset() -> dict:
    data = {'keys': ['data', 'target', 'treatment', 'DESCR', 'feature_names', 'target_name', 'treatment_name'],
            'data.shape': (600000, 50), 'target.shape': (600000,), 'treatment.shape': (600000,)}
    return data


def test_fetch_megafon(megafon_dataset):
    data = fetch_megafon()
    assert isinstance(data, sklearn.utils.Bunch)
    assert set(data.keys()) == set(megafon_dataset['keys'])
    assert data.data.shape == megafon_dataset['data.shape']
    assert data.target.shape == megafon_dataset['target.shape']
    assert data.treatment.shape == megafon_dataset['treatment.shape']


def check_return_X_y_t(bunch, dataset_func):
    X_y_t_tuple = dataset_func(return_X_y_t=True)
    assert isinstance(X_y_t_tuple, tuple)
    assert X_y_t_tuple[0].shape == bunch.data.shape
    assert X_y_t_tuple[1].shape == bunch.target.shape
    assert X_y_t_tuple[2].shape == bunch.treatment.shape


@pytest.mark.parametrize("fetch_func", [fetch_hillstrom, fetch_criteo10, fetch_lenta, fetch_megafon])
def test_return_X_y_t(fetch_func):
    data = fetch_func()
    check_return_X_y_t(data, fetch_func)
