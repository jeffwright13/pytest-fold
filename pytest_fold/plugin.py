import pytest
import tempfile
import re

from pathlib import Path
from _pytest.config import Config

OUTFILE = Path.cwd() / "console_output.fold"
MARKERS = {
    "pytest_fold_firstline": "==>PYTEST_FOLD_MARKER_FIRSTLINE<==",
    "pytest_fold_lastline": "==>PYTEST_FOLD_MARKER_LASTLINE<==",
    "pytest_fold_collectreport_begin": "==>PYTEST_FOLD_MARKER_COLLECTREPORT_BEGIN<==",
    "pytest_fold_collectreport_end": "==>PYTEST_FOLD_MARKER_COLLECTREPORT_END<==",
    "pytest_fold_sessionstart_begin": "==>PYTEST_FOLD_MARKER_SESSIONSTART_BEGIN<==",
    "pytest_fold_sessionstart_end": "==>PYTEST_FOLD_MARKER_SESSIONSTART_END<==",
    "pytest_fold_sessionfinish_begin": "==>PYTEST_FOLD_MARKER_SESSIONFINISH_BEGIN<==",
    "pytest_fold_sessionfinish_end": "==>PYTEST_FOLD_MARKER_SESSIONFINISH_END<==",
    "pytest_fold_runtest_logreport_begin": "==>PYTEST_FOLD_MARKER_SESSION_RUNTEST_LOGREPORT_BEGIN<==",
    "pytest_fold_runtest_logreport_end": "==>PYTEST_FOLD_MARKER_SESSION_RUNTEST_LOGREPORT_END<==",
    "pytest_fold_terminal_summary_begin": "==>PYTEST_FOLD_MARKER_TERMINAL_SUMMARY_BEGIN<==",
    "pytest_fold_terminal_summary_end": "==>PYTEST_FOLD_MARKER_TERMINAL_SUMMARY_END<==",
    "pytest_fold_pass_begin": "==>PYTEST_FOLD_MARKER_PASS_BEGIN<==",
    "pytest_fold_pass_end": "==>PYTEST_FOLD_MARKER_PASS_END<==",
    "pytest_fold_failure_begin": "==>PYTEST_FOLD_MARKER_FAILURE_BEGIN<==",
    "pytest_fold_failure_end": "==>PYTEST_FOLD_MARKER_FAILURE_END<==",
    "pytest_fold_experiment": "~@~@~@ EXPERIMENT @~@~@~",
}

collect_ignore = [
    "setup.py",
    "plugin.py",
    "test_small.py",
    "test_something.py",
    "test_capture.py",
]


def pytest_addoption(parser):
    """These two methods register the pytest-fold option (--fold)"""
    group = parser.getgroup("fold")
    group.addoption(
        "--fold", action="store_true", help="fold: fold failed test output sections"
    )


@pytest.fixture(autouse=True)
def fold(request):
    """These two methods register the pytest-fold option (--fold)"""
    return request.config.getoption("--fold")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_logstart(item, call):
#     """
#     Attach session info to report for later use in pytest_runtest_logreport
#     https://stackoverflow.com/questions/54717786/access-pytest-session-or-arguments-in-pytest-runtest-logreport
#     """
#     out = yield
#     report = out.get_result()
#     report.session = item.session

