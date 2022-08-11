.. _ClassTransformationReg:

********************
Transformed Outcome
********************

Let's redefine target variable, which indicates that treatment make some impact on target or
did target is negative without treatment:

.. math::
    Z = Y * \frac{(W - p)}{(p * (1 - p))}

* :math:`Y` - target vector,
* :math:`W` - vector of binary communication flags, and
* :math:`p` is a *propensity score* (the probabilty that each :math:`y_i` is assigned to the treatment group.).

It is important to note here that it is possible to estimate :math:`p` as the proportion of objects with :math:`W = 1`
in the sample. Or use the method from [2], in which it is proposed to evaluate math:`p` as a function of :math:`X` by
training the classifier on the available data :math:`X = x`, and taking the communication flag vector math:`W` as
the target variable.

.. image:: https://habrastorage.org/r/w1560/webt/35/d2/z_/35d2z_-3yhyqhwtw-mt-npws6xk.png
    :align: center
    :alt: Transformation of the target in Transformed Outcome approach

After applying the formula, we get a new target variable :math:`Z_i` and can train a regression model with the error
functional :math:`MSE= \frac{1}{n}\sum_{i=0}^{n} (Z_i - \hat{Z_i})^2`. Since it is precisely when using MSE that the
predictions of the model are the conditional mathematical expectation of the target variable.

It can be proved that the conditional expectation of the transformed target :math:`Z_i` is the desired causal effect:

.. math::
    E[Z_i| X_i = x] = Y_i^1 - Y_i^0 = \tau_i

.. hint::
    In sklift this approach corresponds to the :class:`.ClassTransformationReg` class.

References
==========

1️⃣  Susan Athey and Guido W Imbens. Machine learning methods for estimating heterogeneouscausal effects. stat, 1050:5, 2015.

2️⃣  P. Richard Hahn, Jared S. Murray, and Carlos Carvalho. Bayesian regression tree models for causal inference: regularization, confounding, and heterogeneous effects. 2019.