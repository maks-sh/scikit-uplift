.. meta::
    :description lang=en:
        Uplift modeling: classification of clients based on their response to a treatment.

******************************************
Clients
******************************************

It is customary to distinguish 4 types of clients based on their response to a treatment:

.. image:: ../../_static/images/user_guide/ug_clients_types.jpg
   :alt: Classification of clients based on their response to a treatment
   :width: 268 px
   :height: 282 px
   :align: center

- :guilabel:`Do-Not-Disturbs` *(aka Sleeping-dogs)* have a negative reaction to the marketing contact. They will purchase if NOT contacted, but will NOT purchase if contacted. The marketing budget applied to these contacts is not only wasted, it also has a negative impact on the results. For example, populations targeted for retention efforts by standard response models could result in withdrawing from current products or services.
- :guilabel:`Lost Causes` will NOT purchase the product whether they are contacted or not. The marketing budget applied to these contacts is wasted because it has no effect on their action.
- :guilabel:`Sure Things` will purchase the product whether they are contacted or not. The marketing budget applied to these contacts is wasted because it has no effect on their action.
- :guilabel:`Persuadables` have a positive reaction to the marketing contact. They purchase ONLY if contacted (or sometimes they purchase MORE or EARLIER only if contacted). They are the only efficient target that marketers should aim for. Methodologies discussed in this article will focus on finding the likely persuadable targets.

It is worth noting that depending on the client base and the company's characteristics, some of these types of clients may not be available. In addition, the performance of a target action depends heavily on various characteristics of the campaign itself, such as the channel of interaction or the type and size of the proposed marketing offer. To maximize profit, you should also select these parameters.

Thus, when predicting uplift and selecting the top predictions, we want to find only one of the four types: **persuadable**. There are several ways to do this.

References
==========

1️⃣ Kane, K., V. S. Y. Lo, and J. Zheng. Mining for the Truly Responsive Customers and Prospects Using True-Lift Modeling: Comparison of New and Existing Methods. Journal of Marketing Analytics 2 (4): 218–238. 2014.

2️⃣ Verbeke, Wouter & Baesens, Bart & Bravo, Cristián. (2018). Profit Driven Business Analytics: A Practitioner's Guide to Transforming Big Data into Added Value.