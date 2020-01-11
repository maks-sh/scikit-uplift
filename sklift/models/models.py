import warnings
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_consistent_length
from sklearn.utils.multiclass import type_of_target


class SoloModel(BaseEstimator):
    """
    Fit solo model on whole dataset with 'treatment' as an additional feature.

    For each test example calculate predictions on new set twice:
    with treatment == '1' and with treatment == '0'.
    After that calculate uplift as a delta between these predictions.

    Return delta of predictions for each example.

    See more details in documentation here_.

    Args:
        estimator (estimator object implementing 'fit'): The object to use to fit the data.

    Attributes:
        trmnt_preds_ (array-like, shape (n_samples, )): Estimator predictions on samples when treatment.
        ctrl_preds_ (array-like, shape (n_samples, )): Estimator predictions on samples when control.

    Example:
        >>> from sklift.models import SoloModel # import approache
        >>> from catboost import CatBoostClassifier # import any estimator adheres to scikit-learn conventions.
        >>> sm = SoloModel(CatBoostClassifier(verbose=100, random_state=777)) # define approach
        >>> sm = sm.fit(X_train, y_train, treat_train, estimator_fit_params={{'plot': True}) # fit the model
        >>> uplift_sm = sm.predict(X_val) # predict uplift

    .. _here:
        https://scikit-uplift.readthedocs.io/en/latest/models.html#one-model-with-treatment-as-feature
    """

    def __init__(self, estimator):
        self.estimator = estimator
        self.trmnt_preds_ = None
        self.ctrl_preds_ = None
        self._type_of_target = None

    def fit(self, X, y, treatment, estimator_fit_params=None):
        """
        Fit the model according to the given training data.

        For each test example calculate predictions on new set twice: by the first and second models.
        After that calculate uplift as a delta between these predictions.

        Return delta of predictions for each example.

        Args:
            X (array-like, shape (n_samples, n_features)): Training vector, where n_samples is the number of samples and
                n_features is the number of features.
            y (array-like, shape (n_samples,)): Target vector relative to X.
            treatment (array-like, shape (n_samples,)): Binary treatment vector relative to X.
            estimator_fit_params (dict, optional): Parameters to pass to the fit method of the estimator.

        Returns:
            object: self
        """

        check_consistent_length(X, y, treatment)
        treatment_values = np.unique(treatment)
        if len(treatment_values) != 2:
            raise ValueError("Expected only two unique values, got %s" % len(treatment_values))

        if isinstance(X, np.ndarray):
            X_mod = np.column_stack((X, treatment))
        elif isinstance(X, pd.core.frame.DataFrame):
            X_mod = X.assign(treatment=treatment)
        else:
            raise TypeError("Expected numpy.ndarray or pandas.DataFrame in training vector X, got %s" % type(X))

        self._type_of_target = type_of_target(y)

        if estimator_fit_params is None:
            estimator_fit_params = {}
        self.estimator.fit(X_mod, y, **estimator_fit_params)
        return self

    def predict(self, X):
        """
        Perform uplift on samples in X.

        Args:
            X (array-like, shape (n_samples, n_features)) - Training vector, where n_samples is the number of samples
            and n_features is the number of features.

        Returns:
            array (shape (n_samples,)): uplift
        """
        if isinstance(X, np.ndarray):
            X_mod_trmnt = np.column_stack((X, np.ones(X.shape[0])))
            X_mod_ctrl = np.column_stack((X, np.zeros(X.shape[0])))
        elif isinstance(X, pd.core.frame.DataFrame):
            X_mod_trmnt = X.assign(treatment=np.ones(X.shape[0]))
            X_mod_ctrl = X.assign(treatment=np.zeros(X.shape[0]))
        else:
            raise TypeError("Expected numpy.ndarray or pandas.DataFrame in training vector X, got %s" % type(X))

        if self._type_of_target == 'binary':
            self.trmnt_preds_ = self.estimator.predict_proba(X_mod_trmnt)[:, 1]
            self.ctrl_preds_ = self.estimator.predict_proba(X_mod_ctrl)[:, 1]
        else:
            self.trmnt_preds_ = self.estimator.predict(X_mod_trmnt)
            self.ctrl_preds_ = self.estimator.predict(X_mod_ctrl)

        uplift = self.trmnt_preds_ - self.ctrl_preds_
        return uplift


