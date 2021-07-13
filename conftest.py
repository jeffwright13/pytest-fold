import os
import sys
import pytest
from _pytest.terminal import TerminalReporter


pytest_plugins = "pytester"


collect_ignore = [
    "pytest_fold.py",
    "setup.py",
    "pytest_something.py",
    "pytest_capture.py",
    "*.yml",
]


# https://stackoverflow.com/questions/65526149/pytest-customize-short-test-summary-info-remove-filepath
class MyReporter(TerminalReporter):
    def short_test_summary(self):
        # your own impl goes here, for example:
        self.write_sep("=", "my own short summary info")
        failed = self.stats.get("failed", [])
        for rep in failed:
            self.write_line(f"failed test {rep.nodeid}")


@pytest.mark.trylast
def pytest_configure(config):
    vanilla_reporter = config.pluginmanager.getplugin("terminalreporter")
    my_reporter = MyReporter(config)
    config.pluginmanager.unregister(vanilla_reporter)
    config.pluginmanager.register(my_reporter, "terminalreporter")





# Register pytest-fold option (--fold)
def pytest_addoption(parser):
    group = parser.getgroup("fold")
    group.addoption(
        "--fold", action="store_true", help="fold: fold failed test output section"
    )


@pytest.fixture(autouse=True)
def fold(request):
    return request.config.getoption("--fold")


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_logreport(report):
    yield
    if report.when == "call":
        if report.failed:
            # breakpoint()
            # if fold:
            #     print("Test failed; overridden by fold plugin.", file=sys.stderr)
            print("Test failed; now what?")
            pass

#   --tb=style     traceback print mode (auto/long/short/line/native/no).

# (Pdb) dir(report)
# ['__annotations__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__test__', '__weakref__', '_from_json', '_get_verbose_word', '_to_json', 'caplog', 'capstderr', 'capstdout', 'count_towards_summary', 'duration', 'failed', 'from_item_and_call', 'fspath', 'get_sections', 'head_line', 'keywords', 'location', 'longrepr', 'longreprtext', 'nodeid', 'outcome', 'passed', 'sections', 'skipped', 'toterminal', 'user_properties', 'when']


# @pytest.mark.tryfirst
# def pytest_runtest_logreport(report):
#     """Overwrite report by removing any captured stderr."""
#     # print("PLUGIN SAYS -> report -> {0}".format(report))
#     # print("PLUGIN SAYS -> report.sections -> {0}".format(report.sections))
#     # print("PLUGIN SAYS -> dir(report) -> {0}".format(dir(report)))
#     # print("PLUGIN SAYS -> type(report) -> {0}".format(type(report)))
#     sections = [
#         item
#         for item in report.sections
#         if item[0] not in (
#             "Captured stdout call",
#             "Captured stderr call",
#             "Captured stdout setup",
#             "Captured stderr setup",
#             "Captured stdout teardown",
#             "Captured stderr teardown",
#             "Captured log call",
#         )
#     ]
#     # print("PLUGIN SAYS -> sections -> {0}".format(sections))
#     report.sections = sections


# # Custom marker "cool"
# def pytest_configure(config):
#     config.addinivalue_line("markers", "cool: this one is for cool tests.")

# # Print out info during test setup, call, teardown
# def pytest_runtest_setup(item):
#     print("stdout: setting up:", item)
#     sys.stderr.write("stderr: setting up:\n")

# def pytest_runtest_call(item):
#     print("stdout: calling:", item)
#     sys.stderr.write("stderr: calling:\n")

# def pytest_runtest_teardown(item):
#     print("stdout: tearing down:", item)
#     sys.stderr.write("stderr: tearing down:\n")


# Override https://docs.pytest.org/en/stable/reference.html#pytest.hookspec.pytest_runtest_logreport
# @pytest.hookimpl(trylast=True, hookwrapper=True)
# def pytest_runtest_logreport(report):
#     if report.when == "setup":
#         print("\n")
#     print(f"BEFORE_YIELD - when: {report.when.upper()} | location: {report.location} | outcome: {report.outcome} | fspath: {report.fspath}")
#     yield
#     if report.when == "call":
#         print("\r")
#     print(f"AFTER_YIELD - when: {report.when.upper()} | location: {report.location} | outcome: {report.outcome} | fspath: {report.fspath}")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_logreport(report):
#     outcome = yield
#     rep = outcome.get_result()
#     # breakpoint()
#     # Define when/what to report:
#     # when = setup / call / teardown
#     # .failed / .passed / .skipped
#     if report.when == "teardown":
#         # breakpoint()
#         print(report.longreprtext)
#         print(report.sections)
#         print(report.capstdout)
#         print(report.capstderr)


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#     # breakpoint()

