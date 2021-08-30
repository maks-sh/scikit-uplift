import pytest
import numpy as np

from numpy.testing import assert_allclose

from ..viz import plot_qini_curve, plot_uplift_curve, plot_uplift_preds, plot_uplift_by_percentile, plot_treatment_balance_curve
from ..metrics import qini_curve, perfect_qini_curve, uplift_curve, perfect_uplift_curve
from ..viz import UpliftCurveDisplay

from sklearn.tree import DecisionTreeClassifier
from ..models import SoloModel

import matplotlib as mpl

def make_predictions():
    X_train, y_train, treat_train = (np.array([[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2]]),
                                     np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 1.0]))
    X_val, y_val, treat_val = (np.array([[5.1, 3.4, 1.5, 0.2], [5.0, 3.5, 1.3, 0.3], [4.5, 2.3, 1.3, 0.3]]),
                               np.array([0.0, 1.0, 0.0]), np.array([0.0, 1.0, 1.0]))

    model = DecisionTreeClassifier(random_state=0)

    s_model = SoloModel(model)
    s_model = s_model.fit(X_train, y_train, treat_train)
    uplift_preds = s_model.predict(X_val)

    return y_val, uplift_preds, treat_val

@pytest.mark.parametrize("random", [True, False])
@pytest.mark.parametrize("perfect", [True, False])
@pytest.mark.parametrize("negative_effect", [True, False])
def test_plot_qini_curve(random, perfect, negative_effect):
    y_true, uplift, treatment = make_predictions()

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

    assert isinstance(viz.line_, mpl.lines.Line2D)
    assert isinstance(viz.ax_, mpl.axes.Axes)
    assert isinstance(viz.figure_, mpl.figure.Figure)


@pytest.mark.parametrize(
    "qini_auc, estimator_name, expected_label",
    [
        (0.61, None, "plot_qini_curve = 0.61"),
        (0.61, "first", "first (plot_qini_curve = 0.61)"),
        (None, "None", "None")
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


@pytest.mark.parametrize("random", [True, False])
@pytest.mark.parametrize("perfect", [True, False])
def test_plot_uplift_curve(random, perfect):
    y_true, uplift, treatment = make_predictions()

    viz = plot_uplift_curve(y_true, uplift, treatment, random, perfect)

    x_actual, y_actual = uplift_curve(y_true, uplift, treatment)

    assert_allclose(viz.x_actual, x_actual)
    assert_allclose(viz.y_actual, y_actual)

    if random:
        x_baseline, y_baseline = x_actual, x_actual * y_actual[-1] / len(y_true)
        assert_allclose(viz.x_baseline, x_baseline)
        assert_allclose(viz.y_baseline, y_baseline)

    if perfect:
        x_perfect, y_perfect = perfect_uplift_curve(
            y_true, treatment)

        assert_allclose(viz.x_perfect, x_perfect)
        assert_allclose(viz.y_perfect, y_perfect)

    assert isinstance(viz.line_, mpl.lines.Line2D)
    assert isinstance(viz.ax_, mpl.axes.Axes)
    assert isinstance(viz.figure_, mpl.figure.Figure)


@pytest.mark.parametrize(
    "uplift_auc, estimator_name, expected_label",
    [
        (0.75, None, "plot_uplift_curve = 0.75"),
        (0.75, "first", "first (plot_uplift_curve = 0.75)"),
        (None, "None", "None")
    ]
)
def test_default_labels(uplift_auc, estimator_name, expected_label):
    x_actual = np.array([0, 1, 2, 3, 5, 6])
    y_actual = np.array([0.0, 1.0, 2.0, 3.0, 2.5, 1.5])

    disp = UpliftCurveDisplay(
        x_actual=x_actual,
        y_actual=y_actual,
        estimator_name=estimator_name
    ).plot(uplift_auc, title="plot_uplift_curve")

    assert disp.line_.get_label() == expected_label


def test_plot_uplift_preds():
    trmnt_preds = np.array([1,1,0,1,1,1])
    ctrl_preds = np.array([0,1,0,1,0,1])
	 
    viz = plot_uplift_preds(trmnt_preds, ctrl_preds, log=True, bins=5)
	 
    assert isinstance(viz[0], mpl.axes.Axes)
    assert isinstance(viz[1], mpl.axes.Axes)
    assert isinstance(viz[2], mpl.axes.Axes)
    
    with pytest.raises(ValueError):
    	plot_uplift_preds(trmnt_preds, ctrl_preds, log=True, bins=0)

def test_plot_uplift_by_percentile():
    y_true, uplift, treatment = make_predictions()

    viz = plot_uplift_by_percentile(y_true, uplift, treatment, strategy='overall',kind='line', bins=1, string_percentiles=True)

    assert viz.get_title() == "Uplift by percentile\nweighted average uplift = 0.5000"
    assert viz.get_xlabel() == "Percentile"
    assert viz.get_ylabel() == "Uplift = treatment response rate - control response rate"
    assert isinstance(viz, mpl.axes.Axes)
    viz = plot_uplift_by_percentile(y_true, uplift, treatment, strategy='by_group',kind='bar', bins=1, string_percentiles=False)

    assert viz[0].get_title() == "Uplift by percentile\nweighted average uplift = 0.5000"
    assert viz[1].get_xlabel() == "Percentile"
    assert viz[1].get_title() == "Response rate by percentile"
    assert isinstance(viz[0], mpl.axes.Axes)
    assert isinstance(viz[1], mpl.axes.Axes)
    viz = plot_uplift_by_percentile(y_true, uplift, treatment, strategy='by_group',kind='bar', bins=1, string_percentiles=True)

    assert viz[0].get_title() == "Uplift by percentile\nweighted average uplift = 0.5000"
    assert viz[1].get_xlabel() == "Percentile"
    assert viz[1].get_title() == "Response rate by percentile"
    assert isinstance(viz[0], mpl.axes.Axes)
    assert isinstance(viz[1], mpl.axes.Axes)
    
    viz = plot_uplift_by_percentile(y_true, uplift, treatment, strategy='by_group',kind='line', bins=1, string_percentiles=False)
    assert isinstance(viz, mpl.axes.Axes)
    

@pytest.mark.parametrize(
    "strategy, kind, bins, string_percentiles",
    [
        ("new_strategy", "bar", 1, False),
        ("by_group", "new_bar", 1, False),
        ("by_group", "bar", 0, False),
        ("by_group", "bar", 100, False),
        ("by_group", "bar", 1, 5)

    ]
)    
def test_plot_uplift_by_percentile_errors(strategy, kind, bins, string_percentiles):
    y_true, uplift, treatment = make_predictions()    
    with pytest.raises(ValueError):
    	viz = plot_uplift_by_percentile(y_true, uplift, treatment, strategy=strategy, kind=kind, bins=bins, string_percentiles=string_percentiles)


def test_plot_treatment_balance_curve():
    y_true, uplift, treatment = make_predictions()

    viz = plot_treatment_balance_curve(uplift, treatment, winsize=0.5)

    assert viz.get_title() == "Treatment balance curve"
    assert viz.get_xlabel() == "Percentage targeted"
    assert viz.get_ylabel() == "Balance: treatment / (treatment + control)"
    assert isinstance(viz, mpl.axes.Axes)
    
def test_plot_treatment_balance_errors():
	y_true, uplift, treatment = make_predictions()
	with pytest.raises(ValueError):		
		viz = plot_treatment_balance_curve(uplift, treatment, winsize=5) 