.. meta::
    :description lang=en:
        Comparison Uplift models with other model, such as Look-alike models (Positive unlabaled learning) or
        Response models.


****************************
Comparison with other models
****************************

Usually, product promotion occurs through communication with the customer through various channels: SMS, push, chatbot messages in social networks, and many others.
There are several ways to use machine learning to create segments for promotion:

.. image:: ../../_static/images/user_guide/ug_comparison_with_other_models.png
    :alt: Comparison with other models

- :guilabel:`The Look-alike model` (or Positive unlabaled learning) evaluates the probability that the client will complete the target action. The training sample uses known positive objects (for example, users who installed the app) and random negative objects (sampling a small subset of all other clients who did not have the app installed). The model will try to search for customers who are similar to those who made the target action.
- :guilabel:`The Response model` evaluates the probability that the client will complete the target action under the condition of communication (treatment). In this case, the training sample is data collected after some interaction with clients. In contrast to the first approach, we have real positive and negative observations at our disposal (for example, the customer issued a credit card or declined).
- :guilabel:`The Uplift model` evaluates the net effect of communication by trying to select only those clients who will perform a targeted action only when we interact. The model evaluates the difference in the client's behavior when there is a treatment and when there is no treatment.

When should we use uplift modeling?
It is usually used when a target action is performed by clients with a fairly high probability without any communication.
For example, we want to advertise a fairly popular product, but we don't want to spend our budget on customers who will buy this product without us.
If the product is not very popular and it is mostly bought only when promoting, then the task is reduced to response modeling.

References
==========

1️⃣ Radcliffe, N.J. (2007). Using control groups to target on predicted lift: Building and assessing uplift model. Direct Market J Direct Market Assoc Anal Council, 1:14–21, 2007.