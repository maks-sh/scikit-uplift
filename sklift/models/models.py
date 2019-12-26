import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_consistent_length


class SoloModel(BaseEstimator):
    """
    Fit solo model on whole dataset with 'treatment' as a feature.

    For each test example calculate predictions on new set twice:
    with treatment == '1' and with treatment == '0'.
    After that calculate uplift as a delta between these predictions.

    Return delta of predictions for each example.

    Parameters
    ----------
    :param estimator: estimator object implementing 'fit'
        The object to use to fit the data.

    Attributes
    ----------
    :attrib trmnt_proba_: array-like, shape (n_samples, )
        Probabilities of predictions on samples when treatment

    :attrib ctrl_proba_: array-like, shape (n_samples, )
        Probabilities of predictions on samples when control
    """

    def __init__(self, estimator):
        self.estimator = estimator
        self.trmnt_proba_ = None
        self.ctrl_proba_ = None
        self.treatment_values_ = None

        # check_estimator(estimator)

    def fit(self, X, y, treatment, estimator_fit_params=None):
        """
        Fit the model according to the given training data.

        Parameters
        ----------
        :param X: array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.
        :param y: array-like, shape (n_samples,)
            Target vector relative to X.
        :param treatment: array-like, shape (n_samples,)
            Binary treatment vector relative to X.
        :param estimator_fit_params:  dict, optional
            Parameters to pass to the fit method of the estimator.

        Returns
        -------
        :return self: object
        """

        check_consistent_length(X, y, treatment)
        self.treatment_values_ = np.unique(treatment)
        if len(self.treatment_values_) != 2:
            raise ValueError("Expected only two unique values, got %s" % len(self.treatment_values_))

        if isinstance(X, np.ndarray):
            X_mod = np.column_stack((X, treatment))
        elif isinstance(X, pd.core.frame.DataFrame):
            X_mod = X.assign(treatment=treatment)
        else:
            raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X))

        if estimator_fit_params is None: estimator_fit_params = {}
        self.estimator.fit(X_mod, y, **estimator_fit_params)
        return self

    def predict(self, X):
        """
        Perform uplift on samples in X.

        Parameters
        ----------
        :param X: array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.

        Returns
        -------
        :return uplift: array, shape (n_samples,)
        """
        if isinstance(X, np.ndarray):
            self.trmnt_proba_ = self.estimator.predict_proba(np.column_stack((X, np.ones(X.shape[0]))))[:, 1]
            self.ctrl_proba_ = self.estimator.predict_proba(np.column_stack((X, np.zeros(X.shape[0]))))[:, 1]
        elif isinstance(X, pd.core.frame.DataFrame):
            self.trmnt_proba_ = self.estimator.predict_proba(X.assign(treatment=np.ones(X.shape[0])))[:, 1]
            self.ctrl_proba_ = self.estimator.predict_proba(X.assign(treatment=np.zeros(X.shape[0])))[:, 1]
        else:
            raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X))

        uplift = self.trmnt_proba_ - self.ctrl_proba_
        return uplift


class ClassTransformation(BaseEstimator):
    """
    Redefine target variable, which indicates that treatment make some impact on target or
    did target is negative without treatment.
    Z = Y * W + (1 - Y)(1 - W)
    Uplift ~ 2P(Z == 1) - 1

    Return only uplift predictions

    Parameters
    ----------
    :param estimator: estimator object implementing 'fit'
        The object to use to fit the data.
    """

    def __init__(self, estimator):
        self.estimator = estimator
        # check_estimator(estimator)

    def fit(self, X, y, treatment, estimator_fit_params=None):
        """
        Fit the model according to the given training data.

        Parameters
        ----------
        :param X: array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.
        :param y: array-like, shape (n_samples,)
            Target vector relative to X.
        :param treatment: array-like, shape (n_samples,)
            Binary treatment vector relative to X.
        :param estimator_fit_params:  dict, optional
            Parameters to pass to the fit method of the estimator.

        Returns
        -------
        :return self: object
        """

        # TODO: check the treatment is binary
        # TODO: check the estimator is classificator
        check_consistent_length(X, y, treatment)

        _, treatment_counts = np.unique(treatment, return_counts=True)
        if treatment_counts[0] != treatment_counts[1]:
            raise ValueError("Class transformation approach supports only balanced on treatment data")

        y_mod = (y == treatment).astype(int)

        if estimator_fit_params is None:
            estimator_fit_params = {}
        self.estimator.fit(X, y_mod, **estimator_fit_params)
        return self

    def predict(self, X):
        uplift = 2 * self.estimator.predict_proba(X)[:, 1] - 1
        return uplift


