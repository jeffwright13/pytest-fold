import os
import sys
import pytest


pytest_plugins = "pytester"


collect_ignore = [
    "pytest_fold.py",
    "setup.py",
    "pytest_something.py",
    "pytest_capture.py",
    "*.yml",
]


def pytest_configure(config):
    config.addinivalue_line("markers", "cool: this one is for cool tests.")


def pytest_runtest_setup(item):
    print("stdout: setting up:", item)
    sys.stderr.write("stderr: setting up:\n")


def pytest_runtest_call(item):
    print("stdout: calling:", item)
    sys.stderr.write("stderr: calling:\n")


def pytest_runtest_teardown(item):
    print("stdout: tearing down:", item)
    sys.stderr.write("stderr: tearing down:\n")


def pytest_addoption(parser):
    group = parser.getgroup("helloworld")
    group.addoption(
        "--name",
        action="store",
        dest="name",
        default="World",
        help="Default 'name' for hello().",
    )


@pytest.fixture
def hello(request):
    name = request.config.getoption("name")

    def _hello(name=None):
        if not name:
            name = request.config.getoption("name")
        return "Hello, {name}!".format(name=name)

    return _hello


# From: https://stackoverflow.com/questions/64812992/pytest-capture-stdout-of-a-certain-test/64822668#64822668
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # on failures, don't add "Captured stdout call" as pytest does that already
    # otherwise, the section "Captured stdout call" will be added twice
    if exitstatus > 0:
        return
    # get all reports
    reports = terminalreporter.getreports("")
    # combine captured stdout of reports for tests named `<smth>::test_summary`
    content_stdout = os.linesep.join(
        report.capstdout
        for report in reports
        if report.capstdout and report.nodeid.endswith("test_summary")
    )
    # add custom section that mimics pytest's one
    if content_stdout:
        terminalreporter.ensure_newline()
        terminalreporter.section(
            "Captured stdout call",
            sep="-",
            blue=True,
            bold=True,
        )
        terminalreporter.line(content_stdout)

    content_stderr = os.linesep.join(
        report.capstderr
        for report in reports
        if report.capstderr and report.nodeid.endswith("test_summary")
    )
    # add custom section that mimics pytest's one
    if content_stderr:
        terminalreporter.ensure_newline()
        terminalreporter.section(
            "Captured stderr call",
            sep="!",
            red=True,
            bold=True,
        )
        terminalreporter.line(content_stderr)


# Experiment with Ctrl-C
def pytest_keyboard_interrupt(excinfo):
    pass
