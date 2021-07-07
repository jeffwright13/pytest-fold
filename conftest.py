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


'''
# Custom marker "cool"
def pytest_configure(config):
    config.addinivalue_line("markers", "cool: this one is for cool tests.")

# Print out info during test setup, call, teardown
def pytest_runtest_setup(item):
    print("stdout: setting up:", item)
    sys.stderr.write("stderr: setting up:\n")

def pytest_runtest_call(item):
    print("stdout: calling:", item)
    sys.stderr.write("stderr: calling:\n")

def pytest_runtest_teardown(item):
    print("stdout: tearing down:", item)
    sys.stderr.write("stderr: tearing down:\n")
'''

# Override https://docs.pytest.org/en/stable/reference.html#pytest.hookspec.pytest_runtest_logreport
@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_logreport(report):
    if report.when == "setup":
        print("\n")
    print(f"BEFORE_YIELD - when: {report.when.upper()} | location: {report.location} | outcome: {report.outcome}")
    yield
    if report.when == "call":
        print("\r")
    print(f"AFTER_YIELD - when: {report.when.upper()} | location: {report.location} | outcome: {report.outcome}")

'''
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_logreport(report):
    outcome = yield
    rep = outcome.get_result()
    # breakpoint()
    # Define when/what to report:
    # when = setup / call / teardown
    # .failed / .passed / .skipped
    if report.when == "teardown":
        # breakpoint()
        print(report.longreprtext)
        print(report.sections)
        print(report.capstdout)
        print(report.capstderr)
'''

'''
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # breakpoint()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmp_path" in item.fixturenames:
                extra = " ({})".format(item.funcargs["tmp_path"])
            else:
                extra = ""

            f.write(rep.nodeid + extra + "\n")
'''




# helloworld() example in Pytest docs "Testing Plugins" section
# https://docs.pytest.org/en/6.2.x/writing_plugins.html#testing-plugins
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


def test_hello(testdir):
    """Make sure that our plugin works."""

    # create a temporary conftest.py file
    testdir.makeconftest(
        """
        import pytest

        @pytest.fixture(params=[
            "Brianna",
            "Andreas",
            "Floris",
        ])
        def name(request):
            return request.param
    """
    )

    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_hello_default(hello):
            assert hello() == "Hello World!"

        def test_hello_name(hello, name):
            assert hello(name) == "Hello {0}!".format(name)
    """
    )

    # run all tests with pytest
    result = testdir.runpytest()

    # check that all 4 tests passed
    result.assert_outcomes(passed=4)

'''
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
'''

# Experiment with Ctrl-C/Del
def pytest_keyboard_interrupt(excinfo):
    breakpoint()
    pass
