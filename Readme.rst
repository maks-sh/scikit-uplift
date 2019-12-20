.. -*- mode: rst -*-

|Python36|_

.. |Python36| image:: https://img.shields.io/badge/python-3.6-blue.svg
.. _Python36: https://badge.fury.io/py/scikit-uplift
.. _RetailHero example notebook: https://github.com/maks-sh/scikit-uplift/notebooks/retailhero.ipynb

scikit-uplift
===============

**scikit-uplift** is a Python module for classic approaches for uplift modelling built on top of scikit-learn .

Quick Start
-----------

.. code-block:: python

    from sklift.models import SoloModel, ClassTransformation, TwoModels
    from catboost import CatBoostClassifier # Any estimator adheres to scikit-learn conventions.

    sm = SoloModel(CatBoostClassifier(verbose=100, random_state=777))
    sm = sm.fit(X_train, y_train, treat_train, estimator_fit_params={'plot': True})
    uplift_sm = sm.predict(X_val)

    cm = ClassTransformation(CatBoostClassifier(verbose=100, random_state=777))
    cm = cm.fit(X_train, y_train, treat_train, estimator_fit_params={'plot': True})
    uplift_cm = cm.predict(X_val)

    tm = TwoModels(
        estimator_trmnt=CatBoostClassifier(verbose=100, random_state=777),
        estimator_ctrl=CatBoostClassifier(verbose=100, random_state=777),
        method='vanilla'
    )
    tm = tm.fit(
        X_train, y_train, treat_train,
        estimator_trmnt_fit_params={'plot': True},
        estimator_ctrl_fit_params={'plot': True}
    )
    uplift_tm = tm.predict(X_val)


See the `RetailHero example notebook`_ for details.



Development
-----------

We welcome new contributors of all experience levels.

Important links
~~~~~~~~~~~~~~~

- Official source code repo: https://github.com/maks-sh/scikit-uplift/
- Issue tracker: https://github.com/maks-sh/scikit-uplift/issues

Installation and source code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can check the latest sources with the command::

    git clone https://github.com/maks-sh/scikit-uplift/scikit-uplift.git

And install by the following command::

    pip install -e .


===============

Papers and materials
---------------------
1. Gutierrez, P., & Gérardy, J. Y.
	Causal Inference and Uplift Modelling: A Review of the Literature. In International Conference on 	Predictive Applications and APIs (pp. 1-13).

2. Artem Betlei, Criteo Research; Eustache Diemert, Criteo Research; Massih-Reza Amini, Univ. Grenoble Alpes
	Dependent and Shared Data Representations improve Uplift Prediction in Imbalanced Treatment Conditions
	FAIM'18 Workshop on CausalML

3. Eustache Diemert, Artem Betlei, Christophe Renaudin, and Massih-Reza Amini. 2018.
    A Large Scale Benchmark for Uplift Modeling.
    In Proceedings of AdKDD & TargetAd (ADKDD’18). ACM, New York, NY, USA, 6 pages.

4. Athey, Susan, and Imbens, Guido. 2015.
    Machine learning methods for estimating heterogeneous causal effects.
    Preprint, arXiv:1504.01132. Google Scholar

5. Oscar Mesalles Naranjo. 2012.
    Testing a New Metric for Uplift Models.
    Dissertation Presented for the Degree of MSc in Statistics and Operational Research.