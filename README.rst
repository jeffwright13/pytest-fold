===========
pytest-fold
===========

.. image:: https://img.shields.io/pypi/v/pytest-fold.svg
    :target: https://pypi.org/project/pytest-fold
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-fold.svg
    :target: https://pypi.org/project/pytest-fold
    :alt: Python versions

.. image:: https://travis-ci.com/jeffwright13/pytest-fold.svg?token=h2yU59uvx7ZpWMRdRGi8&branch=main
    :target: https://www.travis-ci.com/github/jeffwright13/pytest-fold
    :alt: See Build Status on Travis CI

A Pytest plugin to make console output more manageable

Features
--------

- PHASE 1:
 - Marks failing tests with a special "folding" mark

- PHASE 2:
 - Folds console output for failing tests so they only take up a single line each
 - Allows unfolding with user interaction


Requirements
------------

- [poetry](https://python-poetry.org/)


Installation
------------

You can install "pytest-fold" via `pip`_ from `PyPI`_::

    $ pip install pytest-fold


Usage
-----

    pytest --fold ...


Discussion
----------
`pytest-fold` does not mark ERROR output sections for folding. It is assumed that
the tester will want to see full text output from pytest when their tests cause
an error to be asserted. (TODO: make this configurable?)

`pytest-fold` does not mark stderr or stdout sections for folding. It is assumed
that the tester is interested in seeing such output. (TODO: make this configurable?)

`pytest-fold` is currently incompatible with `--tb=native` and will cause an
INTERNALERROR if run together. (TODO: Fix this.)


Contributing
------------
Contributions are very welcome. Please run flake8 and black on your code before
submitting (at some point I will implement [pre-commit](https://pypi.org/project/pre-commit/)
in this project). Tests can be run with `tox`_; please ensure the coverage at
least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-fold" is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.
