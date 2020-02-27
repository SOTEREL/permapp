import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "design_perma"
DESCRIPTION = ""
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
URL = "https://github.com/SOTEREL/design-app"
EMAIL = "vincent.lefoulon@free.fr"
AUTHOR = ", Vincent Lefoulon"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "django>=3.0.3",
        "djangorestframework>=3.11.0",
        "django-cors-headers>=3.2.1",
        "django-filter>=2.2.0",
    ],
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
