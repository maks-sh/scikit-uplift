import numpy as np
from sklearn.utils.extmath import stable_cumsum
from sklearn.metrics import auc


def uplift_curve(y_true, uplift, treatment):
    """Compute Uplift curve

    This is a general function, given points on a curve.  For computing the
    area under the Uplift Curve, see :func:`auuc`.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        array (shape = [>2]), array (shape = [>2]): Points on a curve.

    See also:
        :func:`auuc`: Compute the area under the Uplift curve.

        :func:`plot_uplift_qini_curves`: Plot Uplift and Qini curves.
    """

    # ToDo: Добавить проверки на наличие обоих классов в столбце treatment
    # ToDo: Добавить проверку на наличие обоих классов в  y_true для каждого уникального значения из столбца treatment

    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)
    desc_score_indices = np.argsort(uplift, kind="mergesort")[::-1]
    y_true, uplift, treatment = y_true[desc_score_indices], uplift[desc_score_indices], treatment[desc_score_indices]

    y_true_ctrl, y_true_trmnt = y_true.copy(), y_true.copy()

    y_true_ctrl[treatment == 1] = 0
    y_true_trmnt[treatment == 0] = 0

    distinct_value_indices = np.where(np.diff(uplift))[0]
    threshold_indices = np.r_[distinct_value_indices, uplift.size - 1]

    num_trmnt = stable_cumsum(treatment)[threshold_indices]
    y_trmnt = stable_cumsum(y_true_trmnt)[threshold_indices]

    num_all = threshold_indices + 1

    num_ctrl = num_all - num_trmnt
    y_ctrl = stable_cumsum(y_true_ctrl)[threshold_indices]

    curve_values = (np.divide(y_trmnt, num_trmnt, out=np.zeros_like(y_trmnt), where=num_trmnt != 0) -\
                    np.divide(y_ctrl, num_ctrl, out=np.zeros_like(y_ctrl), where=num_ctrl != 0)) * num_all

    if num_all.size == 0 or curve_values[0] != 0 or num_all[0] != 0:
        # Add an extra threshold position if necessary
        # to make sure that the curve starts at (0, 0)
        num_all = np.r_[0, num_all]
        curve_values = np.r_[0, curve_values]

    return num_all, curve_values


def qini_curve(y_true, uplift, treatment):
    """Compute Qini curve.

    This is a general function, given points on a curve. For computing the
    area under the Qini Curve, see :func:`auqc`.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        array (shape = [>2]), array (shape = [>2]): Points on a curve.

    See also:
        :func:`auqc`: Compute the area under the Qini curve.

        :func:`plot_uplift_qini_curves`: Plot Uplift and Qini curves.
    """
    # ToDo: Добавить проверки на наличие обоих классов в столбце treatment
    # ToDo: Добавить проверку на наличие обоих классов в столбце y_true для каждого уникального значения из столбца treatment

    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    desc_score_indices = np.argsort(uplift, kind="mergesort")[::-1]

    y_true = y_true[desc_score_indices]
    treatment = treatment[desc_score_indices]
    uplift = uplift[desc_score_indices]

    y_true_ctrl, y_true_trmnt = y_true.copy(), y_true.copy()

    y_true_ctrl[treatment == 1] = 0
    y_true_trmnt[treatment == 0] = 0

    distinct_value_indices = np.where(np.diff(uplift))[0]
    threshold_indices = np.r_[distinct_value_indices, uplift.size - 1]

    num_trmnt = stable_cumsum(treatment)[threshold_indices]
    y_trmnt = stable_cumsum(y_true_trmnt)[threshold_indices]

    num_all = threshold_indices + 1

    num_ctrl = num_all - num_trmnt
    y_ctrl = stable_cumsum(y_true_ctrl)[threshold_indices]

    curve_values = y_trmnt - y_ctrl * np.divide(num_trmnt, num_ctrl, out=np.zeros_like(num_trmnt), where=num_ctrl != 0)
    if num_all.size == 0 or curve_values[0] != 0 or num_all[0] != 0:
        # Add an extra threshold position if necessary
        # to make sure that the curve starts at (0, 0)
        num_all = np.r_[0, num_all]
        curve_values = np.r_[0, curve_values]

    return num_all, curve_values


def auuc(y_true, uplift, treatment):
    """
    Compute Area Under the Uplift Curve from prediction scores.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        float: Area Under the Uplift Curve.
    """
    # ToDO: Добавить бейзлайн
    return auc(*uplift_curve(y_true, uplift, treatment))


def auqc(y_true, uplift, treatment):
    # ToDo: добавить описание функции
    """Compute Area Under the Qini Curve (aka Qini coefficient) from prediction scores.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        float: Area Under the Qini Curve.
    """
    # ToDO: Добавить бейзлайн
    return auc(*qini_curve(y_true, uplift, treatment))


def uplift_at_k(y_true, uplift, treatment, k=0.3):
    """Compute uplift at first k percentage of the total sample.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        k (float > 0 and <= 1): Percentage of the total sample to compute uplift.

    Returns:
        float: Uplift at first k percentage of the total sample.

    Reference:
        Baseline from `RetailHero competition`_.

    .. _RetailHero competition:
        https://retailhero.ai/c/uplift_modeling/overview
    """
    order = np.argsort(-uplift)
    treatment_n = int((treatment == 1).sum() * k)
    treatment_p = y_true[order][treatment[order] == 1][:treatment_n].mean()
    control_n = int((treatment == 0).sum() * k)
    control_p = y_true[order][treatment[order] == 0][:control_n].mean()
    score_at_k = treatment_p - control_p
    return score_at_k
