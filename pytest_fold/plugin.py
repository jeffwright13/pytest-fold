import pytest
import subprocess
import tempfile
import re

from pathlib import Path

from _pytest.config import Config
# from _pytest.main import Session
from _pytest._io.terminalwriter import TerminalWriter

from pytest_fold.tuit import main as tuit
from pytest_fold.tuit import MyApp
from pytest_fold.utils import failures_matcher, errors_matcher, failed_test_start_marker, summary_matcher, lastline_matcher, OUTFILE, MARKERS

collect_ignore = [
    "setup.py",
    "plugin.py",
]


def pytest_addoption(parser):
    """Registers the pytest-fold option (--fold)"""
    group = parser.getgroup("fold")
    group.addoption(
        "--fold", action="store_true", help="fold: fold failed test output sections"
    )


@pytest.fixture(autouse=True)
def fold(request):
    """Checks to see if the --fold is enabled"""
    return request.config.getoption("--fold")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach session info to report for later use in pytest_runtest_logreport
    https://stackoverflow.com/questions/54717786/access-pytest-session-or-arguments-in-pytest-runtest-logreport
    """
    out = yield
    report = out.get_result()
    report.session = item.session


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    """
    Write console output to a file for use by TUI
    (part 1; used in conjunction with pytest_unconfigure, below)
    """
    if config.option.fold:
        tr = config.pluginmanager.getplugin("terminalreporter")
        if tr is not None:
            # identify and mark the very first line of terminal output
            try:
                config._pyfoldfirsttime
            except AttributeError:
                config._pyfoldfirsttime = True

            config._pyfoldoutputfile = tempfile.TemporaryFile("wb+")
            oldwrite = tr._tw.write

            def tee_write(s, **kwargs):  # sourcery skip: use-named-expression
                if config._pyfoldfirsttime:
                    # oldwrite(MARKERS["pytest_fold_firstline"] + "\n")
                    config._pyfoldoutputfile.write(
                        (MARKERS["pytest_fold_firstline"] + "\n").encode("utf-8")
                    )
                    config._pyfoldfirsttime = False

                # identify and mark the beginning of the errors section
                search = re.search(errors_matcher, s)
                if search:
                    # oldwrite(MARKERS["pytest_fold_errors"] + "\n")
                    config._pyfoldoutputfile.write(
                        (MARKERS["pytest_fold_errors"] + "\n").encode("utf-8")
                    )

                # identify and mark the beginning of the failures section
                search = re.search(failures_matcher, s)
                if search:
                    # oldwrite(MARKERS["pytest_fold_failures"] + "\n")
                    config._pyfoldoutputfile.write(
                        (MARKERS["pytest_fold_failures"] + "\n").encode("utf-8")
                    )

                # identify and mark the beginning of each failed test (the end of each
                # failed test is identified/marked in 'pytest_runtest_logreport' method)
                search = re.search(failed_test_start_marker, s)
                if search:
                    # oldwrite(MARKERS["pytest_fold_failed_test"] + "\n")
                    config._pyfoldoutputfile.write(
                        (MARKERS["pytest_fold_failed_test"] + "\n").encode("utf-8")
                    )

                # identify and mark the beginning of the final summary info line
                search = re.search(summary_matcher, s)
                if search:
                    # oldwrite(MARKERS["pytest_fold_terminal_summary"] + "\n")
                    config._pyfoldoutputfile.write(
                        (MARKERS["pytest_fold_terminal_summary"] + "\n").encode("utf-8")
                    )

                # identify and mark the very last line of terminal output
                search = re.search(lastline_matcher, s)
                if search:
                    # oldwrite(MARKERS["pytest_fold_lastline"] + "\n")
                    config._pyfoldoutputfile.write(
                        (MARKERS["pytest_fold_lastline"] + "\n").encode("utf-8")
                    )

                # Write this line's text along with its markup info to console
                oldwrite(s, **kwargs)

                # Mark up this line's text by passing it to an instance of TerminalWriter's
                # 'markup' method. Do not pass "flush" to the method or it wil throw an error.
                s1 = s
                kwargs.pop("flush") if "flush" in kwargs.keys() else None
                s1 = TerminalWriter().markup(s, **kwargs)

                # Encode the marked up line so it can be written to the config pbject
                if isinstance(s1, str):
                    marked_up = s1.encode("utf-8")
                config._pyfoldoutputfile.write(marked_up)

            tr._tw.write = tee_write


def pytest_unconfigure(config: Config):
    """
    Write console output to a file for use by TUI
    (part 2; used in conjunction with pytest_configure, above)
    """
    if hasattr(config, "_pyfoldoutputfile"):
        # get terminal contents, then write file
        config._pyfoldoutputfile.seek(0)
        sessionlog = config._pyfoldoutputfile.read()
        config._pyfoldoutputfile.close()

        # Undo our patching in the terminal reporter.
        config.pluginmanager.getplugin("terminalreporter")

        # write out to file
        with open(OUTFILE, "wb") as outfile:
            outfile.write(sessionlog)

        # Call TUI
        pyfold_tui()


def pyfold_tui():
    """
    Final code invocation after Pytest run has completed.
    This method calls the Pyfold TUI to display final results.
    """
    # MyApp.run()
    tuit()
    # path = Path.cwd()
    # subprocess.run(["python", f"{path}/pytest_fold/tui2.py"])
