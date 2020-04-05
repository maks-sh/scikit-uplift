.. _in russian on habr.com: https://habr.com/ru/company/ru_mts/blog/485980/

**************
scikit-uplift
**************

**scikit-uplift (sklift)** is a Python module for basic approaches of uplift modeling built on top of scikit-learn.

Uplift prediction aims to estimate the causal impact of a treatment at the individual level.

More about uplift modelling problem read `in russian on habr.com`_.

Features
#########

* Comfortable and intuitive style of modelling like scikit-learn;

* Applying any estimator adheres to scikit-learn conventions;

* Almost all implemented approaches solve both the problem of classification and regression;

* A lot of metrics (Such as *Area Under Uplift Curve* or *Area Under Qini Curve*) are implemented to evaluate your uplift model.


**The package currently supports the following methods:**

1. Solo Model (aka Treatment Dummy) approach
2. Class Transformation (aka Class Variable Transformation or Revert Label) approach
3. Two Models (aka naïve approach, or difference score method, or double classifier approach) approach, including Dependent Data Representation

**And the following metrics:**

1. Uplift@k
2. Area Under Uplift Curve
3. Area Under Qini Curve

Project info
#############

* GitHub repository: https://github.com/maks-sh/scikit-uplift
* Github examples: https://github.com/maks-sh/scikit-uplift/tree/master/notebooks
* License: MIT

.. toctree::
   :hidden:

   self

.. toctree::
   :maxdepth: 2
   :caption: Contents

   install
   quick_start
   api/index
   tutorials
   changelog


===============

Papers and materials
#####################

1. Gutierrez, P., & Gérardy, J. Y.
	Causal Inference and Uplift Modelling: A Review of the Literature. In International Conference on 	Predictive Applications and APIs (pp. 1-13).

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
    “Mining for the Truly Responsive Customers and Prospects Using True-Lift Modeling: Comparison of New and Existing Methods.”
    Journal of Marketing Analytics 2 (4): 218–238.

===============

Tags
#####
**EN**: uplift modeling, uplift modelling, causal inference, causal effect, causality, individual treatment effect, true lift, net lift, incremental modeling

**RU**: аплифт моделирование, Uplift модель

**ZH**: 隆起建模,因果推断,因果效应,因果关系,个人治疗效应,真正的电梯,净电梯

===============

Indices and tables
###################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
