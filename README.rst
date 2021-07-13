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

* PHASE 1:
** Marks failing tests with a special "folding" mark

* PHASE 2:
** Folds console output for failing tests so they only take up a single line each
** Allows unfolding with user interaction


Requirements
------------

* [poetry](https://python-poetry.org/)


Installation
------------

You can install "pytest-fold" via `pip`_ from `PyPI`_::

    $ pip install pytest-fold


Usage
-----

* pytest --fold ...

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

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/jeffwright13/pytest-fold/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


