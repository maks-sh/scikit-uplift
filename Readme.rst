.. -*- mode: rst -*-

|Python3|_ |PyPi|_ |Docs|_

.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg
.. _Python3: https://badge.fury.io/py/scikit-uplift

.. |PyPi| image:: https://badge.fury.io/py/scikit-uplift.svg
.. _PyPi: https://badge.fury.io/py/scikit-uplift

.. |Docs| image:: https://readthedocs.org/projects/scikit-uplift/badge/?version=latest
.. _Docs: https://scikit-uplift.readthedocs.io/en/latest/

.. |Open In Colab1| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab1: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb

.. |Open In Colab2| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab2: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb

.. |Open In Colab3| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab3: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/pipeline_usage_EN.ipynb

.. |Open In Colab4| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab4: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/pipeline_usage_RU.ipynb

.. _scikit-uplift.readthedocs.io: https://scikit-uplift.readthedocs.io/en/latest/
.. _Part 1: https://habr.com/ru/company/ru_mts/blog/485980/
.. _Part 2: https://habr.com/ru/company/ru_mts/blog/485976/

.. raw:: html

    <div align="center">
        <a href="https://pypi.org/project/scikit-uplift/">
            <img src="https://raw.githubusercontent.com/maks-sh/scikit-uplift/master/docs/_static/sklift-logo.png" alt="scikit-uplift (sklift) logo" height="256px" width="256px" style="display: block; margin: 0 auto;">
        </a>
        </br>
        <b>uplift modeling in scikit-learn style in python</b>
    </div>


scikit-uplift
===============

**scikit-uplift** is a Python module for classic approaches for uplift modeling built on top of scikit-learn.

Uplift prediction aims to estimate the causal impact of a treatment at the individual level.

More about uplift modelling problem read in russian on habr.com: `Part 1`_ and `Part 2`_.

**Features**:

* Comfortable and intuitive style of modelling like scikit-learn;

* Applying any estimator adheres to scikit-learn conventions;

* All approaches can be used in sklearn.pipeline (see example (`EN <https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/pipeline_usage_EN.ipynb>`__ |Open In Colab3|_, `RU <https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/pipeline_usage_RU.ipynb>`__ |Open In Colab4|_))

* Almost all implemented approaches solve both the problem of classification and regression;

* A lot of metrics (Such as *Area Under Uplift Curve* or *Area Under Qini Curve*) are implemented to evaluate your uplift model;

* Useful graphs for analyzing the built model.

Installation
-------------

**Install** the package by the following command from PyPI:

.. code-block:: bash

    pip install scikit-uplift

Or install from source:

.. code-block:: bash

    git clone https://github.com/maks-sh/scikit-uplift.git
    cd scikit-uplift
    python setup.py install

Documentation
--------------

The full documentation is available at `scikit-uplift.readthedocs.io`_.

Or you can build the documentation locally using `Sphinx <http://sphinx-doc.org/>`_ 1.4 or later:

.. code-block:: bash

    cd docs
    pip install -r requirements.txt
    make html

And if you now point your browser to ``_build/html/index.html``, you should see a documentation site.

Quick Start
-----------

See the **RetailHero tutorial notebook** (`EN <https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb>`__ |Open In Colab1|_, `RU <https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb>`__ |Open In Colab2|_) for details.

**Train and predict uplift model**

