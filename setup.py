import os
import sys
from shutil import rmtree
import re

from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = "scikit-uplift"
DESCRIPTION = "Classic approaches of Uplift modelling in scikit-learn style in python"
MAINTAINER = 'Maksim Shevchenko'
URL = "https://github.com/maks-sh/scikit-uplift"
REQUIRES_PYTHON = ">=3.4.0"

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'Readme.rst')) as f:
    LONG_DESCRIPTION = f.read()

# What packages are required for this module to be executed?
try:
    with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
        REQUIRED = f.read().split("\n")
except FileNotFoundError:
    REQUIRED = []


def get_version():
    version_file = os.path.join(here, "sklift", "__init__.py")
    with open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


def get_test_requirements():
    pass


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print(s)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        sys.exit()


setup(
    name=NAME,
    version=get_version(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    maintainer=MAINTAINER,
    url=URL,
    packages=find_packages(exclude=["tests", "docs", "images"]),
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmdclass={"upload": UploadCommand},
)
