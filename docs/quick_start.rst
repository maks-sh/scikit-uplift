.. _RU: https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb
.. _EN: https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb

.. |Open In Colab1| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab1: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb

.. |Open In Colab2| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab2: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb

***********
Quick Start
***********

See the **RetailHero tutorial notebook** (`EN`_ |Open In Colab1|_, `RU`_ |Open In Colab2|_) for details.

Train and predict your uplift model
====================================

Use the intuitive python API to train uplift models with `sklift.models  <https://www.uplift-modeling.com/en/latest/api/models/index.html>`__.

.. code-block:: python
    :linenos:

    # import approaches
    from sklift.models import SoloModel, ClassTransformation
    # import any estimator adheres to scikit-learn conventions.
    from lightgbm import LGBMClassifier

    # define models
    estimator = LGBMClassifier(n_estimators=10)

    # define metamodel
    slearner = SoloModel(estimator=estimator)

    # fit model
    slearner.fit(
        X=X_tr,
        y=y_tr,
        treatment=trmnt_tr,
    )

    # predict uplift
    uplift_slearner = slearner.predict(X_val)

Evaluate your uplift model
===========================

Uplift model evaluation metrics are available in `sklift.metrics  <https://www.uplift-modeling.com/en/latest/api/metrics/index.html>`__.

.. code-block:: python
    :linenos:

    # import metrics to evaluate your model
    from sklift.metrics import (
        uplift_at_k, uplift_auc_score, qini_auc_score, weighted_average_uplift
    )


    # Uplift@30%
    uplift_at_k = uplift_at_k(y_true=y_val, uplift=uplift_slearner,
                              treatment=trmnt_val,
                              strategy='overall', k=0.3)

    # Area Under Qini Curve
    qini_coef = qini_auc_score(y_true=y_val, uplift=uplift_slearner,
                               treatment=trmnt_val)

    # Area Under Uplift Curve
    uplift_auc = uplift_auc_score(y_true=y_val, uplift=uplift_slearner,
                                  treatment=trmnt_val)

    # Weighted average uplift
    wau = weighted_average_uplift(y_true=y_val, uplift=uplift_slearner,
                                  treatment=trmnt_val)

Vizualize the results
======================

Visualize performance metrics with `sklift.viz  <https://www.uplift-modeling.com/en/latest/api/viz/index.html>`__.

.. code-block:: python
    :linenos:

    from sklift.viz import plot_qini_curve
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Qini curves')

    plot_qini_curve(
        y_test, uplift_slearner, trmnt_test,
        perfect=True, name='Slearner', ax=ax
    );

    plot_qini_curve(
        y_test, uplift_revert, trmnt_test,
        perfect=False, name='Revert label', ax=ax
    );

.. image:: _static/images/quick_start_qini.png
    :alt: Example of model's qini curve, perfect qini curve and random qini curve


.. code-block:: python
    :linenos:

    from sklift.viz import plot_uplift_curve
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)
    ax.set_title('Uplift curves')

    plot_uplift_curve(
        y_test, uplift_slearner, trmnt_test,
        perfect=True, name='Slearner', ax=ax
    );

    plot_uplift_curve(
        y_test, uplift_revert, trmnt_test,
        perfect=False, name='Revert label', ax=ax
    );

.. image:: _static/images/quick_start_uplift.png
    :alt: Example of model's uplift curve, perfect uplift curve and random uplift curve

.. code-block:: python
    :linenos:

    from sklift.viz import plot_uplift_by_percentile

    plot_uplift_by_percentile(y_true=y_val, uplift=uplift_preds,
                              treatment=treat_val, kind='bar')

.. image:: _static/images/quick_start_wau.png
    :alt: Uplift by percentile
