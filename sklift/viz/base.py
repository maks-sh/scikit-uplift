import matplotlib.pyplot as plt
import numpy as np
from sklearn.utils.validation import check_consistent_length

from ..utils import check_is_binary
from ..metrics import (
    uplift_curve, perfect_uplift_curve, uplift_auc_score,
    qini_curve, perfect_qini_curve, qini_auc_score,
    treatment_balance_curve, uplift_by_percentile
)


def plot_uplift_preds(trmnt_preds, ctrl_preds, log=False, bins=100):
    """Plot histograms of treatment, control and uplift predictions.

    Args:
        trmnt_preds (1d array-like): Predictions for all observations if they are treatment.
        ctrl_preds (1d array-like): Predictions for all observations if they are control.
        log (bool): Logarithm of source samples. Default is False.
        bins (integer or sequence): Number of histogram bins to be used. Default is 100.
            If an integer is given, bins + 1 bin edges are calculated and returned.
            If bins is a sequence, gives bin edges, including left edge of first bin and right edge of last bin.
            In this case, bins is returned unmodified. Default is 100.

    Returns:
        Object that stores computed values.
    """

    # TODO: Add k as parameter: vertical line on plots
    check_consistent_length(trmnt_preds, ctrl_preds)
    check_is_binary(treatment)

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(
            f'Bins should be positive integer. Invalid value for bins: {bins}')

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


def plot_uplift_curve(y_true, uplift, treatment, random=True, perfect=True):
    """Plot Uplift curves from predictions.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        random (bool): Draw a random curve. Default is True.
        perfect (bool): Draw a perfect curve. Default is True.

    Returns:
        Object that stores computed values.
    """

    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8, 6))

    x_actual, y_actual = uplift_curve(y_true, uplift, treatment)
    ax.plot(x_actual, y_actual, label='Model', color='blue')

    if random:
        x_baseline, y_baseline = x_actual, x_actual * \
            y_actual[-1] / len(y_true)
        ax.plot(x_baseline, y_baseline, label='Random', color='black')
        ax.fill_between(x_actual, y_actual, y_baseline, alpha=0.2, color='b')

    if perfect:
        x_perfect, y_perfect = perfect_uplift_curve(y_true, treatment)
        ax.plot(x_perfect, y_perfect, label='Perfect', color='Red')

    ax.legend(loc='lower right')
    ax.set_title(
        f'Uplift curve\nuplift_auc_score={uplift_auc_score(y_true, uplift, treatment):.4f}')
    ax.set_xlabel('Number targeted')
    ax.set_ylabel('Gain: treatment - control')

    return ax


def plot_qini_curve(y_true, uplift, treatment, random=True, perfect=True, negative_effect=True):
    """Plot Qini curves from predictions.

    Args:
        y_true (1d array-like): Ground truth (correct) labels.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        random (bool): Draw a random curve. Default is True.
        perfect (bool): Draw a perfect curve. Default is True.
        negative_effect (bool): If True, optimum Qini Curve contains the negative effects
            (negative uplift because of campaign). Otherwise, optimum Qini Curve will not
            contain the negative effects. Default is True.

    Returns:
        Object that stores computed values.
    """

    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8, 6))

    x_actual, y_actual = qini_curve(y_true, uplift, treatment)
    ax.plot(x_actual, y_actual, label='Model', color='blue')

    if random:
        x_baseline, y_baseline = x_actual, x_actual * \
            y_actual[-1] / len(y_true)
        ax.plot(x_baseline, y_baseline, label='Random', color='black')
        ax.fill_between(x_actual, y_actual, y_baseline, alpha=0.2, color='b')

    if perfect:
        x_perfect, y_perfect = perfect_qini_curve(
            y_true, treatment, negative_effect)
        ax.plot(x_perfect, y_perfect, label='Perfect', color='Red')

    ax.legend(loc='lower right')
    ax.set_title(
        f'Qini curve\nqini_auc_score={qini_auc_score(y_true, uplift, treatment, negative_effect):.4f}')
    ax.set_xlabel('Number targeted')
    ax.set_ylabel('Number of incremental outcome')

    return ax


