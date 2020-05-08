.. _ClassTransformation:

********************
Class Transformation
********************

.. warning::
    This approach is only suitable for classification problem

Quite an interesting and mathematically confirmed approach to the construction of the model, presented in 2012.
The method is to predict a slightly changed target:

.. math::
    z_i = y_i * w_i + (1 - y_i) * (1 - w_i), где

* :math:`z_i` - new target for :math:`i` customer;

* :math:`y_i` - old target :math:`i` customer;

* :math:`w_i` - treatment flag :math:`i` customer.

In other words, the new class is 1 if we know that on a particular observation, the result in the interaction
would be as good as in the control group if we could know the result in both groups:

.. math::
    z_i = \begin{cases}
        1, & \mbox{if } w_i = 1 \mbox{ and } y_i = 1 \\
        1, & \mbox{if } w_i = 0 \mbox{ and } y_i = 0 \\
        0, & \mbox{otherwise}
       \end{cases}

Let's describe in more detail what is the probability of a new target variable:

.. math::
    P(Z=1|X_1, ..., X_m) = \\
    = P(Z=1|X_1, ..., X_m, W = 1) * P(W = 1|X_1, ..., X_m, ) + \\
    + P(Z=1|X_1, ..., X_m, W = 0) * P(W = 0|X_1, ..., X_m, ) = \\
    = P(Y=1|X_1, ..., X_m, W = 1) * P(W = 1|X_1, ..., X_m, ) + \\
    + P(Y=0|X_1, ..., X_m, W = 0) * P(W = 0|X_1, ..., X_m, ).

We assume that :math:`W` does not depend on the attributes of :math:`X_1, ..., X_m`, because otherwise the experiment
design is not very well designed. Taking this, we have: :math:`P(W | X_1, ..., X_m, ) = P(W)` and

.. math::
    P(Z=1|X_1, ..., X_m) = \\
    = P^T(Y=1|X_1, ..., X_m) * P(W = 1) + \\
    + P^C(Y=0|X_1, ..., X_m) * P(W = 0).

Also assume that :math:`P(W = 1) = P(W = 0) = \frac{1}{2}`, i.e. during the experiment, the control and treatment groups
were divided in equal proportions. Then we get the following:

.. math::
    P(Z=1|X_1, ..., X_m) = \\
    = P^T(Y=1|X_1, ..., X_m) * \frac{1}{2} + P^C(Y=0|X_1, ..., X_m) *\frac{1}{2} \Rightarrow \\
    \Rightarrow 2 * P(Z=1|X_1, ..., X_m) = \\
    = P^T(Y=1|X_1, ..., X_m) + P^C(Y=0|X_1, ..., X_m) = \\
    = P^T(Y=1|X_1, ..., X_m) + 1 - P^C(Y=1|X_1, ..., X_m) \Rightarrow \\
    \Rightarrow P^T(Y=1|X_1, ..., X_m) - P^C(Y=1|X_1, ..., X_m) = \\
     = UPLIFT = 2 * P(Z=1|X_1, ..., X_m) - 1


Thus, by doubling the forecast of the new target and subtracting one from it, we get the value of the uplift itself,
i.e.

.. math::
    UPLIFT = 2 * P(Z=1) - 1

Based on the assumption described above: :math:`P(W = 1) = P(W = 0) = \frac{1}{2}`, this approach should be used
only in cases where the number of clients with whom we have communicated is equal to the number of clients with
whom there was no communication.

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

2. The 2nd place solution of X5 RetailHero uplift contest by `Kirill Liksakov <https://github.com/kirrlix1994>`_

.. list-table::
    :align: center
    :widths: 12 10 8

    * - In English 🇬🇧
      - `nbviewer <https://nbviewer.jupyter.org/github/kirrlix1994/Retail_hero/blob/master/Retail_hero_contest_2nd_place_solution.ipynb>`__
      - `github <https://github.com/kirrlix1994/Retail_hero>`__