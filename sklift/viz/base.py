import matplotlib.pyplot as plt
import numpy as np
from ..metrics import uplift_curve, auuc, qini_curve, auqc, treatment_balance_curve


def plot_uplift_preds(trmnt_preds, ctrl_preds, log=False, bins=100):
    """Plot histograms of treatment, control and uplift predictions.

    Args:
        trmnt_preds (1d array-like): Predictions for all observations if they are treatment.
        ctrl_preds (1d array-like): Predictions for all observations if they are control.
        log (bool, default False): Logarithm of source samples.
        bins (integer or sequence, default 100): Number of histogram bins to be used.
            If an integer is given, bins + 1 bin edges are calculated and returned.
            If bins is a sequence, gives bin edges, including left edge of first bin and right edge of last bin.
            In this case, bins is returned unmodified.

    Returns:
        Object that stores computed values.
    """
    # ToDo: Добавить квантиль как параметр
    if log:
        trmnt_preds = np.log(trmnt_preds + 1)
        ctrl_preds = np.log(ctrl_preds + 1)

    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(20, 7))
    axes[0].hist(
        trmnt_preds, bins=bins, alpha=0.3, color='b', label='Treated', histtype='stepfilled')
    axes[0].set_ylabel('Probability hist')
    axes[0].legend()
    axes[0].set_title('Treatment predictions')

    axes[1].hist(
        ctrl_preds, bins=bins, alpha=0.5, color='y', label='Not treated', histtype='stepfilled')
    axes[1].legend()
    axes[1].set_title('Control predictions')

    axes[2].hist(
        trmnt_preds - ctrl_preds, bins=bins, alpha=0.5, color='green', label='Uplift', histtype='stepfilled')
    axes[2].legend()
    axes[2].set_title('Uplift predictions')

    return axes


def plot_uplift_qini_curves(y_true, uplift, treatment, random=True, perfect=False):
    """Plot Uplift and Qini curves.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        random (bool, default True): Draw a random curve.
        perfect (bool, default False): Draw a perfect curve.

    Returns:
        Object that stores computed values.
    """
    x_up, y_up = uplift_curve(y_true, uplift, treatment)
    x_qi, y_qi = qini_curve(y_true, uplift, treatment)

    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(14, 7))

    axes[0].plot(x_up, y_up, label='Model', color='b')
    axes[1].plot(x_qi, y_qi, label='Model', color='b')

    if random:
        up_ratio_random = y_true[treatment == 1].sum() / len(y_true[treatment == 1]) - \
                          y_true[treatment == 0].sum() / len(y_true[treatment == 0])
        y_up_random = x_up * up_ratio_random

        qi_ratio_random = (y_true[treatment == 1].sum() - len(y_true[treatment == 1]) * \
                           y_true[treatment == 0].sum() / len(y_true[treatment == 0])) / len(y_true)
        y_qi_random = x_qi * qi_ratio_random

        axes[0].plot(x_up, y_up_random, label='Random', color='black')
        axes[0].fill_between(x_up, y_up, y_up_random, alpha=0.2, color='b')
        axes[1].plot(x_qi, y_qi_random, label='Random', color='black')
        axes[1].fill_between(x_qi, y_qi, y_qi_random, alpha=0.2, color='b')

    if perfect:
        x_up_perfect, y_up_perfect = uplift_curve(
            y_true, y_true * treatment - y_true * (1 - treatment), treatment
        )
        x_qi_perfect, y_qi_perfect = qini_curve(
            y_true, y_true * treatment - y_true * (1 - treatment), treatment
        )

        axes[0].plot(x_up_perfect, y_up_perfect, label='Perfect', color='red')
        axes[1].plot(x_qi_perfect, y_qi_perfect, label='Perfect', color='red')

    axes[0].legend()
    axes[0].set_title(f'Uplift curve: AUUC={auuc(y_true, uplift, treatment):.2f}')
    axes[0].set_xlabel('Number targeted')
    axes[0].set_ylabel('Relative gain: treatment - control')

    axes[1].legend()
    axes[1].set_title(f'Qini curve: AUQC={auqc(y_true, uplift, treatment):.2f}')
    axes[1].set_xlabel('Number targeted')
    axes[1].set_ylabel('Number of incremental outcome')

    return axes


def plot_treatment_balance_curve(uplift, treatment, random=True, winsize=0.1):
    """Plot Treatment Balance curve.

    Args:
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        random (bool, default True): Draw a random curve.
        winsize (float, default 0.1): Size of the sliding window to apply. Should be between 0 and 1, extremes excluded.

    Returns:
        Object that stores computed values.
    """
    if (winsize <= 0) or (winsize >= 1):
        raise ValueError('winsize should be between 0 and 1, extremes excluded')

    x_tb, y_tb = treatment_balance_curve(uplift, treatment, winsize=int(len(uplift)*winsize))

    _, axes = plt.subplots(ncols=1, nrows=1, figsize=(14, 7))

    axes.plot(x_tb, y_tb, label='Model', color='b')

    if random:
        y_tb_random = np.average(treatment) * np.ones_like(x_tb)

        axes.plot(x_tb, y_tb_random, label='Random', color='black')
        axes.fill_between(x_tb, y_tb, y_tb_random, alpha=0.2, color='b')

    axes.legend()
    axes.set_title('Treatment balance curve')
    axes.set_xlabel('Percentage targeted')
    axes.set_ylabel('Balance: treatment / (treatment + control')

    return axes
