import warnings
import numpy as np
import pandas as pd
from sklearn.utils.extmath import stable_cumsum
from sklearn.utils.validation import check_consistent_length
from sklearn.metrics import auc


def uplift_curve(y_true, uplift, treatment):
    """Compute Uplift curve

    This is a general function, given points on a curve.  For computing the
    area under the Uplift Curve, see :func:`uplift_auc_score`.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        array (shape = [>2]), array (shape = [>2]): Points on a curve.

    See also:
        :func:`uplift_auc_score`: Compute the area under the Uplift curve.

        :func:`plot_uplift_qini_curves`: Plot Uplift and Qini curves.
    """

    # TODO: check the treatment is binary
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

    curve_values = (np.divide(y_trmnt, num_trmnt, out=np.zeros_like(y_trmnt), where=num_trmnt != 0) -
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
    area under the Qini Curve, see :func:`qini_auc_score`.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        array (shape = [>2]), array (shape = [>2]): Points on a curve.

    See also:
        :func:`qini_auc_score`: Compute the area under the Qini curve.

        :func:`plot_uplift_qini_curves`: Plot Uplift and Qini curves.
    """
    # TODO: check the treatment is binary
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


def uplift_auc_score(y_true, uplift, treatment):
    """Compute Area Under the Uplift Curve from prediction scores.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        float: Area Under the Uplift Curve.
    """
    # ToDO: Add normalization
    # ToDO: Add baseline
    return auc(*uplift_curve(y_true, uplift, treatment))


# FIXME: remove in 0.2.0
def auuc(y_true, uplift, treatment):
    """Compute Area Under the Uplift Curve from prediction scores.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        float: Area Under the Uplift Curve.

    .. warning::
        Metric `auuc` was renamed to :func:`uplift_auc_score`
        in version 0.1.0 and will be removed in 0.2.0
    """
    warnings.warn(
        'Metric `auuc` was renamed to `uplift_auc_score`'
        'in version 0.1.0 and will be removed in 0.2.0',
        FutureWarning
    )
    return uplift_auc_score(y_true, uplift, treatment)


def qini_auc_score(y_true, uplift, treatment):
    """Compute Area Under the Qini Curve (aka Qini coefficient) from prediction scores.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        float: Area Under the Qini Curve.
    """
    # ToDO: Add normalization
    # ToDO: Add baseline
    return auc(*qini_curve(y_true, uplift, treatment))


# FIXME: remove in 0.2.0
def auqc(y_true, uplift, treatment):
    """Compute Area Under the Qini Curve (aka Qini coefficient) from prediction scores.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.

    Returns:
        float: Area Under the Qini Curve.

    .. warning::
        Metric `auqc` was renamed to :func:`qini_auc_score`
        in version 0.1.0 and will be removed in 0.2.0
    """
    warnings.warn(
        'Metric `auqc` was renamed to `qini_auc_score`'
        'in version 0.1.0 and will be removed in 0.2.0',
        FutureWarning
    )
    return qini_auc_score(y_true, uplift, treatment)


def uplift_at_k(y_true, uplift, treatment, strategy, k=0.3):
    """Compute uplift at first k percentage of the total sample.

    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        k (float or int): If float, should be between 0.0 and 1.0 and represent the proportion of the dataset
            to include in the computation of uplift. If int, represents the absolute number of samples.
        strategy (string, ['overall', 'by_group']): Determines the calculating strategy.

            * ``'overall'``:
                The first step is taking the first k observations of all test data ordered by uplift prediction
                (overall both groups - control and treatment) and conversions in treatment and control groups
                calculated only on them. Then the difference between these conversions is calculated.

            * ``'by_group'``:
                Separately calculates conversions in top k observations in each group (control and treatment)
                sorted by uplift predictions. Then the difference between these conversions is calculated

    .. versionchanged:: 0.1.0

        * Add supporting absolute values for ``k`` parameter
        * Add parameter ``strategy``

    Returns:
        float: Uplift score at first k observations of the total sample.

    """
    # ToDo: checker that treatment is binary and all groups is not empty
    check_consistent_length(y_true, uplift, treatment)

    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    strategy_methods = ['overall', 'by_group']
    if strategy not in strategy_methods:
        raise ValueError(f'Uplift score supports only calculating methods in {strategy_methods},'
                         f' got {strategy}.'
                         )

    n_samples = len(y_true)
    order = np.argsort(uplift, kind='mergesort')[::-1]
    _, treatment_counts = np.unique(treatment, return_counts=True)
    n_samples_ctrl = treatment_counts[0]
    n_samples_trmnt = treatment_counts[1]

    k_type = np.asarray(k).dtype.kind

    if (k_type == 'i' and (k >= n_samples or k <= 0)
       or k_type == 'f' and (k <= 0 or k >= 1)):
        raise ValueError(f'k={k} should be either positive and smaller'
                         f' than the number of samples {n_samples} or a float in the '
                         f'(0, 1) range')

    if k_type not in ('i', 'f'):
        raise ValueError(f'Invalid value for k: {k_type}')

    if strategy == 'overall':
        if k_type == 'f':
            n_size = int(n_samples * k)
        else:
            n_size = k

        # ToDo: _checker_ there are observations among two groups among first k
        score_ctrl = y_true[order][:n_size][treatment[order][:n_size] == 0].mean()
        score_trmnt = y_true[order][:n_size][treatment[order][:n_size] == 1].mean()

    else:  # strategy == 'by_group':
        if k_type == 'f':
            n_ctrl = int((treatment == 0).sum() * k)
            n_trmnt = int((treatment == 1).sum() * k)

        else:
            n_ctrl = k
            n_trmnt = k

        if n_ctrl > n_samples_ctrl:
            raise ValueError(f'With k={k}, the number of the first k observations'
                             ' bigger than the number of samples'
                             f'in the control group: {n_samples_ctrl}'
                             )
        if n_trmnt > n_samples_trmnt:
            raise ValueError(f'With k={k}, the number of the first k observations'
                             ' bigger than the number of samples'
                             f'in the treatment group: {n_samples_ctrl}'
                             )

        score_ctrl = y_true[order][treatment[order] == 0][:n_ctrl].mean()
        score_trmnt = y_true[order][treatment[order] == 1][:n_trmnt].mean()

    return score_trmnt - score_ctrl


def response_rate_by_percentile(y_true, uplift, treatment, group, strategy='overall', bins=10):
    """Compute response rate (target mean in the control or treatment group) at each percentile.
    
    Args:
        y_true (1d array-like): Correct (true) target values.
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        group (string, ['treatment', 'control']): Group type for computing response rate: treatment or control.

            * ``'treatment'``:
                Values equal 1 in the treatment column.
            * ``'control'``:
                Values equal 0 in the treatment column.

        strategy (string, ['overall', 'by_group']): Determines the calculating strategy. Default is 'overall'.

            * ``'overall'``:
                The first step is taking the first k observations of all test data ordered by uplift prediction
                (overall both groups - control and treatment) and conversions in treatment and control groups
                calculated only on them. Then the difference between these conversions is calculated.
            * ``'by_group'``:
                Separately calculates conversions in top k observations in each group (control and treatment)
                sorted by uplift predictions. Then the difference between these conversions is calculated

        bins (int): Determines the number of bins (and relative percentile) in the data. Default is 10.
        
    Returns:
        array (shape = [>2]), array (shape = [>2]), array (shape = [>2]):
        response rate at each percentile for control or treatment group,
        variance of the response rate at each percentile,
        group size at each percentile.
    """
    
    group_types = ['treatment', 'control']
    strategy_methods = ['overall', 'by_group']
    
    n_samples = len(y_true)
    check_consistent_length(y_true, uplift, treatment)
    
    if group not in group_types:
        raise ValueError(f'Response rate supports only group types in {group_types},'
                         f' got {group}.') 

    if strategy not in strategy_methods:
        raise ValueError(f'Response rate supports only calculating methods in {strategy_methods},'
                         f' got {strategy}.')
    
    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(f'Bins should be positive integer.'
                         f' Invalid value bins: {bins}')
          
    if bins >= n_samples:
        raise ValueError(f'Number of bins = {bins} should be smaller than the length of y_true {n_samples}')
    
    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)
    order = np.argsort(uplift, kind='mergesort')[::-1]
    
    if group == 'treatment':
        trmnt_flag = 1
    else:  # group == 'control'
        trmnt_flag = 0
    
    if strategy == 'overall':
        y_true_bin = np.array_split(y_true[order], bins)
        trmnt_bin = np.array_split(treatment[order], bins)
        
        group_size = np.array([len(y[trmnt == trmnt_flag]) for y, trmnt in zip(y_true_bin, trmnt_bin)])
        response_rate = np.array([np.mean(y[trmnt == trmnt_flag]) for y, trmnt in zip(y_true_bin, trmnt_bin)])

    else:  # strategy == 'by_group'
        y_bin = np.array_split(y_true[order][treatment[order] == trmnt_flag], bins)
        
        group_size = np.array([len(y) for y in y_bin])
        response_rate = np.array([np.mean(y) for y in y_bin])

    variance = np.multiply(response_rate, np.divide((1 - response_rate), group_size))

    return response_rate, variance, group_size


def weighted_average_uplift(y_true, uplift, treatment, strategy='overall', bins=10):
    """
    Weighted average uplift.

    It is an average of uplift by percentile.
    Weights are sizes of the treatment group by percentile.

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
                sorted by uplift predictions. Then the difference between these conversions is calculated

        bins (int): Determines the number of bins (and the relative percentile) in the data. Default is 10.

    Returns:
        float: Weighted average uplift.
    """

    strategy_methods = ['overall', 'by_group']

    n_samples = len(y_true)
    check_consistent_length(y_true, uplift, treatment)

    if strategy not in strategy_methods:
        raise ValueError(f'Response rate supports only calculating methods in {strategy_methods},'
                         f' got {strategy}.')

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(f'Bins should be positive integer.'
                         f' Invalid value bins: {bins}')

    if bins >= n_samples:
        raise ValueError(f'Number of bins = {bins} should be smaller than the length of y_true {n_samples}')

    response_rate_trmnt, variance_trmnt, n_trmnt = response_rate_by_percentile(
        y_true, uplift, treatment, group='treatment', strategy=strategy, bins=bins)

    response_rate_ctrl, variance_ctrl, n_ctrl = response_rate_by_percentile(
        y_true, uplift, treatment, group='control', strategy=strategy, bins=bins)

    uplift_scores = response_rate_trmnt - response_rate_ctrl

    weighted_avg_uplift = 1 / np.sum(n_trmnt) * np.dot(n_trmnt, uplift_scores)

    return weighted_avg_uplift


def uplift_by_percentile(y_true, uplift, treatment, strategy='overall', bins=10, std=False, total=False):
    """Compute metrics: uplift, group size, group response rate, standard deviation at each percentile.

    Metrics in columns and percentiles in rows of pandas DataFrame:

        - ``n_treatment``, ``n_control`` - group sizes.
        - ``response_rate_treatment``, ``response_rate_control`` - group response rates.
        - ``uplift`` - treatment response rate substract control response rate.
        - ``std_treatment``, ``std_control`` - (optional) response rates standard deviation.
        - ``std_uplift`` - (optional) uplift standard deviation.

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
                sorted by uplift predictions. Then the difference between these conversions is calculated

        std (bool): If True, add columns with the uplift standard deviation and the response rate standard deviation. Default is False.
        total (bool): If True, add the last row with the total values. Default is False.
            The total uplift is a weighted average uplift. See :func:`weighted_average_uplift`.
            The total response rate is a response rate on the full data amount.
        bins (int): Determines the number of bins (and the relative percentile) in the data. Default is 10.

    Returns:
        pandas.DataFrame: Dataframe where metrics are by columns and percentiles are by rows.
    """

    strategy_methods = ['overall', 'by_group']

    n_samples = len(y_true)
    check_consistent_length(y_true, uplift, treatment)

    if strategy not in strategy_methods:
        raise ValueError(f'Response rate supports only calculating methods in {strategy_methods},'
                         f' got {strategy}.')

    if not isinstance(total, bool):
        raise ValueError(f'Flag total should be bool: True or False.'
                         f' Invalid value total: {total}')

    if not isinstance(std, bool):
        raise ValueError(f'Flag std should be bool: True or False.'
                         f' Invalid value std: {std}')

    if not isinstance(bins, int) or bins <= 0:
        raise ValueError(f'Bins should be positive integer.'
                         f' Invalid value bins: {bins}')

    if bins >= n_samples:
        raise ValueError(f'Number of bins = {bins} should be smaller than the length of y_true {n_samples}')

    y_true, uplift, treatment = np.array(y_true), np.array(uplift), np.array(treatment)

    response_rate_trmnt, variance_trmnt, n_trmnt = response_rate_by_percentile(
        y_true, uplift, treatment, group='treatment', strategy=strategy, bins=bins)

    response_rate_ctrl, variance_ctrl, n_ctrl = response_rate_by_percentile(
        y_true, uplift, treatment, group='control', strategy=strategy, bins=bins)

    uplift_scores = response_rate_trmnt - response_rate_ctrl
    uplift_variance = variance_trmnt + variance_ctrl

    percentiles = [round(p * 100 / bins, 1) for p in range(1, bins + 1)]

    df = pd.DataFrame({
        'percentile': percentiles,
        'n_treatment':n_trmnt,
        'n_control': n_ctrl,
        'response_rate_treatment': response_rate_trmnt,
        'response_rate_control': response_rate_ctrl,
        'uplift': uplift_scores
    })

    if total:
        response_rate_trmnt_total, variance_trmnt_total, n_trmnt_total = response_rate_by_percentile(
            y_true, uplift, treatment, strategy=strategy, group='treatment', bins=1)

        response_rate_ctrl_total, variance_ctrl_total, n_ctrl_total  = response_rate_by_percentile(
            y_true, uplift, treatment, strategy=strategy, group='control', bins=1)

        weighted_avg_uplift = 1 / n_trmnt_total * np.dot(n_trmnt, uplift_scores)

        df.loc[-1, :] = ['total', n_trmnt_total, n_ctrl_total, response_rate_trmnt_total,
                         response_rate_ctrl_total, weighted_avg_uplift]

    if std:
        std_treatment = np.sqrt(variance_trmnt)
        std_control = np.sqrt(variance_ctrl)
        std_uplift = np.sqrt(uplift_variance)

        if total:
            std_treatment = np.append(std_treatment, np.sum(std_treatment))
            std_control = np.append(std_control, np.sum(std_control))
            std_uplift = np.append(std_uplift, np.sum(std_uplift))

        df.loc[:, 'std_treatment'] = std_treatment
        df.loc[:, 'std_control'] = std_control
        df.loc[:, 'std_uplift'] = std_uplift

    df = df\
        .set_index('percentile', drop=True, inplace=False)\
        .astype({'n_treatment': 'int32', 'n_control': 'int32'})

    return df


def treatment_balance_curve(uplift, treatment, winsize):
    """Compute the treatment balance curve: proportion of treatment group in the ordered predictions.

    Args:
        uplift (1d array-like): Predicted uplift, as returned by a model.
        treatment (1d array-like): Treatment labels.
        winsize(int): Size of the sliding window for calculating the balance between treatment and control.

    Returns:
        array (shape = [>2]), array (shape = [>2]): Points on a curve.
    """
    uplift, treatment = np.array(uplift), np.array(treatment)

    desc_score_indices = np.argsort(uplift, kind="mergesort")[::-1]

    treatment = treatment[desc_score_indices]

    balance = np.convolve(treatment, np.ones(winsize), 'valid') / winsize
    idx = np.linspace(1, 100, len(balance))
    return idx, balance
