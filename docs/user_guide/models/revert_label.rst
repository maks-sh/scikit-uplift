.. _ClassTransformation:

********************
Class Transformation
********************

.. warning::
    This approach is only suitable for classification problem

Simple yet powerful and mathematically proven uplift modeling method, presented in 2012.
The main idea is to predict a slightly changed target :math:`Z_i`:

.. math::
    Z_i = Y_i \cdot W_i + (1 - Y_i) \cdot (1 - W_i),

* :math:`Z_i` - new target for the :math:`i` customer;

* :math:`Y_i` - previous target for the :math:`i` customer;

* :math:`W_i` - treatment flag assigned to the :math:`i` customer.

In other words, the new target equals 1 if a response in the treatment group is as good as a response in the control group and equals 0 otherwise:

.. math::
    Z_i = \begin{cases}
        1, & \mbox{if } W_i = 1 \mbox{ and } Y_i = 1 \\
        1, & \mbox{if } W_i = 0 \mbox{ and } Y_i = 0 \\
        0, & \mbox{otherwise}
       \end{cases}

Let's go deeper and estimate the conditional probability of the target variable:

.. math::
    P(Z=1|X = x) = \\
    = P(Z=1|X = x, W = 1) \cdot P(W = 1|X = x) + \\
    + P(Z=1|X = x, W = 0) \cdot P(W = 0|X = x) = \\
    = P(Y=1|X = x, W = 1) \cdot P(W = 1|X = x) + \\
    + P(Y=0|X = x, W = 0) \cdot P(W = 0|X = x).

We assume that :math:`W` is independent of :math:`X = x` by design.
Thus we have: :math:`P(W | X = x) = P(W)` and

.. math::
    P(Z=1|X = x) = \\
    = P^T(Y=1|X = x) \cdot P(W = 1) + \\
    + P^C(Y=0|X = x) \cdot P(W = 0)

Also, we assume that :math:`P(W = 1) = P(W = 0) = \frac{1}{2}`, which means that during the experiment the control and the treatment groups
were divided in equal proportions. Then we get the following:

.. math::
    P(Z=1|X = x) = \\
    = P^T(Y=1|X = x) \cdot \frac{1}{2} + P^C(Y=0|X = x) \cdot \frac{1}{2} \Rightarrow \\

    2 \cdot P(Z=1|X = x) = \\
    = P^T(Y=1|X = x) + P^C(Y=0|X = x) = \\
    = P^T(Y=1|X = x) + 1 - P^C(Y=1|X = x) \Rightarrow \\
    \Rightarrow P^T(Y=1|X = x) - P^C(Y=1|X = x) = \\
     = uplift = 2 \cdot P(Z=1|X = x) - 1

.. image:: ../../_static/images/user_guide/ug_revert_label_mem.png
    :align: center
    :alt: Mem about class transformation approach for uplift modeling

Thus, by doubling the estimate of the new target :math:`Z` and subtracting one we will get an estimation of the uplift:

.. math::
    uplift = 2 \cdot P(Z=1) - 1


This approach is based on the assumption: :math:`P(W = 1) = P(W = 0) = \frac{1}{2}`. That is the reason that it has to be used
only in cases where the number of treated customers (communication) is equal to the number of control customers (no communication).

.. hint::
    In sklift this approach corresponds to the :class:`.ClassTransformation` class.

References
==========

1️⃣ Maciej Jaskowski and Szymon Jaroszewicz. Uplift modeling for clinical trial data. ICML Workshop on Clinical Data Analysis, 2012.

Examples using ``sklift.models.ClassTransformation``
====================================================

.. |Open In Colab1| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero_EN.ipynb
.. |Open In Colab2| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/RetailHero.ipynb

1. The overview of the basic approaches to the Uplift Modeling problem

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

2. The 2nd place solution of X5 RetailHero uplift contest by `Kirill Liksakov <https://github.com/kirrlix1994>`_

.. list-table::
    :align: center
    :widths: 12 10 8

    * - In English 🇬🇧
      - `nbviewer <https://nbviewer.jupyter.org/github/kirrlix1994/Retail_hero/blob/master/Retail_hero_contest_2nd_place_solution.ipynb>`__
      - `github <https://github.com/kirrlix1994/Retail_hero>`__