# Release History

## Legend for changelogs

* 🔥 something big that you couldn’t do before.
* 💥 something that you couldn’t do before.
* 📝 a miscellaneous minor improvement.
* 🔨 something that previously didn’t work as documentated – or according to reasonable expectations – should now work.
* ❗️ you will need to change your code to have the same effect in the future; or a feature will be removed in the future.

## Version 0.2.0

### [User Guide](https://scikit-uplift.readthedocs.io/en/latest/user_guide/index.html)

* 🔥 Add [User Guide](https://scikit-uplift.readthedocs.io/en/latest/user_guide/index.html)

### [sklift.models](https://scikit-uplift.readthedocs.io/en/latest/api/models.html)

* 💥 Add `treatment interaction` method to [SoloModel](https://scikit-uplift.readthedocs.io/en/latest/api/models/SoloModel.html) approach by [@AdiVarma27](https://github.com/AdiVarma27).

### [sklift.metrics](https://scikit-uplift.readthedocs.io/en/latest/api/metrics.html)

* 💥 Add [uplift_by_percentile](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/uplift_by_percentile.html) function by [@ElisovaIra](https://github.com/ElisovaIra).
* 💥 Add [weighted_average_uplift](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/weighted_average_uplift.html) function by [@ElisovaIra](https://github.com/ElisovaIra).
* 💥 Add [perfect_uplift_curve](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/perfect_uplift_curve.html) function.
* 💥 Add [perfect_qini_curve](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/perfect_qini_curve.html) function.
* 🔨 Add normalization in [uplift_auc_score](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/uplift_auc_score.html) and [qini_auc_score](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/qini_auc_score.html) functions.
* ❗ Remove metrics `auuc` and `auqc`. In exchange for them use respectively [uplift_auc_score](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/uplift_auc_score.html) and [qini_auc_score](https://scikit-uplift.readthedocs.io/en/latest/api/metrics/qini_auc_score.html)

### [sklift.viz](https://scikit-uplift.readthedocs.io/en/latest/api/viz.html)

* 💥 Add [plot_uplift_curve](https://scikit-uplift.readthedocs.io/en/latest/api/viz/plot_uplift_curve.html) function.
* 💥 Add [plot_qini_curve](https://scikit-uplift.readthedocs.io/en/latest/api/viz/plot_qini_curve.html) function.
* ❗ Remove `plot_uplift_qini_curves`.

### Miscellaneous

* 💥 Add contributors in main Readme and in main page of docs.
* 💥 Add [contributing guide](https://scikit-uplift.readthedocs.io/en/latest/contributing.html).
* 💥 Add [code of conduct](https://github.com/maks-sh/scikit-uplift/blob/master/.github/CODE_OF_CONDUCT.md).
* 📝 Reformat [Tutorials](https://scikit-uplift.readthedocs.io/en/latest/tutorials.html) page.
* 📝 Add github buttons in docs.
* 📝 Add logo compatibility with pypi.

## Version 0.1.2

### [sklift.models](https://scikit-uplift.readthedocs.io/en/v0.1.2/api/models.html)

* 🔨 Fix bugs in [TwoModels](https://scikit-uplift.readthedocs.io/en/v0.1.2/api/models.html#sklift.models.models.TwoModels) for regression problem.
* 📝 Minor code refactoring.

### [sklift.metrics](https://scikit-uplift.readthedocs.io/en/v0.1.2/api/metrics.html)

* 📝 Minor code refactoring.

### [sklift.viz](https://scikit-uplift.readthedocs.io/en/v0.1.2/api/viz.html)

* 💥 Add bar plot in [plot_uplift_by_percentile](https://scikit-uplift.readthedocs.io/en/v0.1.2/api/viz.html#sklift.viz.base.plot_uplift_by_percentile) by [@ElisovaIra](https://github.com/ElisovaIra).
* 🔨 Fix bug in [plot_uplift_by_percentile](https://scikit-uplift.readthedocs.io/en/v0.1.2/api/viz.html#sklift.viz.base.plot_uplift_by_percentile).
* 📝 Minor code refactoring.

## Version 0.1.1

### [sklift.viz](https://scikit-uplift.readthedocs.io/en/v0.1.1/api/viz.html)

* 💥 Add [plot_uplift_by_percentile](https://scikit-uplift.readthedocs.io/en/v0.1.1/api/viz.html#sklift.viz.base.plot_uplift_by_percentile) by [@ElisovaIra](https://github.com/ElisovaIra).
* 🔨 Fix bug with import [plot_treatment_balance_curve](https://scikit-uplift.readthedocs.io/en/v0.1.1/api/viz.html#sklift.viz.base.plot_treatment_balance_curve).

### [sklift.metrics](https://scikit-uplift.readthedocs.io/en/v0.1.1/api/metrics.html)

* 💥 Add [response_rate_by_percentile](https://scikit-uplift.readthedocs.io/en/v0.1.1/api/viz.html#sklift.metrics.metrics.response_rate_by_percentile) by [@ElisovaIra](https://github.com/ElisovaIra).
* 🔨 Fix bug with import [uplift_auc_score](https://scikit-uplift.readthedocs.io/en/v0.1.1/api/metrics.html#sklift.metrics.metrics.uplift_auc_score) and [qini_auc_score](https://scikit-uplift.readthedocs.io/en/v0.1.1/metrics.html#sklift.metrics.metrics.qini_auc_score).
* 📝 Fix typos in docstrings.

### Miscellaneous

* 💥 Add tutorial ["Example of usage model from sklift.models in sklearn.pipeline"](https://nbviewer.jupyter.org/github/maks-sh/scikit-uplift/blob/master/notebooks/pipeline_usage_EN.ipynb).
* 📝 Add link to Release History in main Readme.md.

## Version 0.1.0

### [sklift.models](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/models.html)

* 📝 Fix typo in [TwoModels](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/models.html#sklift.models.models.TwoModels) docstring by [@spiaz](https://github.com/spiaz).
* 📝 Improve docstrings and add references to all approaches.

### [sklift.metrics](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/metrics.html)

* 💥 Add [treatment_balance_curve](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/metrics.html#sklift.metrics.metrics.treatment_balance_curve) by [@spiaz](https://github.com/spiaz).
* ❗️ The metrics `auuc` and `auqc` are now respectively renamed to [uplift_auc_score](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/metrics.html#sklift.metrics.metrics.uplift_auc_score) and [qini_auc_score](https://scikit-uplift.readthedocs.io/en/v0.1.0/metrics.html#sklift.metrics.metrics.qini_auc_score). So, `auuc` and `auqc` will be removed in 0.2.0.
* ❗️ Add a new parameter `startegy` in [uplift_at_k](https://scikit-uplift.readthedocs.io/en/v0.1.0/metrics.html#sklift.metrics.metrics.uplift_at_k).

### [sklift.viz](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/viz.html)

* 💥 Add [plot_treatment_balance_curve](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/viz.html#sklift.viz.base.plot_treatment_balance_curve) by [@spiaz](https://github.com/spiaz).
* 📝 fix typo in [plot_uplift_qini_curves](https://scikit-uplift.readthedocs.io/en/v0.1.0/api/viz.html#sklift.viz.base.plot_uplift_qini_curves) by [@spiaz](https://github.com/spiaz).

### Miscellaneous

* ❗️ Remove sklift.preprocess submodule.
* 💥 Add compatibility of tutorials with colab and add colab buttons by [@ElMaxuno](https://github.com/ElMaxuno).
* 💥 Add Changelog.
* 📝 Change the documentation structure. Add next pages: [Tutorials](https://scikit-uplift.readthedocs.io/en/v0.1.0/tutorials.html), [Release History](https://scikit-uplift.readthedocs.io/en/v0.1.0/changelog.html) and [Hall of fame](https://scikit-uplift.readthedocs.io/en/v0.1.0/hall_of_fame.html).