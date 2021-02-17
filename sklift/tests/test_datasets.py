import pytest

from functools import partial

from ..datasets import (
    fetch_hillstrom, fetch_lenta, fetch_criteo
)


fetch_criteo10 = partial(fetch_criteo, percent10=True)


def check_return_X_y_t(bunch, dataset_func):
    X_y_t_tuple = dataset_func(return_X_y_t=True)
    assert isinstance(X_y_t_tuple, tuple)
    assert X_y_t_tuple[0].shape == bunch.data.shape
    assert X_y_t_tuple[1].shape == bunch.target.shape
    assert X_y_t_tuple[2].shape == bunch.treatment.shape


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
