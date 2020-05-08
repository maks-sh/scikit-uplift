.. _TwoModels:

**************************
Approaches with two models
**************************

.. _in the scikit-learn documentation: https://scikit-learn.org/stable/modules/calibration.html

The two-model approach can be found in almost any uplift modeling work, and is often used as a baseline.
However, the use of two models can lead to some unpleasant consequences: if the training will be used fundamentally
different models or the nature of the data of the test and control groups will be very different,
then the returned models will not be comparable with each other. As a result, the calculation of the uplift will
not be completely correct. To avoid this effect, it is necessary to calibrate the models so that their scores can be
interpolated as probabilities. Calibration of model probabilities is well described `in the scikit-learn documentation`_.

Two independent models
==========================

.. hint::
    In sklift this approach corresponds to the :class:`sklift.models.TwoModels` class and the **vanilla** method.

As the name implies, the approach is to model the conditional probabilities of the treatment and control groups
separately. The articles argue that this approach is rather weak, since both models focus on predicting the result
separately and can therefore skip the "weaker" differences in the samples.

.. image:: ../../_static/images/TwoModels_vanila.png
    :align: center
    :alt: Two independent models vanila

Two dependent models
========================

The dependent data representation approach is based on the classifier chain method originally developed
for multi-class classification problems. The idea is that if there are :math:`L` different labels, you can build
:math:`L` different classifiers, each of which solves the problem of binary classification and in the learning process,
each subsequent classifier uses the predictions of the previous ones as additional features.
The authors of this method proposed to use the same idea to solve the problem of uplift modeling in two stages.

.. hint::
    In sklift this approach corresponds to the :class:`.TwoModels` class and the **ddr_control** method.

At the beginning we train the classifier based on control data:

.. math::
    P^C = P(Y=1| X, W = 0),

then we will perform the :math:`P_C` predictions as a new feature for training the second classifier on test data,
thus effectively introducing a dependency between the two data sets:

.. math::
    P^T = P(Y=1| X, P_C(X), W = 1)

To get the uplift for each observation, calculate the difference:

.. math::
    uplift(x_i) = P^T (x_i, P_C(x_i)) - P^C(x_i)

Intuitively, the second classifier studies the difference between the expected result in the test and the control, i.e.
the uplift itself.

.. image:: ../../_static/images/TwoModels_ddr_control.png
    :align: center
    :alt: Two independent models dependent data representation control

Similarly, you can first train the :math:`P_T` classifier and then use its predictions as a trait for
the :math:`P_C` classifier.

.. hint::
    In sklift this approach corresponds to the :class:`.TwoModels` class and the **ddr_treatment** method.

References
==========

1️⃣ Betlei, Artem & Diemert, Eustache & Amini, Massih-Reza. (2018). Uplift Prediction with Dependent Feature Representation in Imbalanced Treatment and Control Conditions: 25th International Conference, ICONIP 2018, Siem Reap, Cambodia, December 13–16, 2018, Proceedings, Part V. 10.1007/978-3-030-04221-9_5.

2️⃣ Zhao, Yan & Fang, Xiao & Simchi-Levi, David. (2017). Uplift Modeling with Multiple Treatments and General Response Types. 10.1137/1.9781611974973.66.

Examples using ``sklift.models.SoloModel``
============================================

.. |Open In Colab1| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb
.. |Open In Colab2| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb

1. The overview of the basic approaches to solving the Uplift Modeling problem

.. list-table::
    :align: center
    :widths: 12 15 10 8

    * - In English 🇬🇧
      - |Open In Colab1|
      - `nbviewer <https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb>`__
      - `github <https://github.com/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb>`__
    * - In Russian 🇷🇺
      - |Open In Colab2|
      - `nbviewer <https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb>`__
      - `github <https://github.com/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb>`__