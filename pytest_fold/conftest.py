import pytest
import tempfile

from _pytest.config import Config
from pathlib import Path
from pytest_fold import utils

OUTFILE = Path.cwd() / "console_output.fold"

MARKER1 = "==>MARKER1<=="
MARKER2 = "==>MARKER2<=="

collect_ignore = [
    "setup.py",
    "test_small.py",
    "test_something.py",
    "test_capture.py",
]

# Register pytest-fold option (--fold)
def pytest_addoption(parser):
    group = parser.getgroup("fold")
    group.addoption(
        "--fold", action="store_true", help="fold: fold failed test output sections"
    )


@pytest.fixture(autouse=True)
def fold(request):
    return request.config.getoption("--fold")


# attach session info to report for later use in pytest_runtest_logreport
# https://stackoverflow.com/questions/54717786/access-pytest-session-or-arguments-in-pytest-runtest-logreport
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    out = yield
    report = out.get_result()
    report.session = item.session


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_logreport(report):
    yield
    if report.when == "call" and report.failed and report.session.config.option.fold:
        report.longrepr.chain[0][0].reprentries[0].lines.insert(0, MARKER1)
        report.longrepr.chain[0][0].extraline = MARKER2


# Write console output to a file for use by TUI. Stolen from Pytest's pastebin.py
# Tip of the hat to pytest_session2file:
# (https://github.com/BuhtigithuB/pytest_session2file/blob/master/pytest_session2file/pytest_session2file.py)
@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    if config.option.fold:
        tr = config.pluginmanager.getplugin("terminalreporter")
        # If no terminal reporter plugin is present, nothing we can do here;
        # this can happen when this function executes in a worker node
        # when using pytest-xdist, for example.
        if tr is not None:
            config._pyfoldoutputfile = tempfile.TemporaryFile("wb+")
            oldwrite = tr._tw.write

            def tee_write(s, **kwargs):
                oldwrite(s, **kwargs)
                # if isinstance(s, str):
                #     s = s.encode("utf-8")
                config._pyfoldoutputfile.write(s.encode("utf-8"))

            tr._tw.write = tee_write


def pytest_unconfigure(config: Config) -> None:
    if hasattr(config, "_pyfoldoutputfile"):
        # get terminal contents, then write file
        config._pyfoldoutputfile.seek(0)
        sessionlog = config._pyfoldoutputfile.read()
        config._pyfoldoutputfile.close()
        # del config._pyfoldoutputfile
        # Undo our patching in the terminal reporter.
        tr = config.pluginmanager.getplugin("terminalreporter")
        del tr._tw.__dict__["write"]
        # write out to file
        with open(OUTFILE, "wb") as outfile:
            outfile.write(sessionlog)
        run_it()


def run_it():
    pass
