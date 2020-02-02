.. -*- mode: rst -*-

.. _RU: https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb
.. _EN: https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb

Quick Start
-----------

See the **RetailHero tutorial notebook** (`EN`_, `RU`_) for details.

**Train and predict your uplift model**

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
    from sklift.metrics import auqc, auuc, uplift_at_k

    # Uplift@30%
    sm_uplift_at_k = uplift_at_k(y_true=y_val, uplift=uplift_sm, treatment=treat_val, k=0.3)
    # Area Under Qini Curve
    sm_auqc = auqc(y_true=y_val, uplift=uplift_sm, treatment=treat_val)
    # Area Under Uplift Curve
    sm_auuc = auuc(y_true=y_val, uplift=uplift_sm, treatment=treat_val)

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

.. figure:: https://github.com/maks-sh/scikit-uplift/raw/master/notebooks/imgs/readme_img1.png
    :alt: Probabilities Histogram, Uplift anf Qini curves
