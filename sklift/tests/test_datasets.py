import pytest

from ..datasets import (
    fetch_hillstrom
)


def check_return_X_y_t(bunch, dataset_func):
    X_y_t_tuple = dataset_func(return_X_y_t=True)
    assert isinstance(X_y_t_tuple, tuple)
    assert X_y_t_tuple[0].shape == bunch.data.shape
    assert X_y_t_tuple[1].shape == bunch.target.shape
    assert X_y_t_tuple[2].shape == bunch.treatment.shape


@pytest.mark.parametrize("target_col", ['visit', 'conversion', 'spend'])
@pytest.mark.parametrize("as_frame", [True, False])
def test_fetch_hillstrom(
    target_col, as_frame
):
    data = fetch_hillstrom(target_col=target_col, as_frame=as_frame)
    assert data.data.shape == (64_000, 8)
    assert data.target.shape == (64_000,)
    assert data.treatment.shape == (64_000,)


def test_fetch_hillstrom_return_X_y_t():
    fetch_func = fetch_hillstrom
    data = fetch_func()
    check_return_X_y_t(data, fetch_func)
