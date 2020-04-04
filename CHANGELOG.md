# Release History

## Legend for changelogs

* :fire: : something big that you couldn’t do before.
* :boom: : something that you couldn’t do before.
* :memo: : a miscellaneous minor improvement.
* :hammer: : something that previously didn’t work as documentated – or according to reasonable expectations – should now work.
* :exclamation: : you will need to change your code to have the same effect in the future; or a feature will be removed in the future.

## Version 0.0.4
*In development*

### [sklift.models](https://scikit-uplift.readthedocs.io/en/latest/models.html)

* :memo: fix typo in [TwoModels](https://scikit-uplift.readthedocs.io/en/latest/models.html#sklift.models.models.TwoModels) docstring by @spiaz 

### [sklift.metrics](https://scikit-uplift.readthedocs.io/en/latest/metrics.html)

* :exclamation: The metrics `auuc` and `auqc` are now respectively renamed to [uplift_auc_score](https://scikit-uplift.readthedocs.io/en/latest/metrics.html#sklift.metrics.metrics.uplift_auc_score) and [qini_auc_score](https://scikit-uplift.readthedocs.io/en/latest/metrics.html#sklift.metrics.metrics.qini_auc_score). So, `auuc` and `auqc` will be removed in 0.0.5

### Miscellaneous

* :memo: Add Changelog