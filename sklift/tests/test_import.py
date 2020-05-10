try:
    from .. import *  # noqa
    _top_import_error = None
except Exception as e:
    _top_import_error = e


def test_import_sklift():
    assert _top_import_error is None
