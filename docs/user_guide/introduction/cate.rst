.. meta::
    :description lang=en:
        Basic concept of causal inference: CATE, uplift, propensity score.


******************************************
Causal Inference: Basics
******************************************

To optimize the effect of exposure, we want to calculate the difference in human reactions in the presence of communication and in its absence.
The problem is that we can't simultaneously make a communication (for example, send an e-mail) and not make a communication (not send an e-mail).

.. image:: https://habrastorage.org/webt/fl/fi/dz/flfidz416o7of5j0nmgdjqqkzfe.jpeg
   :alt: Joke about Schrodinger's cat
   :align: center

Denoting :math:`Y_i^1` person :math:`i`’s outcome when he receives the active treatment and :math:`Y_i^0` :math:`i`’s outcome when he receives the control treatment, the :guilabel:`causal effect`, :math:`\tau_i`, of the active treatment *vis-a-vis* the control treatment is given by:

.. math::
    \tau_i = Y_i^1 - Y_i^0

Researchers are typically interested in estimating the :guilabel:`Conditional Average Treatment Effect` (CATE), that is, the expected causal effect of the active treatment for a subgroup in the population:

.. math::
    CATE = E[Y_i^1 \vert X_i] - E[Y_i^0 \vert X_i]

Where :math:`X_i` - features vector describing :math:`i`-th person.

We can observe neither causal effect nor CATE for the :math:`i`-th object, and, accordingly, we can't optimize it.
But we can estimate CATE or equation for the uplift of a specific object:

.. math::
    \textbf{uplift} = \widehat{CATE} = E[Y_i \vert X_i = x, W_i = 1] - E[Y_i \vert X_i = x, W_i = 0]

Where:

- :math:`W_i \in {0, 1}` - a binary variable taking on value 1 if person :math:`i` receives the active treatment (:guilabel:`treatment group`), and 0 if person i receives the control treatment (:guilabel:`control group`);
- :math:`Y_i` - person :math:`i`’s observed outcome, which is actually equal:

.. math::
    Y_i = W_i * Y_i^1 + (1 - W_i) * Y_i^0 = \
    \begin{cases}
        Y_i^1, & \mbox{if } W_i = 1 \\
        Y_i^0, & \mbox{if } W_i = 0 \\
    \end{cases}

This won’t identify the CATE unless one is willing to assume that :math:`W_i` is independent of :math:`Y_i^1` and :math:`Y_i^0` conditional on :math:`X_i`. This assumption is the so-called *Unconfoundedness Assumption* or the *Conditional Independence Assumption* (CIA) found in the social sciences and medical literature.
This assumption holds true when treatment assignment is random conditional on :math:`X_i`.
Briefly this can be written as:

.. math::
    CIA : \{Y_i^0, Y_i^1\} \perp \!\!\! \perp W_i \vert X_i

Also introduce additional useful notation.
Let us define the :guilabel:`propensity score`, :math:`p(X_i) = P(W_i = 1| X_i)`, i.e. the probability of treatment given :math:`X_i`.

References
==========

1️⃣ Gutierrez, P., & Gérardy, J. Y. (2017). Causal Inference and Uplift Modelling: A Review of the Literature. In International Conference on Predictive Applications and APIs (pp. 1-13).