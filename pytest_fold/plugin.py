import pickle

from _pytest.config import Config
from _pytest.reports import TestReport
from pytest_fold.tuit_new import main as tui
from pytest_fold.utils import REPORTFILE

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
        default="asciimatics",
        help="specify user interface ('asciimatics' 'a' | 'textual' 't')",
        choices=["asciimatics", "a", "textual", "t"],
    )


def pytest_report_teststatus(report: TestReport, config: Config):
    """Construct list(s) of individial test report/report-info instances"""
    reports.append(report)


def pytest_unconfigure(config: Config):
    """
    Write test reulst info to a file for use by TUI
    """
    with open(REPORTFILE, "wb") as report_file:
        pickle.dump(reports, report_file)

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
