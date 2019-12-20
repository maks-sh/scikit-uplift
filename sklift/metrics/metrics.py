import numpy as np


def uplift_at_k(y_true, uplift, treatment, k=0.3):
    order = np.argsort(-uplift)
    treatment_n = int((treatment == 1).sum() * k)
    treatment_p = y_true[order][treatment[order] == 1][:treatment_n].mean()
    control_n = int((treatment == 0).sum() * k)
    control_p = y_true[order][treatment[order] == 0][:control_n].mean()
    score_at_k = treatment_p - control_p
    return score_at_k
