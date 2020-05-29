***************************
Uplift vs other models
***************************

Companies use different ways to promote a product to a customer through various channels: it can be SMS, push notification, chatbot message in social networks, and many others.
There are several ways to use machine learning to create promotion segments:

.. image:: ../../_static/images/user_guide/ug_comparison_with_other_models.png
    :alt: Comparison uplift models with Look-alike models (Positive unlabaled learning) and Response models

- :guilabel:`The Look-alike model` (or *Positive unlabeled learning*) evaluates a probability that the customer will accomplish a target action. A training dataset contains known positive objects (for instance, users who installed an app) and random negative objects (a random subset of all other customers who do not install the app). The model searches for customers who are similar to those who make the target action.
- :guilabel:`The Response model` evaluates the probability that the customer will accomplish the target action under the existence of communication (a.k.a treatment). In this case the training dataset is data collected after some interaction with the customers. In contrast to the first approach, we have confirmed positive and negative observations at our disposal (for instance, the customer who decides to issue a credit card or to decline an offer).
- :guilabel:`The Uplift model` evaluates the net effect of communication by trying to select only those customers who are going to perform the target action only when the company makes a communication with them. The model predicts a difference between the customer's behavior when there is a treatment (communication) and when there is no treatment (no communication).

When should we use uplift modeling?
Uplift modeling is used when the customer's target action is likely to happen without any communication.
For instance, we want to promote some popular product but we don't want to spend our marketing budget on customers who will buy the product anyway with or without communication.
If the product is not popular and it is has to be promoted to be bought, then a modeling task turns to the response modeling task.

References
==========

1️⃣ Radcliffe, N.J. (2007). Using control groups to target on predicted lift: Building and assessing uplift model. Direct Market J Direct Market Assoc Anal Council, 1:14–21, 2007.