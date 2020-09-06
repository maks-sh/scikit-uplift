.. |Open In Colab3| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab3: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/pipeline_usage_EN.ipynb

.. |Open In Colab4| image:: https://colab.research.google.com/assets/colab-badge.svg
.. _Open In Colab4: https://colab.research.google.com/github/maks-sh/scikit-uplift/blob/master/notebooks/pipeline_usage_RU.ipynb

**************
scikit-uplift
**************

**scikit-uplift (sklift)** is an uplift modeling python package that provides fast sklearn-style models implementation, evaluation metrics and visualization tools.

The main idea is to provide easy-to-use and fast python package for uplift modeling. It delivers the model interface with the familiar scikit-learn API. One can use any popular estimator (for instance, from the Catboost library).

*Uplift modeling* estimates a causal effect of treatment and uses it to effectively target customers that are most likely to respond to a marketing campaign.

**Use cases for uplift modeling:**

* Target customers in the marketing campaign. Quite useful in promotion of some popular product where there is a big part of customers who make a target action by themself without any influence. By modeling uplift you can find customers who are likely to make the target action (for instance, install an app) only when treated (for instance, received a push).

* Combine a churn model and an uplift model to offer some bonus to a group of customers who are likely to churn.

* Select a tiny group of customers in the campaign where a price per customer is high.

Read more about *uplift modeling* problem in `User Guide <https://scikit-uplift.readthedocs.io/en/latest/user_guide/index.html>`__,

Articles in russian on habr.com: `Part 1 <https://habr.com/ru/company/ru_mts/blog/485980/>`__
and `Part 2 <https://habr.com/ru/company/ru_mts/blog/485976/>`__.

Features
#########

- Сomfortable and intuitive scikit-learn-like API;

- Applying any estimator compatible with scikit-learn (e.g. Xgboost, LightGBM, Catboost, etc.);

- All approaches can be used in `sklearn.pipeline`. See the example of usage: |Open In Colab3|_;

- Almost all implemented approaches solve classification and regression problem;

- More uplift metrics that you have ever seen in one place! Include brilliants like  *Area Under Uplift Curve* (AUUC) or *Area Under Qini Curve* (Qini coefficient) with ideal cases;

- Nice and useful viz for analyzing a performance model.


**The package currently supports the following methods:**

1. Solo Model (aka Treatment Dummy and Treatment interaction) approach
2. Class Transformation (aka Class Variable Transformation or Revert Label) approach
3. Two Models (aka naïve approach, or difference score method, or double classifier approach) approach, including Dependent Data Representation

**And the following metrics:**

1. Uplift@k
2. Area Under Uplift Curve
3. Area Under Qini Curve
4. Weighted average uplift

Project info
#############

* GitHub repository: https://github.com/maks-sh/scikit-uplift
* Github examples: https://github.com/maks-sh/scikit-uplift/tree/master/notebooks
* Documentation: https://www.uplift-modeling.com/en/latest/index.html
* Contributing guide: https://www.uplift-modeling.com/en/latest/contributing.html
* License: `MIT <https://github.com/maks-sh/scikit-uplift/blob/master/LICENSE>`__

Community
#############

Sklift is being actively maintained and welcomes new contributors of all experience levels.

- Please see our `Contributing Guide <https://www.uplift-modeling.com/en/latest/contributing.html>`_ for more details.
- By participating in this project, you agree to abide by its `Code of Conduct <https://github.com/maks-sh/scikit-uplift/blob/master/.github/CODE_OF_CONDUCT.md>`__.

If you have any questions, please contact us at team@uplift-modeling.com

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/0
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/0
   :alt: Top contributor 1

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/1
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/1
   :alt: Top contributor 2

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/2
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/2
   :alt: Top contributor 3

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/3
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/3
   :alt: Top contributor 4

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/4
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/4
   :alt: Top contributor 5

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/5
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/5
   :alt: Top contributor 6

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/6
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/6
   :alt: Top contributor 7

.. image:: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/images/7
   :target: https://sourcerer.io/fame/maks-sh/maks-sh/scikit-uplift/links/7
   :alt: Legend

.. toctree::
   :hidden:

   self

.. toctree::
   :maxdepth: 2
   :caption: Contents

   install
   quick_start
   user_guide/index
   api/index
   tutorials
   contributing
   changelog
   hall_of_fame


===============

Papers and materials
#####################

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

10. Nicholas J Radcliffe. 2007.
	Using control groups to target on predicted lift: Building and assessing uplift model.
	Direct Marketing Analytics Journal, (3):14–21, 2007.

11. Devriendt, F., Guns, T., & Verbeke, W. 2020.
	Learning to rank for uplift modeling. ArXiv, abs/2002.05897.

===============

Tags
#####
**EN**: uplift modeling, uplift modelling, causal inference, causal effect, causality, individual treatment effect, true lift, net lift, incremental modeling

**RU**: аплифт моделирование, Uplift модель

**ZH**: 隆起建模,因果推断,因果效应,因果关系,个人治疗效应,真正的电梯,净电梯