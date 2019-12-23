import numpy as np
from sklearn.utils.extmath import stable_cumsum
from sklearn.metrics import auc


def uplift_curve(y_true, uplift, treatment):
    # ToDo: добавить описание функции
    """

    :param y_true:
    :param uplift:
    :param treatment:
    :return:
    """

    # ToDo: Добавить проверки на наличие обоих классов в столбце treatment
    # ToDo: Добавить проверку на наличие обоих классов в  y_true для каждого уникального значения из столбца treatment

    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)
    desc_score_indices = np.argsort(uplift, kind="mergesort")[::-1]
    y_true, uplift, treatment = y_true[desc_score_indices], uplift[desc_score_indices], treatment[desc_score_indices]

    y_true_ctrl = y_true.copy()
    y_true_ctrl[treatment == 1] = 0

    y_true_trmnt = y_true.copy()
    y_true_trmnt[treatment == 0] = 0

    distinct_value_indices = np.where(np.diff(uplift))[0]
    threshold_indices = np.r_[distinct_value_indices, uplift.size - 1]

    # Количество N_T
    N_T = stable_cumsum(treatment)[threshold_indices]
    Y_T = stable_cumsum(y_true_trmnt)[threshold_indices]

    # Количество N_T + N_C
    N = threshold_indices + 1

    # Количество N_C
    N_C = N - N_T
    Y_C = stable_cumsum(y_true_ctrl)[threshold_indices]

    curve_values = (np.divide(Y_T, N_T, out=np.zeros_like(Y_T), where=N_T != 0) - \
                   np.divide(Y_C, N_C, out=np.zeros_like(Y_C), where=N_C != 0)) * N
    if N.size == 0 or curve_values[0] != 0 or N[0] != 0:
        # Add an extra threshold position if necessary
        # to make sure that the curve starts at (0, 0)
        N = np.r_[0, N]
        curve_values = np.r_[0, curve_values]

    return N, curve_values


def qini_curve(y_true, uplift, treatment):
    # ToDo: добавить описание функции
    """

    :param y_true:
    :param uplift:
    :param treatment:
    :return:
    """
    # ToDo: Добавить проверки на наличие обоих классов в столбце treatment
    # ToDo: Добавить проверку на наличие обоих классов в столбце y_true для каждого уникального значения из столбца treatment

    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    desc_score_indices = np.argsort(uplift, kind="mergesort")[::-1]

    y_true = y_true[desc_score_indices]
    treatment = treatment[desc_score_indices]
    uplift = uplift[desc_score_indices]

    y_true_ctrl = y_true.copy()
    y_true_ctrl[treatment == 1] = 0

    y_true_trmnt = y_true.copy()
    y_true_trmnt[treatment == 0] = 0

    distinct_value_indices = np.where(np.diff(uplift))[0]
    threshold_indices = np.r_[distinct_value_indices, uplift.size - 1]

    # Количество N_T
    N_T = stable_cumsum(treatment)[threshold_indices]
    Y_T = stable_cumsum(y_true_trmnt)[threshold_indices]

    # Количество N_T + N_C
    N = threshold_indices + 1

    # Количество N_C
    N_C = N - N_T
    Y_C = stable_cumsum(y_true_ctrl)[threshold_indices]

    curve_values = Y_T - Y_C * np.divide(N_T, N_C, out=np.zeros_like(N_T), where=N_C != 0)
    if N.size == 0 or curve_values[0] != 0 or N[0] != 0:
        # Add an extra threshold position if necessary
        # to make sure that the curve starts at (0, 0)
        N = np.r_[0, N]
        curve_values = np.r_[0, curve_values]

    return N, curve_values


def auuc(y_true, uplift, treatment):
    # ToDo: добавить описание функции
    """
    Area Under the Uplift Curve
    :param y_true:
    :param uplift:
    :param treatment:
    :return:
    """
    # ToDO: Добавить бейзлайн
    return auc(*uplift_curve(y_true, uplift, treatment))


def auqc(y_true, uplift, treatment):
    # ToDo: добавить описание функции
    """Area Under the Qini Curve aka Qini coefficient
    :param y_true:
    :param uplift:
    :param treatment:
    :return:

    Eustache Diemert, Artem Betlei, Christophe Renaudin, and Massih-Reza Amini. 2018.
    A Large Scale Benchmark for Uplift Modeling.
    In Proceedings of AdKDD & TargetAd (ADKDD’18). ACM, New York, NY, USA, 6 pages.
    """
    # ToDO: Добавить бейзлайн
    return auc(*qini_curve(y_true, uplift, treatment))


def uplift_at_k(y_true, uplift, treatment, k=0.3):
    """
    reference: Baseline from RetailHero competition
    """
    order = np.argsort(-uplift)
    treatment_n = int((treatment == 1).sum() * k)
    treatment_p = y_true[order][treatment[order] == 1][:treatment_n].mean()
    control_n = int((treatment == 0).sum() * k)
    control_p = y_true[order][treatment[order] == 0][:control_n].mean()
    score_at_k = treatment_p - control_p
    return score_at_k