#     # we only look at actual failing test calls, not setup/teardown
#     if rep.when == "call" and rep.failed:
#         mode = "a" if os.path.exists("failures") else "w"
#         with open("failures", mode) as f:
#             # let's also access a fixture for the fun of it
#             if "tmp_path" in item.fixturenames:
#                 extra = " ({})".format(item.funcargs["tmp_path"])
#             else:
#                 extra = ""

#             f.write(rep.nodeid + extra + "\n")


# # helloworld() example in Pytest docs "Testing Plugins" section
# # https://docs.pytest.org/en/6.2.x/writing_plugins.html#testing-plugins
# def pytest_addoption(parser):
#     group = parser.getgroup("helloworld")
#     group.addoption(
#         "--name",
#         action="store",
#         dest="name",
#         default="World",
#         help="Default 'name' for hello().",
#     )


# @pytest.fixture
# def hello(request):
#     name = request.config.getoption("name")

#     def _hello(name=None):
#         if not name:
#             name = request.config.getoption("name")
#         return "Hello, {name}!".format(name=name)

#     return _hello


# def test_hello(testdir):
#     """Make sure that our plugin works."""

#     # create a temporary conftest.py file
#     testdir.makeconftest(
#         """
#         import pytest

#         @pytest.fixture(params=[
#             "Brianna",
#             "Andreas",
#             "Floris",
#         ])
#         def name(request):
#             return request.param
#     """
#     )

#     # create a temporary pytest test file
#     testdir.makepyfile(
#         """
#         def test_hello_default(hello):
#             assert hello() == "Hello World!"

#         def test_hello_name(hello, name):
#             assert hello(name) == "Hello {0}!".format(name)
#     """
#     )

#     # run all tests with pytest
#     result = testdir.runpytest()

#     # check that all 4 tests passed
#     result.assert_outcomes(passed=4)

# # From: https://stackoverflow.com/questions/64812992/pytest-capture-stdout-of-a-certain-test/64822668#64822668
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     # on failures, don't add "Captured stdout call" as pytest does that already
#     # otherwise, the section "Captured stdout call" will be added twice
#     if exitstatus > 0:
#         return
#     # get all reports
#     reports = terminalreporter.getreports("")
#     # combine captured stdout of reports for tests named `<smth>::test_summary`
#     content_stdout = os.linesep.join(
#         report.capstdout
#         for report in reports
#         if report.capstdout and report.nodeid.endswith("test_summary")
#     )
#     # add custom section that mimics pytest's one
#     if content_stdout:
#         terminalreporter.ensure_newline()
#         terminalreporter.section(
#             "Captured stdout call",
#             sep="-",
#             blue=True,
#             bold=True,
#         )
#         terminalreporter.line(content_stdout)

#     content_stderr = os.linesep.join(
#         report.capstderr
#         for report in reports
#         if report.capstderr and report.nodeid.endswith("test_summary")
#     )
#     # add custom section that mimics pytest's one
#     if content_stderr:
#         terminalreporter.ensure_newline()
#         terminalreporter.section(
#             "Captured stderr call",
#             sep="!",
#             red=True,
#             bold=True,
#         )
#         terminalreporter.line(content_stderr)

# # Experiment with Ctrl-C/Del
# def pytest_keyboard_interrupt(excinfo):
#     breakpoint()
#     pass


# def pytest_addoption(parser):
#     parser.addoption('--silent', action='store_true', default=False)


# def pytest_report_teststatus(report):
#     category, short, verbose = '', '', ''
#     if not pytest.config.getoption('--silent'):
#         return None

#     if hasattr(report, 'wasxfail'):
#         if report.skipped:
#             category = 'xfailed'
#         elif report.passed:
#             category = 'xpassed'
#         return (category, short, verbose)
#     elif report.when in ('setup', 'teardown'):
#         if report.failed:
#             category = 'error'
#         elif report.skipped:
#             category = 'skipped'
#         return (category, short, verbose)
#     category = report.outcome
#     return (category, short, verbose)

# Allow Pytest debug in Sublime
# See https://stackoverflow.com/questions/62419998/how-can-i-get-pytest-to-not-catch-exceptions/62563106#62563106
if os.getenv("_PYTEST_RAISE", "0") != "0":

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call):
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo):
        raise excinfo.value