class ClassTransformation(BaseEstimator):
    """
    Redefine target variable, which indicates that treatment make some impact on target or
    did target is negative without treatment.

    Z = Y * W + (1 - Y)(1 - W),

    where Y - target, W - communication flag.

    Then, Uplift ~ 2 * (Z == 1) - 1

    Returns only uplift predictions.

    See more details in documentation here_.

    Args:
        estimator (estimator object implementing 'fit'): The object to use to fit the data.

    Example:
        >>> from sklift.models import SoloModel # import approaches
        >>> from catboost import CatBoostClassifier # import any estimator adheres to scikit-learn conventions.
        >>> ct = ClassTransformation(CatBoostClassifier(verbose=100, random_state=777)) # define approach
        >>> ct = ct.fit(X_train, y_train, treat_train, estimator_fit_params={{'plot': True}) # fit the model
        >>> uplift_ct = ct.predict(X_val) # predict uplift

    .. _here:
        https://scikit-uplift.readthedocs.io/en/latest/models.html#class-transformation
    """
    def __init__(self, estimator):
        self.estimator = estimator
        self._type_of_target = None

    def fit(self, X, y, treatment, estimator_fit_params=None):
        """
        Fit the model according to the given training data.

        Args:
            X (array-like, shape (n_samples, n_features)): Training vector, where n_samples is the number of samples and
                n_features is the number of features.
            y (array-like, shape (n_samples,)): Target vector relative to X.
            treatment (array-like, shape (n_samples,)): Binary treatment vector relative to X.
            estimator_fit_params (dict, optional): Parameters to pass to the fit method of the estimator.

        Returns:
            object: self
        """

        # TODO: check the treatment is binary
        check_consistent_length(X, y, treatment)
        self._type_of_target = type_of_target(y)

        if self._type_of_target != 'binary':
            raise ValueError("This approach is only suitable for binary classification problem")
        # TODO: Заменить raise на Warning
        _, treatment_counts = np.unique(treatment, return_counts=True)
        if treatment_counts[0] != treatment_counts[1]:
            warnings.warn(
                "It is recommended to use this approach on treatment balanced data. Current sample size is unbalanced.",
                category=UserWarning,
                stacklevel=2
            )

        y_mod = (np.array(y) == np.array(treatment)).astype(int)

        if estimator_fit_params is None:
            estimator_fit_params = {}
        self.estimator.fit(X, y_mod, **estimator_fit_params)
        return self

    def predict(self, X):
        """
        Perform uplift on samples in X.

        Args:
            X (array-like, shape (n_samples, n_features)) - Training vector, where n_samples is the number of samples
                and n_features is the number of features.

        Returns
            array (shape (n_samples,)): uplift
        """
        uplift = 2 * self.estimator.predict_proba(X)[:, 1] - 1
        return uplift


