import pytest
import numpy as np

from numpy.testing import assert_allclose

from ..viz import plot_qini_curve
from ..metrics import qini_curve, perfect_qini_curve
from ..viz import UpliftCurveDisplay

from sklearn.tree import DecisionTreeClassifier
from ..models import SoloModel


@pytest.mark.parametrize("random", [True, False])
@pytest.mark.parametrize("perfect", [True, False])
@pytest.mark.parametrize("negative_effect", [True, False])
def test_plot_qini_curve(random, perfect, negative_effect):
    X_train, y_train, treat_train = np.array(
        [[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2]]), np.array([0.0, 0.0, 1.0]), np.array(
        [0.0, 1.0, 1.0])
    X_val, y_val, treat_val = np.array([[5.1, 3.4, 1.5, 0.2], [5.0, 3.5, 1.3, 0.3], [4.5, 2.3, 1.3, 0.3]]), np.array(
        [0.0, 1.0, 0.0]), np.array([0.0, 1.0, 1.0])

    model = DecisionTreeClassifier()

    s_model = SoloModel(model)

    s_model = s_model.fit(X_train, y_train, treat_train)

    uplift_preds = s_model.predict(X_val)

    y_true, uplift, treatment = y_val, uplift_preds, treat_val

    viz = plot_qini_curve(y_true, uplift, treatment, random, perfect, negative_effect)

    x_actual, y_actual = qini_curve(y_true, uplift, treatment)

    assert_allclose(viz.x_actual, x_actual)
    assert_allclose(viz.y_actual, y_actual)

    if random:
        x_baseline, y_baseline = x_actual, x_actual * y_actual[-1] / len(y_true)
        assert_allclose(viz.x_baseline, x_baseline)
        assert_allclose(viz.y_baseline, y_baseline)

    if perfect:
        x_perfect, y_perfect = perfect_qini_curve(
            y_true, treatment, negative_effect)

        assert_allclose(viz.x_perfect, x_perfect)
        assert_allclose(viz.y_perfect, y_perfect)

    import matplotlib as mpl

    assert isinstance(viz.line_, mpl.lines.Line2D)
    assert isinstance(viz.ax_, mpl.axes.Axes)
    assert isinstance(viz.figure_, mpl.figure.Figure)


@pytest.mark.parametrize(
    "qini_auc, estimator_name, expected_label",
    [
        (0.61, None, "plot_qini_curve = 0.61"),
        (0.61, "first", "first (plot_qini_curve = 0.61)")
    ]
)
def test_default_labels(qini_auc, estimator_name, expected_label):
    x_actual = np.array([0, 1, 2, 3, 5, 6])
    y_actual = np.array([0.0, 1.0, 2.0, 3.0, 2.5, 1.5])

    disp = UpliftCurveDisplay(
        x_actual=x_actual,
        y_actual=y_actual,
        estimator_name=estimator_name
    ).plot(qini_auc, title="plot_qini_curve")

    assert disp.line_.get_label() == expected_label
