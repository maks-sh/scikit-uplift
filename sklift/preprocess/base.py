import numpy as np


def balancer(X, treatment, y, random_state=0, verbose=False):
    # ToDo: random_state
    # ToDo: return pandas.DataFrame if isinstance(X, pandas.DataFrame)
    X_ctrl, y_ctrl = np.array(X[treatment == 0]), np.array(y[treatment == 0])
    X_trmnt, y_trmnt = np.array(X[treatment == 1]), np.array(y[treatment == 1])

    values, treatment_counts = np.unique(treatment, return_counts=True)

    if treatment_counts[0] > treatment_counts[1]:
        np.random.seed(seed=random_state)
        idx = np.random.choice(X_ctrl.shape[0], treatment_counts[1], replace=False)
        X_ctrl, y_ctrl = X_ctrl[idx, :], y_ctrl[idx]

    else:
        np.random.seed(seed=random_state)
        idx = np.random.choice(X_trmnt.shape[0], treatment_counts[0], replace=False)
        X_trmnt, y_trmnt = X_trmnt[idx, :], y_trmnt[idx]

    X_mod, y_mod = np.vstack((X_ctrl, X_trmnt)), np.hstack((y_ctrl, y_trmnt))
    treatment_mod = np.hstack((np.zeros(X_ctrl.shape[0]), np.ones(X_trmnt.shape[0])))

    if verbose:
        print(f"Treatment percent in initial  data: {treatment_counts[1] / len(treatment):.3f}")
        print(f"Treatment percent in modified  data: {np.unique(treatment_mod, return_counts=True)[1][1] / len(treatment_mod):.3f}")
        print('Initial train data shape:', X.shape)
        print('Modified train data shape:', X_mod.shape, '\n')

    return X_mod, treatment_mod, y_mod