class TwoModels(BaseEstimator):
    """
    Fit two separate models: on the treatment data and on the control data.

    See more details in documentation here_.

    Args:
        estimator_trmnt (estimator object implementing 'fit'): The object to use to fit the treatment data.
        estimator_ctrl (estimator object implementing 'fit'): The object to use to fit the control data.
        method (string, ‘vanila’, ’ddr_control’ or ‘ddr_treatment’, default='vanila'): Specifies the approach:
            * ‘vanila’ - two independent models
            * ’ddr_control’ -  dependent data representation (First train control classificator)
            * ’ddr_treatment’ -  dependent data representation (First train treatment classificator)


    Attributes:
        trmnt_preds_ (array-like, shape (n_samples, )): Estimator predictions on samples when treatment.
        ctrl_preds_ (array-like, shape (n_samples, )): Estimator predictions on samples when control.

    .. _here:
        https://scikit-uplift.readthedocs.io/en/latest/models.html#one-model-with-treatment-as-feature

    Example:
        >>> from sklift.models import TwoModels # import approach
        >>> from catboost import CatBoostClassifier # import any estimator adheres to scikit-learn conventions.
        >>> tm_ctrl = TwoModels( # define approach
        >>>     estimator_trmnt=CatBoostClassifier(silent=True, thread_count=2, random_state=42),
        >>>     estimator_ctrl=CatBoostClassifier(silent=True, thread_count=2, random_state=42),
        >>>     method='ddr_control'
        >>> )
        >>> tm_ctrl = tm_ctrl.fit( # fit the models
        >>>     X_train, y_train, treat_train,
        >>>     estimator_trmnt_fit_params={'cat_features': cat_features},
        >>>     estimator_ctrl_fit_params={'cat_features': cat_features}
        >>> )
        >>> uplift_tm_ctrl = tm_ctrl.predict(X_val) # predict uplift
    """

    def __init__(self, estimator_trmnt, estimator_ctrl, method='vanilla'):
        self.estimator_trmnt = estimator_trmnt
        self.estimator_ctrl = estimator_ctrl
        self.method = method
        self.trmnt_preds_ = None
        self.ctrl_preds_ = None
        self._type_of_target = None

        all_methods = ['vanilla', 'ddr_control', 'ddr_treatment']
        if method not in all_methods:
            raise ValueError("Two models approach supports only methods in %s, got"
                             " %s." % (all_methods, method))

    def fit(self, X, y, treatment, estimator_trmnt_fit_params=None, estimator_ctrl_fit_params=None):
        """
        Fit the model according to the given training data.

        For each test example calculate predictions on new set twice: by the first and second models.
        After that calculate uplift as a delta between these predictions.

        Return delta of predictions for each example.

        Args:
            X (array-like, shape (n_samples, n_features)): Training vector, where n_samples is the number of samples and
                n_features is the number of features.
            y (array-like, shape (n_samples,)): Target vector relative to X.
            treatment (array-like, shape (n_samples,)): Binary treatment vector relative to X.
            estimator_trmnt_fit_params (dict, optional): Parameters to pass to the fit method of the treatment estimator.
            estimator_ctrl_fit_params (dict, optional): Parameters to pass to the fit method of the control estimator.

        Returns:
            object: self
        """
        # TODO: check the treatment is binary
        check_consistent_length(X, y, treatment)
        self._type_of_target = type_of_target(y)

        X_ctrl, y_ctrl = X[treatment == 0], y[treatment == 0]
        X_trmnt, y_trmnt = X[treatment == 1], y[treatment == 1]

        if estimator_trmnt_fit_params is None:
            estimator_trmnt_fit_params = {}
        if estimator_ctrl_fit_params is None:
            estimator_ctrl_fit_params = {}

        if self.method == 'vanilla':
            self.estimator_ctrl.fit(
                X_ctrl, y_ctrl, **estimator_ctrl_fit_params
            )
            self.estimator_trmnt.fit(
                X_trmnt, y_trmnt, **estimator_trmnt_fit_params
            )

        if self.method == 'ddr_control':
            self.estimator_ctrl.fit(
                X_ctrl, y_ctrl, **estimator_ctrl_fit_params
            )
            if self._type_of_target == 'binary':
                ddr_control = self.estimator_ctrl.predict_proba(X_trmnt)[:, 1]
            else:
                ddr_control = self.estimator_ctrl.predict_(X_trmnt)

            if isinstance(X_trmnt, np.ndarray):
                X_trmnt_mod = np.column_stack((X_trmnt, ddr_control))
            elif isinstance(X_trmnt, pd.core.frame.DataFrame):
                X_trmnt_mod = X_trmnt.assign(ddr_control=ddr_control)
            else:
                raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X_trmnt))

            self.estimator_trmnt.fit(
                X_trmnt_mod, y_trmnt, **estimator_trmnt_fit_params
            )

        if self.method == 'ddr_treatment':
            self.estimator_trmnt.fit(
                X_trmnt, y_trmnt, **estimator_trmnt_fit_params
            )
            if self._type_of_target == 'binary':
                ddr_treatment = self.estimator_trmnt.predict_proba(X_ctrl)[:, 1]
            else:
                ddr_treatment = self.estimator_trmnt.predict(X_ctrl)[:, 1]

            if isinstance(X_ctrl, np.ndarray):
                X_ctrl_mod = np.column_stack((X_ctrl, ddr_treatment))
            elif isinstance(X_trmnt, pd.core.frame.DataFrame):
                X_ctrl_mod = X_ctrl.assign(ddr_treatment=ddr_treatment)
            else:
                raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X_ctrl))

            self.estimator_ctrl.fit(
                X_ctrl_mod, y_ctrl, **estimator_ctrl_fit_params
            )

        return self

    def predict(self, X):
        """
        Perform uplift on samples in X.

        Args:
            X (array-like, shape (n_samples, n_features)) - Training vector, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
            array (shape (n_samples,)): uplift
        """

        if self.method == 'ddr_control':
            if self._type_of_target == 'binary':
                self.ctrl_preds_ = self.estimator_ctrl.predict_proba(X)[:, 1]
            else:
                self.ctrl_preds_ = self.estimator_ctrl.predict(X)

            if isinstance(X, np.ndarray):
                X_mod = np.column_stack((X, self.ctrl_preds_))
            elif isinstance(X, pd.core.frame.DataFrame):
                X_mod = X.assign(ddr_control=self.ctrl_preds_)
            else:
                raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X_mod))
            self.trmnt_preds_ = self.estimator_trmnt.predict_proba(X_mod)[:, 1]

        elif self.method == 'ddr_treatment':
            if self._type_of_target == 'binary':
                self.trmnt_preds_ = self.estimator_trmnt.predict_proba(X)[:, 1]
            else:
                self.trmnt_preds_ = self.estimator_trmnt.predict_proba(X)[:, 1]

            if isinstance(X, np.ndarray):
                X_mod = np.column_stack((X, self.trmnt_preds_))
            elif isinstance(X, pd.core.frame.DataFrame):
                X_mod = X.assign(ddr_treatment=self.trmnt_preds_)
            else:
                raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X_mod))
            self.ctrl_preds_ = self.estimator_ctrl.predict_proba(X_mod)[:, 1]

        else:
            if self._type_of_target == 'binary':
                self.ctrl_preds_ = self.estimator_ctrl.predict_proba(X)[:, 1]
                self.trmnt_preds_ = self.estimator_trmnt.predict_proba(X)[:, 1]
            else:
                self.ctrl_preds_ = self.estimator_ctrl.predict(X)
                self.trmnt_preds_ = self.estimator_trmnt.predict(X)

        uplift = self.trmnt_preds_ - self.ctrl_preds_

        return uplift
