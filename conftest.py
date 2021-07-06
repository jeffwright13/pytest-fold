import os
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
    print("/tests: setting up:", item)


def pytest_runtest_call(item):
    print("/tests: calling:", item)


def pytest_runtest_teardown(item):
    print("/tests: tearing down:", item)


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
    content = os.linesep.join(
        report.capstdout
        for report in reports
        if report.capstdout and report.nodeid.endswith("test_summary")
    )
    # add custom section that mimics pytest's one
    if content:
        terminalreporter.ensure_newline()
        terminalreporter.section(
            "Captured stdout call",
            sep="-",
            blue=True,
            bold=True,
        )
        terminalreporter.line(content)
