#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-fold",
    version="0.1.0",
    author="Jeff Wright",
    author_email="jeff.washcloth@gmail.com",
    license="MIT",
    url="https://github.com/jeffwright13/pytest-fold",
    description="Fold console output and drop user into interactive shell",
    long_description=read("README.rst"),
    py_modules=["pytest_fold"],
    install_requires=["pytest>=6.5.2"],
    classifiers=[
        "Framework :: Pytest",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="pytest fold output logs fail",
    entry_points={
        "pytest11": [
            "fold = pytest_fold",
        ],
    },
)
