# pytest-fold
## A Pytest plugin to make console output more manageable


https://user-images.githubusercontent.com/4308435/152477806-e78ed2f9-4646-4b0b-bb21-90c097a1e73c.mp4


## Introduction
Do you run long Pytest campaigns and get lots of failures? And then spend the next 15 minutes scrolling back in your console to find the one traceback that you're interested in drilling down into? Well, maybe `pytest-fold` can help. `pytest-fold` is a simple plugin that captures the output from your test runs, and redirects it into an interactive Text User Interface (TUI), where all your failed tests are "folded up" by default, showing only their titles and their status. Simply click on any test title to open it up and show its traceback information. Click again and it folds away once more.

## Features
- ANSI text markup support - whatever the output on your console looks like is how things are going to show up in the TUI
- Mouse and keyboard support 
- Support for all output formats/modes:
  - `-v`, `-vv`, `-no-header`, `--showlocals`, `--color=<yes|no|auto>`
  - all variants of `--tb` except "native"
- Support for other, simple output-manipulating plugins:
  - `pytest-clarity`
- Not supported: plugins that completely take over the console:
  - `pytest-sugar`

## Requirements
- Works on Mac, Linux, Windows
- Requires Pytest >= 6.2.5

## Installation
For now, this is manually installable as a Pytest plugin. Clone the project, create a venv, then install in editable mode:

* `git clone git@github.com:jeffwright13/pytest-fold.git`
* `cd pytest-fold`
* `python -m venv venv`
* `source venv/bin/activate`
* `pip install -e .`

## Usage
**Suppressing of Pytest's stdout/stderr capture (using the `-s` flag) is temorarily required. Otherwise the TUI's display will be corrupted.**

From top-level directory:

* `pytest --fold -s <other-pytest-options>`

To quit the TUI, either click the Quit button, or press `Ctrl-X`.

## Known Limitations / Issues
- You must invoke your Pytest test runs with the `--fold` option **plus** `-s` (see "Usage" above)
- Rudimentary user interface; needs a lot of love.
- Not fully tested with all combinations of output formats. Probably some use-cases where things won't work right.
- It's a plugin, but not tied up and polished yet, and not on PyPi.
- ERROR output sections are treated just like FAILURES sections. It is assumed that the tester will want to see full text output from pytest when their tests cause an error to be asserted.
- `pytest-fold` does not mark stderr or stdout sections for folding. It is assumed that the tester is interested in seeing such output.
- `pytest-fold` is currently incompatible with `--tb=native` and will cause an INTERNALERROR if run together. (TODO: Fix this.)

## Contributing
Contributions are very welcome.
Please run pylakes and black on your code before submitting a PR (at some point I will implement [pre-commit](https://pypi.org/project/pre-commit/) in this project). Tests can be run with `tox`_; please ensure the coverage at least stays the same before you submit a pull request. (Although I haven't run these tests in 7 months, so who knows what condition they're in lol)

## License
Distributed under the terms of the `MIT`_ license, "pytest-fold" is free and open source software.

## Issues
If you encounter any problems, have feedback or requests, or anything else, please `file an issue`, along with a detailed description.
