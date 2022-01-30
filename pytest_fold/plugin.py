import pytest
import tempfile

from pathlib import Path
from _pytest.config import Config

OUTFILE = Path.cwd() / "console_output.fold"
MARKERS = {
    "pytest_fold_experiment": "~@~@~@ EXPERIMENT @~@~@~",
    "pytest_fold_SESSIONSTART_begin": "==>PYTEST_FOLD_MARKER_SESSIONSTART_BEGIN<==",
    "pytest_fold_SESSIONSTART_end": "==>PYTEST_FOLD_MARKER_SESSIONSTART_END<==",
    "pytest_fold_SESSIONFINISH_begin": "==>PYTEST_FOLD_MARKER_SESSIONFINISH_BEGIN<==",
    "pytest_fold_SESSIONFINISH_end": "==>PYTEST_FOLD_MARKER_SESSIONFINISH_END<==",
    "pytest_fold_runtest_logreport_begin": "==>PYTEST_FOLD_MARKER_SESSION_RUNTEST_LOGREPORT_BEGIN<==",
    "pytest_fold_runtest_logreport_end": "==>PYTEST_FOLD_MARKER_SESSION_RUNTEST_LOGREPORT_END<==",
    "pytest_fold_terminal_summary_begin": "==>PYTEST_FOLD_MARKER_TERMINAL_SUMMARY_BEGIN<==",
    "pytest_fold_terminal_summary_end": "==>PYTEST_FOLD_MARKER_TERMINAL_SUMMARY_END<==",
    "pytest_fold_pass_begin": "==>PYTEST_FOLD_MARKER_PASS_BEGIN<==",
    "pytest_fold_pass_end": "==>PYTEST_FOLD_MARKER_PASS_END<==",
    "pytest_fold_failure_begin": "==>PYTEST_FOLD_MARKER_FAILURE_BEGIN<==",
    "pytest_fold_failure_end": "==>PYTEST_FOLD_MARKER_FAILURE_END<==",
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

@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_sessionstart(session):
    """
    Write pyfold section-begin marker before session starts
    """
    print(MARKERS["pytest_fold_SESSIONSTART_begin"])
    out = yield
    print(MARKERS["pytest_fold_SESSIONSTART_end"])


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session):
    """
    Write pyfold section-end marker after session finishes
    """
    print("\n")
    print(MARKERS["pytest_fold_SESSIONFINISH_begin"])
    out = yield
    print(MARKERS["pytest_fold_SESSIONFINISH_end"])


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
    if report.session.config.option.fold and report.when == "call":
        # if report.passed:
        #     report.longrepr.chain[0][0].reprentries[0].lines.insert(0, MARKERS["pytest_pass_begin"])
        #     report.longrepr.chain[0][0].extraline = MARKERS["pytest_pass_end"]
        if report.failed:
            report.longrepr.chain[0][0].reprentries[0].lines.insert(
                0, MARKERS["pytest_fold_failure_begin"]
            )
            report.longrepr.chain[0][0].extraline = MARKERS["pytest_fold_failure_end"]


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    """
    Write console output to a file for use by TUI
    (part 1; used in conjunction with pytest_unconfigure, below)
    """
    if config.option.fold:
        tr = config.pluginmanager.getplugin("terminalreporter")
        if tr is not None:
            config._pyfoldoutputfile = tempfile.TemporaryFile("wb+")
            oldwrite = tr._tw.write

            def tee_write(s, **kwargs):
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
#     out = yield
#     print("")


# @pytest.hookimpl(trylast=True, hookwrapper=True)
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     print(MARKERS["pytest_fold_terminal_summary_begin"])
#     out = yield
#     print(out)
#     print(MARKERS["pytest_fold_terminal_summary_end"])


# @pytest.hookimpl(hookwrapper=True)
# def pytest_report_collectionfinish(config):
#     print(MARKERS["pytest_experiment")
#     out = yield
#     print(MARKERS["pytest_experiment")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_report_teststatus(report, config):
#     print(MARKERS["pytest_experiment")
#     out = yield
#     print(MARKERS["pytest_experiment")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_collectstart(collector):
#     print(MARKERS["pytest_experiment")
#     out = yield
#     print(MARKERS["pytest_experiment")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_report_header(config):
#     print(MARKERS["pytest_experiment")
#     out = yield
#     print(MARKERS["pytest_experiment")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_fixture_setup(fixturedef, request):
#     print(MARKERS["pytest_experiment")
#     out = yield
#     print(MARKERS["pytest_experiment")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_configure(config):
#     print(MARKERS["pytest_experiment")
#     out = yield
#     print(MARKERS["pytest_experiment")