def plot_uplift_by_percentile(y_true, uplift, treatment, strategy='overall', kind='line', bins=10):
    """Plot uplift score, treatment response rate and control response rate at each percentile.

    Treatment response rate ia a target mean in the treatment group.
    Control response rate is a target mean in the control group.
    Uplift score is a difference between treatment response rate and control response rate.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        strategy (string, ['overall', 'by_group']): Determines the calculating strategy. Default is 'overall'.

            * ``'overall'``:
                The first step is taking the first k observations of all test data ordered by uplift prediction
                (overall both groups - control and treatment) and conversions in treatment and control groups
                calculated only on them. Then the difference between these conversions is calculated.
            * ``'by_group'``:
                Separately calculates conversions in top k observations in each group (control and treatment)
                sorted by uplift predictions. Then the difference between these conversions is calculated.

        kind (string, ['line', 'bar']): The type of plot to draw. Default is 'line'.

            * ``'line'``:
                Generates a line plot.
            * ``'bar'``:
                Generates a traditional bar-style plot.

        bins (int): Determines а number of bins (and the relative percentile) in the test data. Default is 10.

    Returns:
        Object that stores computed values.
    """

    strategy_methods = ['overall', 'by_group']
    kind_methods = ['line', 'bar']

    check_consistent_length(y_true, uplift, treatment)
    check_is_binary(treatment)
    n_samples = len(y_true)

    if strategy not in strategy_methods:
        raise ValueError(f'Response rate supports only calculating methods in {strategy_methods},'
                         f' got {strategy}.')

    if kind not in kind_methods:
        raise ValueError(f'Function supports only types of plots in {kind_methods},'
                         f' got {kind}.')

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(
            f'Bins should be positive integer. Invalid value bins: {bins}')

    if bins >= n_samples:
        raise ValueError(
            f'Number of bins = {bins} should be smaller than the length of y_true {n_samples}')

    df = uplift_by_percentile(y_true, uplift, treatment, strategy=strategy,
                              std=True, total=True, bins=bins)

    percentiles = df.index[:bins].values.astype(float)

    response_rate_trmnt = df.loc[percentiles, 'response_rate_treatment'].values
    std_trmnt = df.loc[percentiles, 'std_treatment'].values

    response_rate_ctrl = df.loc[percentiles, 'response_rate_control'].values
    std_ctrl = df.loc[percentiles, 'std_control'].values

    uplift_score = df.loc[percentiles, 'uplift'].values
    std_uplift = df.loc[percentiles, 'std_uplift'].values

    uplift_weighted_avg = df.loc['total', 'uplift']

    check_consistent_length(percentiles, response_rate_trmnt, response_rate_ctrl, uplift_score,
                            std_trmnt, std_ctrl, std_uplift)

    if kind == 'line':
        _, axes = plt.subplots(ncols=1, nrows=1, figsize=(8, 6))
        axes.errorbar(percentiles, response_rate_trmnt, yerr=std_trmnt,
                      linewidth=2, color='forestgreen', label='treatment\nresponse rate')
        axes.errorbar(percentiles, response_rate_ctrl, yerr=std_ctrl,
                      linewidth=2, color='orange', label='control\nresponse rate')
        axes.errorbar(percentiles, uplift_score, yerr=std_uplift,
                      linewidth=2, color='red', label='uplift')
        axes.fill_between(percentiles, response_rate_trmnt,
                          response_rate_ctrl, alpha=0.1, color='red')

        if np.amin(uplift_score) < 0:
            axes.axhline(y=0, color='black', linewidth=1)
        axes.set_xticks(percentiles)
        axes.legend(loc='upper right')
        axes.set_title(
            f'Uplift by percentile\nweighted average uplift = {uplift_weighted_avg:.4f}')
        axes.set_xlabel('Percentile')
        axes.set_ylabel(
            'Uplift = treatment response rate - control response rate')

    else:  # kind == 'bar'
        delta = percentiles[0]
        fig, axes = plt.subplots(ncols=1, nrows=2, figsize=(
            8, 6), sharex=True, sharey=True)
        fig.text(0.04, 0.5, 'Uplift = treatment response rate - control response rate',
                 va='center', ha='center', rotation='vertical')

        axes[1].bar(np.array(percentiles) - delta / 6, response_rate_trmnt, delta / 3,
                    yerr=std_trmnt, color='forestgreen', label='treatment\nresponse rate')
        axes[1].bar(np.array(percentiles) + delta / 6, response_rate_ctrl, delta / 3,
                    yerr=std_ctrl, color='orange', label='control\nresponse rate')
        axes[0].bar(np.array(percentiles), uplift_score, delta / 1.5,
                    yerr=std_uplift, color='red', label='uplift')

        axes[0].legend(loc='upper right')
        axes[0].tick_params(axis='x', bottom=False)
        axes[0].axhline(y=0, color='black', linewidth=1)
        axes[0].set_title(
            f'Uplift by percentile\nweighted average uplift = {uplift_weighted_avg:.4f}')

        axes[1].set_xticks(percentiles)
        axes[1].legend(loc='upper right')
        axes[1].axhline(y=0, color='black', linewidth=1)
        axes[1].set_xlabel('Percentile')
        axes[1].set_title('Response rate by percentile')

    return axes


def plot_treatment_balance_curve(uplift, treatment, random=True, winsize=0.1):
    """Plot Treatment Balance curve.

    Args:
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        random (bool): Draw a random curve. Default is True.
        winsize (float): Size of the sliding window to apply. Should be between 0 and 1, extremes excluded. Default is 0.1.

    Returns:
        Object that stores computed values.
    """

    check_consistent_length(uplift, treatment)
    check_is_binary(treatment)

    if (winsize <= 0) or (winsize >= 1):
        raise ValueError(
            'winsize should be between 0 and 1, extremes excluded')

    x_tb, y_tb = treatment_balance_curve(
        uplift, treatment, winsize=int(len(uplift) * winsize))

    _, ax = plt.subplots(ncols=1, nrows=1, figsize=(14, 7))

    ax.plot(x_tb, y_tb, label='Model', color='b')

    if random:
        y_tb_random = np.average(treatment) * np.ones_like(x_tb)

        ax.plot(x_tb, y_tb_random, label='Random', color='black')
        ax.fill_between(x_tb, y_tb, y_tb_random, alpha=0.2, color='b')

    ax.legend()
    ax.set_title('Treatment balance curve')
    ax.set_xlabel('Percentage targeted')
    ax.set_ylabel('Balance: treatment / (treatment + control)')

    return ax
