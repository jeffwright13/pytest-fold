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

A Pytest plugin to make multi-failure console output more manageable


Features
--------

TBD


Requirements
------------

Should be captured in `requirements.txt` and `setup.py`


Installation
------------

For now, this is manually installable as a Pytest plugin. Clone the project, create a venv, then install in editable mode:

* `git clone git@github.com:jeffwright13/pytest-fold.git`
* `cd pytest-fold`
* `python -m venv venv`
* `source venv/bin/activate`
* `pip install -e .`


Usage
-----

From top-level directory:

* `pytest --fold <other-pytest-options>`
* `python pytest_fold/tui.py`


Known Limitations / Issues
--------------------------

- Rudimentary user interface; needs a lot of love.
- Most ANSI color codes don't make it yet, meaning the tests are not color coded like they are on console (I have not yet figured out why some sections have ANSI control codes in them and some don't).
- Not fully tested with all combinations of output formats. Probably some use-cases where things won't work right.
- Need to figure out how to auto-launch the TUI after a Pytest run, so it is an 'end to end' solution
- It's a plugin, but not tied up and polished yet, and not on PyPi.
- ERROR output sections are treated just like FAILURES sections. It is assumed that the tester will want to see full text output from pytest when their tests cause an error to be asserted.
- `pytest-fold` does not mark stderr or stdout sections for folding. It is assumed that the tester is interested in seeing such output.
- `pytest-fold` is currently incompatible with `--tb=native` and will cause an INTERNALERROR if run together. (TODO: Fix this.)


Contributing
------------

Contributions are very welcome.
Please run pylakes and black on your code before submitting a PR (at some point I will implement [pre-commit](https://pypi.org/project/pre-commit/) in this project). Tests can be run with `tox`_; please ensure the coverage at least stays the same before you submit a pull request. (Although I haven't run these tests in 7 months, so who knows what condition they're in lol)


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-fold" is free and open source software.


Issues
------

If you encounter any problems, have feedback or requests, or anything else, please `file an issue`, along with a detailed description.
