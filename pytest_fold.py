# import tempfile
# import pytest
# from _pytest.config import Config
# from pathlib import Path

# # MARKER1 = "==>MARKER1<=="
# # MARKER2 = "==>MARKER2<=="
# OUTFILE = Path.cwd / "console_output.fold"


# # collect_ignore = [
# #     "pytest_fold.py",
# #     "setup.py",
# #     "pytest_something.py",
# #     "pytest_capture.py",
# #     "*.yml",
# # ]


# # # Register pytest-fold option (--fold)
# # def pytest_addoption(parser):
# #     group = parser.getgroup("fold")
# #     group.addoption(
# #         "--fold", action="store_true", help="fold: fold failed test output sections"
# #     )


# # @pytest.fixture(autouse=True)
# # def fold(request):
# #     return request.config.getoption("--fold")


# # # attach session info to report for later use in pytest_runtest_logreport
# # # https://stackoverflow.com/questions/54717786/access-pytest-session-or-arguments-in-pytest-runtest-logreport
# # @pytest.hookimpl(hookwrapper=True)
# # def pytest_runtest_makereport(item, call):
# #     out = yield
# #     report = out.get_result()
# #     report.session = item.session


# # # Mark all failed tests' output with begin and end markers
# # @pytest.hookimpl(trylast=True, hookwrapper=True)
# # def pytest_runtest_logreport(report):
# #     yield
# #     if report.when == "call" and report.failed and report.session.config.option.fold:
# #         report.longrepr.chain[0][0].reprentries[0].lines.insert(0, MARKER1)
# #         report.longrepr.chain[0][0].extraline = MARKER2


# # Write console output to a file for use by TUI. Stolen from Pytest's pastebin.py
# # Tip of the hat to pytest_session2file:
# # (https://github.com/BuhtigithuB/pytest_session2file/blob/master/pytest_session2file/pytest_session2file.py)
# @pytest.hookimpl(trylast=True)
# def pytest_configure(config: Config) -> None:
#     if config.option.pastebin == "all":
#         tr = config.pluginmanager.getplugin("terminalreporter")
#         # If no terminal reporter plugin is present, nothing we can do here;
#         # this can happen when this function executes in a worker node
#         # when using pytest-xdist, for example.
#         if tr is not None:
#             # pastebin file will be UTF-8 encoded binary file.
#             config.stash[OUTFILE] = OUTFILE
#             oldwrite = tr._tw.write

#             def tee_write(s, **kwargs):
#                 oldwrite(s, **kwargs)
#                 if isinstance(s, str):
#                     s = s.encode("utf-8")
#                 config.stash[OUTFILE].write(s)

#             tr._tw.write = tee_write


# def pytest_unconfigure(config: Config) -> None:
#     if OUTFILE in config.stash:
#         # get terminal contents and delete file
#         config.stash[OUTFILE].seek(0)
#         sessionlog = config.stash[OUTFILE].read()
#         config.stash[OUTFILE].close()
#         del config.stash[OUTFILE]
#         # Undo our patching in the terminal reporter.
#         tr = config.pluginmanager.getplugin("terminalreporter")
#         del tr._tw.__dict__["write"]
#         # write out to file
#         with open(OUTFILE, 'w') as outfile:
#             outfile.writelines(sessionlog)


# # plugin = pytest.config.pluginmanager.get_plugin("pytest_session2file")

# # def pytest_addoption(parser):
# #     group = parser.getgroup("fold")
# #     group.addoption(
# #         "--fold",
# #         action="store",
# #         dest="fold",
# #         default="2021",
# #         help="Fold test results in console",
# #     )

# #     parser.addini("FOLD", "pytest.ini setting for pytest_fold")


# # @pytest.fixture
# # def fold(request):
# #     return request.config.option.fold