# @pytest.hookimpl(hookwrapper=True, trylast=True)
# def pytest_sessionstart(session):
#     """
#     Write pyfold section-begin marker before session starts
#     """
#     print(MARKERS["pytest_fold_sessionstart_begin"])
#     out = yield
#     print(MARKERS["pytest_fold_sessionstart_end"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_sessionfinish(session):
#     """
#     Write pyfold section-end marker after session finishes
#     """
#     print("\n")
#     print(MARKERS["pytest_fold_sessionfinish_begin"])
#     out = yield
#     print(MARKERS["pytest_fold_sessionfinish_end"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach session info to report for later use in pytest_runtest_logreport
    https://stackoverflow.com/questions/54717786/access-pytest-session-or-arguments-in-pytest-runtest-logreport
    """
    out = yield
    report = out.get_result()
    report.session = item.session


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_logreport(report):  # sourcery skip: merge-nested-ifs
    """
    Write pytest-fold markers around all failed testcases
    """
    # print(MARKERS["pytest_runtest_logreport_begin"])
    out = yield
    # print(MARKERS["pytest_runtest_logreport_begin"])
    if report.session.config.option.fold:
        if report.when == "setup":
            report.session._store["larry"] = "LARRY THE ICE CREAM MAN"
        if report.when == "call":
            if report.passed:
                pass
                # report.longrepr.chain[0][0].reprentries[0].lines.insert(0, MARKERS["pytest_pass_begin"])
                # report.longrepr.chain[0][0].extraline = MARKERS["pytest_pass_end"]
            if report.failed:
                report.longrepr.chain[0][0].reprentries[0].lines.insert(
                    0, MARKERS["pytest_fold_failure_begin"]
                )
                report.longrepr.chain[0][0].extraline = MARKERS["pytest_fold_failure_end"]
        if report.when == "teardown":
            report.session._store["larry"] = "LARRY THE ICE CREAM MAN"


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    """
    Write console output to a file for use by TUI
    (part 1; used in conjunction with pytest_unconfigure, below)
    """
    pattern = re.compile(r"^=.*in\s\d+.\d+s.*=+")
    if config.option.fold:
        tr = config.pluginmanager.getplugin("terminalreporter")
        if tr is not None:

            try:  # test to see if this is the first tiem hitting this code...which means we have the first line of the terminal output
                config._pyfoldfirsttime
            except AttributeError:
                config._pyfoldfirsttime = True

            config._pyfoldoutputfile = tempfile.TemporaryFile("wb+")
            oldwrite = tr._tw.write

            def tee_write(s, **kwargs):
                if config._pyfoldfirsttime:
                    oldwrite(MARKERS["pytest_fold_firstline"] + "\n")
                    config._pyfoldoutputfile.write((MARKERS["pytest_fold_firstline"] + "\n").encode("utf-8"))
                    config._pyfoldfirsttime = False

                search = re.search(pattern, s)
                if search:  # final line of terminal output
                    oldwrite(MARKERS["pytest_fold_lastline"] + "\n")
                    config._pyfoldoutputfile.write((MARKERS["pytest_fold_lastline"] + "\n").encode("utf-8"))

                oldwrite(s, **kwargs)
                if isinstance(s, str):
                    s = s.encode("utf-8")
                config._pyfoldoutputfile.write(s)

            tr._tw.write = tee_write


def pytest_unconfigure(config: Config) -> None:
    """
    Write console output to a file for use by TUI
    (part 2; used in conjunction with pytest_configure, above)
    """
    if hasattr(config, "_pyfoldoutputfile"):
        # get terminal contents, then write file
        config._pyfoldoutputfile.seek(0)
        sessionlog = config._pyfoldoutputfile.read()
        config._pyfoldoutputfile.close()
        # del config._pyfoldoutputfile
        # Undo our patching in the terminal reporter.
        tr = config.pluginmanager.getplugin("terminalreporter")
        print("")
        # del tr._tw.__dict__["write"]
        # write out to file
        with open(OUTFILE, "wb") as outfile:
            outfile.write(sessionlog)
        run_it()


def run_it():
    """Stub file for possible later use to auto-launch TUI"""
    pass


# @pytest.hookimpl(hookwrapper=True)
# def pytest_collectreport(report):
#     print(MARKERS["pytest_fold_collectreport_begin"])
#     out = yield
#     print(MARKERS["pytest_fold_collectreport_end"])


# @pytest.hookimpl(trylast=True, hookwrapper=True)
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     print(MARKERS["pytest_fold_terminal_summary_begin"])
#     out = yield
#     print(out)
#     print(MARKERS["pytest_fold_terminal_summary_end"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_report_collectionfinish(config):
#     print(MARKERS["pytest_fold_experiment"])
#     out = yield
#     print(MARKERS["pytest_fold_experiment"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_report_teststatus(report, config):
#     print(MARKERS["pytest_fold_experiment"])
#     out = yield
#     print(MARKERS["pytest_fold_experiment"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_collectstart(collector):
#     print(MARKERS["pytest_fold_experiment"])
#     out = yield
#     print(MARKERS["pytest_fold_experiment"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_report_header(config):
#     print(MARKERS["pytest_fold_experiment"])
#     out = yield
#     print(MARKERS["pytest_fold_experiment"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_fixture_setup(fixturedef, request):
#     print(MARKERS["pytest_fold_experiment"])
#     out = yield
#     print(MARKERS["pytest_fold_experiment"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_configure(config):
#     print(MARKERS["pytest_fold_experiment"])
#     out = yield
#     print(MARKERS["pytest_fold_experiment"])
