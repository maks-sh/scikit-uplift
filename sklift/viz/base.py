import matplotlib.pyplot as plt
import numpy as np
from ..metrics import uplift_curve, auuc, qini_curve, auqc


def plot_uplift_probs(trmnt_proba, ctrl_proba, log=None, bins=100):
    # ToDo: Добавить квантиль как параметр
    if log is not None:
        trmnt_proba = np.log(trmnt_proba + 1)
        ctrl_proba = np.log(ctrl_proba + 1)

    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(20, 7))
    axes[0].hist(
        trmnt_proba, bins=bins, color='b', alpha=0.3, label='Treated', histtype='stepfilled')
    axes[0].set_ylabel('Probability hist')
    axes[0].legend()
    axes[0].set_title('Treatment probabilities')

    axes[1].hist(
        ctrl_proba, bins=bins, alpha=0.5, color='y', label='Not treated', histtype='stepfilled')
    axes[1].legend()
    axes[1].set_title('Control probabilities')

    axes[2].hist(
        trmnt_proba - ctrl_proba, bins=bins, alpha=0.5, color='green', label='Uplift', histtype='stepfilled')
    axes[2].legend()
    axes[2].set_title('Uplift predictions')

    return axes


def plot_uplift_qini_curves(y_true, uplift, treatment, random=True, perfect=False):
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
    axes[0].set_xlabel('Number targteted')
    axes[0].set_ylabel('Relative gain: treatment - control')

    axes[1].legend()
    axes[1].set_title(f'Qini curve: AUQC={auqc(y_true, uplift, treatment):.2f}')
    axes[1].set_xlabel('Number targteted')
    axes[1].set_ylabel('Number of incremental outcome')

    return axes