import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.validation import check_consistent_length
from ..metrics import (
    uplift_curve,
    auuc,
    qini_curve,
    auqc,
    response_rate_by_percentile,
    uplift_by_percentile,
    treatment_balance_curve
)


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
    # TODO: Add k as parameter: vertical line on plots
    check_consistent_length(trmnt_preds, ctrl_preds)

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(f'Bins should be positive integer. Invalid value for bins: {bins}')

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
    check_consistent_length(y_true, uplift, treatment)
    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    x_up, y_up = uplift_curve(y_true, uplift, treatment)
    x_qi, y_qi = qini_curve(y_true, uplift, treatment)

    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(14, 7))

    axes[0].plot(x_up, y_up, label='Model', color='b')
    axes[1].plot(x_qi, y_qi, label='Model', color='b')

    if random:
        up_ratio_random = (y_true[treatment == 1].sum() / len(y_true[treatment == 1]) -
                           y_true[treatment == 0].sum() / len(y_true[treatment == 0]))
        y_up_random = x_up * up_ratio_random

        qi_ratio_random = (y_true[treatment == 1].sum() - len(y_true[treatment == 1]) *
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

    axes[0].legend(loc='upper left')
    axes[0].set_title(f'Uplift curve: AUUC={auuc(y_true, uplift, treatment):.2f}')
    axes[0].set_xlabel('Number targeted')
    axes[0].set_ylabel('Relative gain: treatment - control')

    axes[1].legend(loc='upper left')
    axes[1].set_title(f'Qini curve: AUQC={auqc(y_true, uplift, treatment):.2f}')
    axes[1].set_xlabel('Number targeted')
    axes[1].set_ylabel('Number of incremental outcome')

    return axes


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

    n_samples = len(y_true)
    check_consistent_length(y_true, uplift, treatment)

    if strategy not in strategy_methods:
        raise ValueError(f'Response rate supports only calculating methods in {strategy_methods},'
                         f' got {strategy}.')

    if kind not in kind_methods:
        raise ValueError(f'Function supports only types of plots in {kind_methods},'
                         f' got {kind}.')

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(f'Bins should be positive integer. Invalid value bins: {bins}')

    if bins >= n_samples:
        raise ValueError(f'Number of bins = {bins} should be smaller than the length of y_true {n_samples}')

    df = uplift_by_percentile(y_true, uplift, treatment, strategy=strategy,
                              std=True, total=True, bins=bins)

    percentiles = df.index[:bins].values.astype(float)
    response_rate_trmnt, std_trmnt = df.loc[percentiles, 'response_rate_treatment'].values, \
                                     df.loc[percentiles, 'std_treatment'].values
    response_rate_ctrl, std_ctrl = df.loc[percentiles, 'response_rate_control'].values, \
                                   df.loc[percentiles, 'std_control'].values
    uplift_score, std_uplift = df.loc[percentiles, 'uplift'].values, \
                               df.loc[percentiles, 'std_uplift'].values
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
        axes.fill_between(percentiles, response_rate_trmnt, response_rate_ctrl, alpha=0.1, color='red')

        if np.amin(uplift_score) < 0:
            axes.axhline(y=0, color='black', linewidth=1)
        axes.set_xticks(percentiles)
        axes.legend(loc='upper right')
        axes.set_title(f'Uplift by percentile\nweighted average uplift = {uplift_weighted_avg:.2f}')
        axes.set_xlabel('Percentile')
        axes.set_ylabel('Uplift = treatment response rate - control response rate')

    else:  # kind == 'bar'
        delta = percentiles[0]
        fig, axes = plt.subplots(ncols=1, nrows=2, figsize=(8, 6), sharex=True, sharey=True)
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
        axes[0].set_title(f'Uplift by percentile\nweighted average uplift = {uplift_weighted_avg:.2f}')

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
    axes.set_ylabel('Balance: treatment / (treatment + control)')

    return axes
