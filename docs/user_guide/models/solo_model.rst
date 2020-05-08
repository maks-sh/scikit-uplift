.. _SoloModel:

*********************************
Approaches with the same model
*********************************

One model with treatment as feature
========================================

The simplest and most intuitive solution: the model is trained on union of two groups, with the binary
communication flag acting as an additional feature. Each object from the test sample is scored twice:
with the communication flag equal to `1` and equal to `0`. Subtracting the probabilities for each observation,
we get the required uplift.

.. image:: ../../_static/images/SoloModel.png
    :align: center
    :alt: Solo model dummy method

.. hint::
    In sklift this approach corresponds to the  :class:`.SoloModel` class and the **dummy** method.

Treatment interaction
=========================

The approach described above has various modifications. For example, double the number of attributes by adding
the product of each attribute to the interaction flag:

.. image:: ../../_static/images/SoloModel_treatment_intercation.png
    :align: center
    :alt: Solo model treatment interaction method

.. hint::
    In sklift this approach corresponds to the :class:`.SoloModel` class and the **treatment_interaction** method.



References
==========

1️⃣ Lo, Victor. (2002). The True Lift Model - A Novel Data Mining Approach to Response Modeling in Database Marketing. SIGKDD Explorations. 4. 78-86.

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