*******************
Introduction
*******************

.. image::
   https://habrastorage.org/webt/hf/7i/nu/hf7inuu3agtnwl1yo0g--mznzno.jpeg

.. contents:: Table of Contents

Uplift modeling evaluates the effect of communication with clients and selects the group that is most affected.
This class of tasks is easy to implement, but it is not widely used in the machine learning courses or in the relevant literature.
In this section, we will get acquainted with uplift models and causal inference, consider how they differ from other models.

Comparison with other models
=============================

Usually, product promotion occurs through communication with the customer through various channels: SMS, push, chatbot messages in social networks, and many others.
There are several ways to use machine learning to create segments for promotion:

.. image::
   https://habrastorage.org/webt/iw/rp/zd/iwrpzdgxqq7nuss45c0ha0hpkrm.png

- **The Look-alike model** evaluates the probability that the client will complete the target action. The training sample uses known positive objects (for example, users who installed the app) and random negative objects (sampling a small subset of all other clients who did not have the app installed). The model will try to search for customers who are similar to those who made the target action.
- **The Response model** evaluates the probability that the client will complete the target action under the condition of communication. In this case, the training sample is data collected after some interaction with clients. In contrast to the first approach, we have real positive and negative observations at our disposal (for example, the customer issued a credit card or declined).
- **The Uplift model** evaluates the net effect of communication by trying to select only those clients who will perform a targeted action only when we interact. The model evaluates the difference in the client's behavior when there is a treatment and when there is no treatment.

When should we use uplift modeling?
It is usually used when a target action is performed by clients with a fairly high probability without any communication.
For example, we want to advertise a fairly popular product, but we don't want to spend our budget on customers who will buy this product without us.
If the product is not very popular and it is mostly bought only when promoting, then the task is reduced to response modeling.