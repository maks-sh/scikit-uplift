import matplotlib.pyplot as plt
import numpy as np


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