class TwoModels(BaseEstimator):
    """

    Parameters
    ----------
    :param estimator_trmnt: estimator object implementing 'fit'
        The object to use to fit the treatment data.
    :param estimator_ctrl: estimator object implementing 'fit'
        The object to use to fit the control data.
    :param method: string, default: 'vanila'
        This parameter can be:
            - vanila
            - ddr_control
            - ddr_treatment

    Attributes
    ----------
    :attrib trmnt_proba_: array-like, shape (n_samples, )
        Probabilities of predictions on samples when treatment

    :attrib ctrl_proba_: array-like, shape (n_samples, )
        Probabilities of predictions on samples when control
    """

    def __init__(self, estimator_trmnt, estimator_ctrl, method='vanilla'):
        self.estimator_trmnt = estimator_trmnt
        self.estimator_ctrl = estimator_ctrl
        self.method = method
        self.trmnt_proba_ = None
        self.ctrl_proba_ = None

        # check_estimator(estimator_trmnt)
        # check_estimator(estimator_ctrl)

        all_methods = ['vanilla', 'ddr_control', 'ddr_treatment']
        if method not in all_methods:
            raise ValueError("Two models approach supports only methods in %s, got"
                             " %s." % (all_methods, method))

    def fit(self, X, y, treatment, estimator_trmnt_fit_params=None, estimator_ctrl_fit_params=None):
        """
        Fit the model according to the given training data.

        Parameters
        ----------
        :param X: array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.
        :param y: array-like, shape (n_samples,)
            Target vector relative to X.
        :param treatment: array-like, shape (n_samples,)
            Binary treatment vector relative to X.
        :param estimator_trmnt_fit_params:  dict, optional
            Parameters to pass to the fit method of the treatment estimator.
        :param estimator_ctrl_fit_params:  dict, optional
            Parameters to pass to the fit method of the control estimator.

        Returns
        -------
        :return self: object
        """
        # TODO: check the treatment is binary
        check_consistent_length(X, y, treatment)

        X_ctrl, y_ctrl = X[treatment == 0], y[treatment == 0]
        X_trmnt, y_trmnt = X[treatment == 1], y[treatment == 1]

        if estimator_trmnt_fit_params is None: estimator_trmnt_fit_params = {}
        if estimator_ctrl_fit_params is None: estimator_ctrl_fit_params = {}

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
            ddr_control = self.estimator_ctrl.predict_proba(X_trmnt)[:, 1]

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
            ddr_treatment = self.estimator_trmnt.predict_proba(X_ctrl)[:, 1]

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

        Parameters
        ----------
        :param X: array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.

        Returns
        -------
        :return uplift: array, shape (n_samples,)
        """

        if self.method == 'ddr_control':
            self.ctrl_proba_ = self.estimator_ctrl.predict_proba(X)[:, 1]

            if isinstance(X, np.ndarray):
                X_mod = np.column_stack((X, self.ctrl_proba_))
            elif isinstance(X, pd.core.frame.DataFrame):
                X_mod = X.assign(ddr_control=self.ctrl_proba_)
            else:
                raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X_mod))
            self.trmnt_proba_ = self.estimator_trmnt.predict_proba(X_mod)[:, 1]

        elif self.method == 'ddr_treatment':
            self.trmnt_proba_ = self.estimator_trmnt.predict_proba(X)[:, 1]

            if isinstance(X, np.ndarray):
                X_mod = np.column_stack((X, self.trmnt_proba_))
            elif isinstance(X, pd.core.frame.DataFrame):
                X_mod = X.assign(ddr_treatment=self.trmnt_proba_)
            else:
                raise TypeError("Expected numpy.ndarray or pandas.DataFrame, got %s" % type(X_mod))
            self.ctrl_proba_ = self.estimator_ctrl.predict_proba(X_mod)[:, 1]

        else:
            self.trmnt_proba_ = self.estimator_trmnt.predict_proba(X)[:, 1]
            self.ctrl_proba_ = self.estimator_ctrl.predict_proba(X)[:, 1]

        uplift = self.trmnt_proba_ - self.ctrl_proba_

        return uplift
