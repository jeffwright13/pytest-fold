import re
import pickle
import tempfile
import pytest

from _pytest.config import Config
from _pytest._io.terminalwriter import TerminalWriter
from _pytest.reports import TestReport
from pytest_fold.tui_pytermtk import main as tui
from pytest_fold.utils import (
    test_session_starts_matcher,
    errors_section_matcher,
    failures_section_matcher,
    warnings_summary_matcher,
    passes_section_matcher,
    short_test_summary_matcher,
    lastline_matcher,
    MARKERS,
    REPORTFILE,
    MARKEDTERMINALOUTPUTFILE,
    UNMARKEDTERMINALOUTPUTFILE,
)


collect_ignore = [
    "setup.py",
    "plugin.py",
]

reports = []


def pytest_addoption(parser):
    group = parser.getgroup("fold")
    group.addoption(
        "--fold",
        action="store_true",
        help="fold failed test output sections",
    )
    group.addoption(
        "--fold-tui",
        "--ft",
        action="store",
        default="pytermk",
        help="specify user interface ('pytermtk' ' k' | 'asciimatics' 'a' | 'textual' 't')",
        choices=["pytermtk", "k", "asciimatics", "a", "textual", "t"],
    )


def pytest_report_teststatus(report: TestReport, config: Config):
    """Construct list(s) of individial test report/report-info instances"""
    reports.append(report)


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    """
    Write console output to a file for use by TUI
    This code works by looking at every line sent by pytest to the terminal output,
    and based on the line, marking (or not marking) it depending on its category
    """
    if config.option.fold:
        tr = config.pluginmanager.getplugin("terminalreporter")
        if tr is not None:
            # identify and mark the very first line of terminal output
            try:
                config._pyfoldfirsttime
            except AttributeError:
                config._pyfoldfirsttime = True

            config._pyfold_unmarked_outputfile = tempfile.TemporaryFile("wb+")
            config._pyfold_marked_outputfile = tempfile.TemporaryFile("wb+")
            oldwrite = tr._tw.write

            # identify and mark each results section
            def tee_write(s, **kwargs):
                if re.search(test_session_starts_matcher, s):
                    config._pyfold_marked_outputfile.write(
                        (MARKERS["pytest_fold_test_session_starts"] + "\n").encode("utf-8")
                    )

                if re.search(errors_section_matcher, s):
                    config._pyfold_marked_outputfile.write(
                        (MARKERS["pytest_fold_errors_section"] + "\n").encode("utf-8")
                    )

                if re.search(failures_section_matcher, s):
                    config._pyfold_marked_outputfile.write(
                        (MARKERS["pytest_fold_failures_section"] + "\n").encode("utf-8")
                    )

                if re.search(warnings_summary_matcher, s):
                    config._pyfold_marked_outputfile.write(
                        (MARKERS["pytest_fold_warnings_summary"] + "\n").encode("utf-8")
                    )

                if re.search(passes_section_matcher, s):
                    config._pyfold_marked_outputfile.write(
                        (MARKERS["pytest_fold_passes_section"] + "\n").encode("utf-8")
                    )

                if re.search(short_test_summary_matcher, s):
                    config._pyfold_marked_outputfile.write(
                        (MARKERS["pytest_fold_short_test_summary"] + "\n").encode("utf-8")
                    )

                if re.search(lastline_matcher, s):
                    config._pyfold_marked_outputfile.write(
                        (MARKERS["pytest_fold_last_line"] + "\n").encode("utf-8")
                    )

                # Write this line's text along with its markup info to console
                oldwrite(s, **kwargs)

                # Mark up this line's text by passing it to an instance of TerminalWriter's
                # 'markup' method. Do not pass "flush" to the method or it will throw an error.
                s1 = s
                kwargs.pop("flush") if "flush" in kwargs.keys() else None
                s1 = TerminalWriter().markup(s, **kwargs)

                # Encode the marked up line so it can be written to the config object
                if isinstance(s1, str):
                    marked_up = s1.encode("utf-8")
                config._pyfold_marked_outputfile.write(marked_up)

                # Write this line's original (unmarked) text to unmarked file
                s_orig = s
                kwargs.pop("flush") if "flush" in kwargs.keys() else None
                s_orig = TerminalWriter().markup(s, **kwargs)
                if isinstance(s_orig, str):
                    unmarked_up = s_orig.encode("utf-8")
                config._pyfold_unmarked_outputfile.write(unmarked_up)

            # Write to both terminal/console and tempfiles:
            # _pyfold_marked_outputfile, _pyfold_unmarked_outputfile
            tr._tw.write = tee_write


def pytest_unconfigure(config: Config):
    """
    Write terminal and test results info to files for use by TUI
    """
    # Write terminal output to file
    if hasattr(config, "_pyfold_marked_outputfile"):
        # get terminal contents, then write file
        config._pyfold_marked_outputfile.seek(0)
        markedsessionlog = config._pyfold_marked_outputfile.read()
        config._pyfold_marked_outputfile.close()

    if hasattr(config, "_pyfold_unmarked_outputfile"):
        # get terminal contents, then write file
        config._pyfold_unmarked_outputfile.seek(0)
        unmarkedsessionlog = config._pyfold_unmarked_outputfile.read()
        config._pyfold_unmarked_outputfile.close()

        # Undo our patching in the terminal reporter
        config.pluginmanager.getplugin("terminalreporter")

        # Write marked-up results to file
        with open(MARKEDTERMINALOUTPUTFILE, "wb") as marked_file:
            marked_file.write(markedsessionlog)

        # Write un-marked-up results to file
        with open(UNMARKEDTERMINALOUTPUTFILE, "wb") as unmarked_file:
            unmarked_file.write(unmarkedsessionlog)

        # Write the reports list to file
        with open(REPORTFILE, "wb") as report_file:
            pickle.dump(reports, report_file)

    # Launch the TUI
    if config.getoption("--fold") == True:
        pyfold_tui(config)


def pyfold_tui(config: Config) -> None:
    """
    Final code invocation after Pytest run has completed.
    This method calls the Pyfold TUI to display final results.
    """
    # disable capturing while TUI runs to avoid error `redirected stdin is pseudofile, has
    # no fileno()`; adapted from https://githubmemory.com/repo/jsbueno/terminedia/issues/25
    if config.getoption("--fold") == True:
        capmanager = config.pluginmanager.getplugin("capturemanager")
        try:
            capmanager.suspend_global_capture(in_=True)
        finally:
            tui()
            capmanager.resume_global_capture()