.. code-block:: python

    # import approaches
    from sklift.models import SoloModel, ClassTransformation, TwoModels
    # import any estimator adheres to scikit-learn conventions.
    from catboost import CatBoostClassifier

    # define approach
    sm = SoloModel(CatBoostClassifier(verbose=100, random_state=777))
    # fit model
    sm = sm.fit(X_train, y_train, treat_train, estimator_fit_params={{'plot': True})

    # predict uplift
    uplift_sm = sm.predict(X_val)

**Evaluate your uplift model**

.. code-block:: python

    # import metrics to evaluate your model
    from sklift.metrics import qini_auc_score, uplift_auc_score, uplift_at_k

    # Uplift@30%
    sm_uplift_at_k = uplift_at_k(y_true=y_val, uplift=uplift_sm, treatment=treat_val, k=0.3)
    # Area Under Qini Curve
    sm_qini_auc_score = qini_auc_score(y_true=y_val, uplift=uplift_sm, treatment=treat_val)
    # Area Under Uplift Curve
    sm_uplift_auc_score = uplift_auc_score(y_true=y_val, uplift=uplift_sm, treatment=treat_val)

**Vizualize the results**

.. code-block:: python

    # import vizualisation tools
    from sklift.viz import plot_uplift_preds, plot_uplift_qini_curves

    # get conditional predictions (probabilities) of performing a target action
    # with interaction for each object
    sm_trmnt_preds = sm.trmnt_preds_
    # get conditional predictions (probabilities) of performing a target action
    # without interaction for each object
    sm_ctrl_preds = sm.ctrl_preds_

    # draw probability distributions and their difference (uplift)
    plot_uplift_preds(trmnt_preds=sm_trmnt_preds, ctrl_preds=sm_ctrl_preds);
    # draw Uplift and Qini curves
    plot_uplift_qini_curves(y_true=y_val, uplift=uplift_sm, treatment=treat_val);

.. image:: https://raw.githubusercontent.com/maks-sh/scikit-uplift/master/docs/_static/images/readme_img1.png
    :align: center
    :alt: Probabilities Histogram, Uplift anf Qini curves



Development
-----------

We welcome new contributors of all experience levels.

Important links
~~~~~~~~~~~~~~~

- Official source code repo: https://github.com/maks-sh/scikit-uplift/
- Issue tracker: https://github.com/maks-sh/scikit-uplift/issues
- Release History: https://scikit-uplift.readthedocs.io/en/latest/changelog.html

===============

Papers and materials
---------------------
1. Gutierrez, P., & Gérardy, J. Y.
	Causal Inference and Uplift Modelling: A Review of the Literature.
	In International Conference on Predictive Applications and APIs (pp. 1-13).

2. Artem Betlei, Criteo Research; Eustache Diemert, Criteo Research; Massih-Reza Amini, Univ. Grenoble Alpes
	Dependent and Shared Data Representations improve Uplift Prediction in Imbalanced Treatment Conditions
	FAIM'18 Workshop on CausalML.

3. Eustache Diemert, Artem Betlei, Christophe Renaudin, and Massih-Reza Amini. 2018.
    A Large Scale Benchmark for Uplift Modeling.
    In Proceedings of AdKDD & TargetAd (ADKDD’18). ACM, New York, NY, USA, 6 pages.

4. Athey, Susan, and Imbens, Guido. 2015.
    Machine learning methods for estimating heterogeneous causal effects.
    Preprint, arXiv:1504.01132. Google Scholar.

5. Oscar Mesalles Naranjo. 2012.
    Testing a New Metric for Uplift Models.
    Dissertation Presented for the Degree of MSc in Statistics and Operational Research.

6. Kane, K., V. S. Y. Lo, and J. Zheng. 2014.
    Mining for the Truly Responsive Customers and Prospects Using True-Lift Modeling:
    Comparison of New and Existing Methods.
    Journal of Marketing Analytics 2 (4): 218–238.

7. Maciej Jaskowski and Szymon Jaroszewicz.
    Uplift modeling for clinical trial data.
    ICML Workshop on Clinical Data Analysis, 2012.

8. Lo, Victor. 2002.
    The True Lift Model - A Novel Data Mining Approach to Response Modeling in Database Marketing.
    SIGKDD Explorations. 4. 78-86.

9. Zhao, Yan & Fang, Xiao & Simchi-Levi, David. 2017.
    Uplift Modeling with Multiple Treatments and General Response Types. 10.1137/1.9781611974973.66.

===============

Tags
~~~~~~~~~~~~~~~
**EN**: uplift modeling, uplift modelling, causal inference, causal effect, causality, individual treatment effect, true lift, net lift, incremental modeling

**RU**: аплифт моделирование, Uplift модель

**ZH**: 隆起建模,因果推断,因果效应,因果关系,个人治疗效应,真正的电梯,净电梯

