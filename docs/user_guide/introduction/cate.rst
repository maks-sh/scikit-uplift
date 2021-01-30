******************************************
Causal Inference: Basics
******************************************

In a perfect world, we want to calculate a difference in a person's reaction received communication, and the reaction without receiving any communication.
But there is a problem: we can not make a communication (send an e-mail) and do not make a communication (no e-mail) at the same time.

.. image:: https://habrastorage.org/webt/fl/fi/dz/flfidz416o7of5j0nmgdjqqkzfe.jpeg
   :alt: Joke about Schrodinger's cat
   :align: center

Denoting :math:`Y_i^1` person :math:`i`’s outcome when receives the treatment (a presence of the communication) and :math:`Y_i^0` :math:`i`’s outcome when he receives no treatment (control, no communication), the :guilabel:`causal effect` :math:`\tau_i` of the treatment *vis-a-vis* no treatment is given by:

.. math::
    \tau_i = Y_i^1 - Y_i^0

Researchers are typically interested in estimating the :guilabel:`Conditional Average Treatment Effect` (CATE), that is, the expected causal effect of the treatment for a subgroup in the population:

.. math::
    CATE = E[Y_i^1 \vert X_i] - E[Y_i^0 \vert X_i]

Where :math:`X_i` - features vector describing :math:`i`-th person.

We can observe neither causal effect nor CATE for the :math:`i`-th object, and, accordingly, we can't optimize it.
But we can estimate CATE or *uplift* of an object:

.. math::
    \textbf{uplift} = \widehat{CATE} = E[Y_i \vert X_i = x, W_i = 1] - E[Y_i \vert X_i = x, W_i = 0]

Where:

- :math:`W_i \in {0, 1}` - a binary variable: 1 if person :math:`i` receives the :guilabel:`treatment group`, and 0 if person :math:`i` receives no treatment :guilabel:`control group`;
- :math:`Y_i` - person :math:`i`’s observed outcome, which is equal:

.. math::
    Y_i = W_i * Y_i^1 + (1 - W_i) * Y_i^0 = \
    \begin{cases}
        Y_i^1, & \mbox{if } W_i = 1 \\
        Y_i^0, & \mbox{if } W_i = 0 \\
    \end{cases}

This won’t identify the CATE unless one is willing to assume that :math:`W_i` is independent of :math:`Y_i^1` and :math:`Y_i^0` conditional on :math:`X_i`. This assumption is the so-called *Unconfoundedness Assumption* or the *Conditional Independence Assumption* (CIA) found in the social sciences and medical literature.
This assumption holds true when treatment assignment is random conditional on :math:`X_i`.
Briefly, this can be written as:

.. math::
    CIA : \{Y_i^0, Y_i^1\} \perp \!\!\! \perp W_i \vert X_i

Also, introduce additional useful notation.
Let us define the :guilabel:`propensity score`, :math:`p(X_i) = P(W_i = 1| X_i)`, i.e. the probability of treatment given :math:`X_i`.

References
==========

1️⃣ Gutierrez, P., & Gérardy, J. Y. (2017). Causal Inference and Uplift Modelling: A Review of the Literature. In International Conference on Predictive Applications and APIs (pp. 1-13).