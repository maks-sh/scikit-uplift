import numpy as np

def check_is_binary(array):
    """Checker if array consists of int or float binary values 0 (0.) and 1 (1.)

    Args:
        array (1d array-like): Array to check.
    """

    if not np.all(np.unique(array) == np.array([0, 1])):
        raise ValueError(f"Input array is not binary. "
                         f"Array should contain only int or float binary values 0 (or 0.) and 1 (or 1.). "
                         f"Got values {np.unique(array)}.")


def check_matplotlib_support(caller_name):
    """Raise ImportError with detailed error message if mpl is not installed.
    Plot utilities like any of the Display's plotting functions should lazily import
    matplotlib and call this helper before any computation.
    
    Args:
        caller_name (str): The name of the caller that requires matplotlib.
    """
    try:
        import matplotlib  # noqa
    except ImportError as e:
        raise ImportError(
            "{} requires matplotlib. You can install matplotlib with "
            "`pip install matplotlib`".format(caller_name)
        ) from e
