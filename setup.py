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
    version="0.7.5",
    author="Jeff Wright",
    author_email="jeff.washcloth@gmail.com",
    license="MIT",
    url="https://github.com/jeffwright13/pytest-fold",
    description="Mark console output and drop user into interactive text user interface",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=["pytest_fold"],
    py_modules=["pytest_fold"],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=6.2.5",
        "pytermgui>=4.1.0",
        "single-source>=0.2.0",
        "Faker>=13.0.0",
    ],
    classifiers=[
        "Framework :: Pytest",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="pytest testing fold output logs fail pytermtk asciimatics textual single-source",
    entry_points={
        "pytest11": ["pytest_fold = pytest_fold.plugin"],
        "console_scripts": ["tuitk = pytest_fold.tui_pytermtk:main"],
    },
)
