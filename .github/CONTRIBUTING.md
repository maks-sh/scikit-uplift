# Contributing to scikit-uplift

First off, thanks for taking the time to contribute! 🙌👍🎉

All development is done on GitHub: https://github.com/maks-sh/scikit-uplift.

## Submitting a bug report or a feature request

We use GitHub issues to track all bugs and feature requests.
Feel free to open an issue if you have found a bug or wish to see a feature implemented at https://github.com/maks-sh/scikit-uplift/issues.

## Contributing code

### How to contribute

The code in the master branch should meet the current release. 
So, please make a pull request to the ``dev`` branch.

1. Fork the [project repository](https://github.com/maks-sh/scikit-uplift).
2. Clone your fork of the scikit-uplift repo from your GitHub account to your local disk:
    ``` bash
    $ git clone git@github.com:YourLogin/scikit-uplift.git
    $ cd scikit-learn
    ```
3. Add the upstream remote. This saves a reference to the main scikit-uplift repository, which you can use to keep your repository synchronized with the latest changes:
    ``` bash
    $ git remote add upstream https://github.com/maks-sh/scikit-uplift.git
    ```
4. Synchronize your ``dev`` branch with the upstream ``dev`` branch:
    ``` bash
    $ git checkout dev
    $ git pull upstream dev
    ```
5. Create a feature branch to hold your development changes:
    ``` bash
    $ git checkout -b feature/my_new_feature
    ```
    and start making changes. Always use a feature branch. It’s a good practice.
6. Develop the feature on your feature branch on your computer, using Git to do the version control. When you’re done editing, add changed files using ``git add`` and then ``git commit``.
Then push the changes to your GitHub account with:

    ``` bash
    $ git push -u origin feature/my_new_feature
    ```
7. Create a pull request from your fork into ``dev`` branch.

### Styleguides

#### Python

We follow the PEP8 style guide for Python. Docstrings follow google style.

#### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line