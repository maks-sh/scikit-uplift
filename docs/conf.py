import re
import os
import sys
import datetime

sys.path.insert(0, os.path.abspath("../"))


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    root = os.path.dirname(current_dir)
    version_file = os.path.join(root, "sklift", "__init__.py")
    with open(version_file) as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'scikit-uplift'
author = 'Maksim Shevchenko and Contributors'
copyright = "{}, {}".format(datetime.datetime.now().year, author)

# The full version, including alpha/beta/rc tags
release = get_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "recommonmark",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.bibtex"
]

bibtex_bibfiles = ['refs.bib']

master_doc = 'index'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'Readme.rst']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]
html_js_files = ['https://buttons.github.io/buttons.js']
html_logo = "./_static/sklift-logo.png"

# Removing the view source link
html_show_sourcelink = False

# Add supporting *.md files by recommonmark extension
source_suffix = ['.rst', '.md']

html_theme_options = {
    'navigation_depth': 3,
}

trim_footnote_reference_space = True