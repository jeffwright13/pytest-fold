# pytest-fold
## A Pytest plugin to make console output more manageable

### Using PyTermTk (experimental; incomplete):
https://user-images.githubusercontent.com/4308435/159505704-75683248-4734-4db9-9f6e-f4ec28ebfdb6.mp4

### ...using Textual TUI (Mac/Windows):
![ezgif com-gif-maker](https://user-images.githubusercontent.com/4308435/154848960-391fd62f-4859-4d2b-8d03-9f55f4b04cad.gif)

### ...using Asciimatics TUI (Mac/Windows/Linux):
![ezgif com-gif-maker(1)](https://user-images.githubusercontent.com/4308435/154856734-35695a56-8d4c-423f-89c6-c9f6522e0039.gif)


## Introduction
Do you run long Pytest campaigns and get lots of failures? And then spend the next 15 minutes scrolling back in your console to find the one traceback that you're interested in drilling down into? Well, maybe `pytest-fold` can help. `pytest-fold` is a simple plugin that captures the output from your test runs, and redirects it into an interactive Text User Interface (TUI), where all your failed tests are "folded up" by default, showing only their titles and their status. Simply click on any test title to open it up and show its traceback information.

## Features
- ANSI text markup support - whatever the output on your console looks like is how things are going to show up in the TUI
- Mouse and keyboard support (including scrolling in the Textual TUI)
- Support for FAILURES & ERRORS sections, as well as initial "test session starts", 'warnings summary', 'short test summary info' sections
- Support for all output formats/modes:
  - `-v`, `-vv`, `-no-header`, `--showlocals`, `--color=<yes|no|auto>`
  - all variants of `--tb` except "native"
- Support for other, simple output-manipulating plugins:
  - `pytest-clarity`
  - `pytest-emoji`
- Not supported: plugins that completely take over the console:
  - `pytest-sugar`

## Requirements
- Pytest >= 6.2.5
- Python >= 3.8
- Works on Mac, Linux, Windows (using Asciimatics TUI); and Mac (using Textual TUI)

## Installation
`pip install pytest-fold`

## Usage

From top-level directory:

* `pytest --fold [--fold-tui asciimatics|textual] <other-pytest-options>`

To quit the Ascimatics TUI, either click the Quit button, or press `Ctrl-X`. To quit the Textual TUI, either click the Quit button, or press `Q`.

If you have already exited the TUI and would like to re-enter it with the same data generated from the last Pytest run, type:

* `pytest --fold-now -s [--fold-tui asciimatics|textual]`

## Known Limitations / Issues
- `pytest-fold` does not display passed tests (that's not really the use case).
- Rudimentary user interfaces; both need a lot of love.
- Not fully tested with all combinations of output formats. Probably some use-cases where things won't work right.
- ERROR output sections are treated just like FAILURES sections. It is assumed that the tester will want to see full text output from pytest when their tests cause an error to be asserted.
- `pytest-fold` does not mark stderr or stdout sections for folding. It is assumed that the tester is interested in seeing such output.
- `pytest-fold` is currently incompatible with `--tb=native` and will cause an INTERNALERROR if run together. (TODO: Fix this.)
- `pytest-fold` may crash in the Asciimatics TUI if the console is resized.

## Contributing
Contributions are very welcome.
Please run pyflakes and black on your code before submitting a PR (at some point I will implement [pre-commit](https://pypi.org/project/pre-commit/) in this project).

## License
Distributed under the terms of the `MIT`_ license, "pytest-fold" is free and open source software.

## Issues
If you encounter any problems, have feedback or requests, or anything else, please `file an issue`, along with a detailed description.
