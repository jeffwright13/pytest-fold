import sys
import time
import logging
import pytest
from pytest_fold import __version__

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.propagate = True
# stdout_handler = logging.StreamHandler(sys.stdout)
# logger.addHandler(stdout_handler)

# def test_version():
#     assert __version__ == "0.1.0"


# def test_which_fails_1():
#     assert 0


# def test_which_passes_1():
#     assert 1 == 1


# def test_which_fails_2():
#     assert 0


# def test_which_passes_2():
#     assert 1 == 1


# def test_which_fails_3():
#     assert 0


# def test_which_passes_3():
#     assert 1 == 1


def test_fail_capturing(capsys):
    print("\nFAIL this stdout is captured")
    sys.stderr.write("FAIL this stderr is captured\n")
    logger.warning("FAIL this log is captured")
    with capsys.disabled():
        print("FAIL stdout not captured, going directly to sys.stdout")
        sys.stderr.write("FAIL stderr not captured, going directly to sys.stderr\n")
        logger.warning("FAIL is this log captured?")
    print("FAIL this stdout is also captured")
    sys.stderr.write("FAIL this stderr is also captured\n")
    logger.warning("FAIL this log is also captured")
    assert False

def test_pass_capturing(capsys):
    print("\nPASS this stdout is captured")
    sys.stderr.write("PASS this stderr is captured\n")
    logger.warning("PASS this log is captured")
    with capsys.disabled():
        print("PASS stdout not captured, going directly to sys.stdout")
        sys.stderr.write("PASS stderr not captured, going directly to sys.stderr\n")
        logger.warning("is this log captured?")
    print("PASS this stdout is also captured")
    sys.stderr.write("PASS this stderr is also captured\n")
    logger.warning("PASS this log is also captured")
    assert True

# def test_which_fails_and_has_stdout_1(capsys):
#     print("this test fails")
#     assert 0 == 1


# def test_which_pauses_and_fails_and_has_stdout_1(capsys):
#     print("this test pauses, then passses")
#     time.sleep(2)
#     assert 0 == -11


# def test_which_passes_and_has_stdout_2(capsys):
#     print("this test passes")  # stdout is consumed by pytest
#     assert "a" == "a"


# def test_summary():
#     assert "a" == "a"


# def test_hello(hello):
#     assert "hello" == "hello"

# ### Following few tests takn from Okken's book
# @pytest.fixture()
# def sample_test(pytester):
#     pytester.makepyfile(
#         """
#         def test_pass():
#             assert 1 == 1
#             def test_fail():
#             assert 1 == 2
#         """
#     )
#     return pytester


# def test_with_fold(sample_test):
#     result = sample_test.runpytest("--fold")
#     result.stdout.fnmatch_lines(
#         [
#             "*",
#         ]
#     )
#     assert result.ret == 1


# def test_with_fold_verbose(sample_test):
#     result = sample_test.runpytest("-v", "--fold")
#     result.stdout.fnmatch_lines(
#         [
#             "▶",
#         ]
#     )
#     assert result.ret == 1


# def test_no_fold_verbose(sample_test):
#     result = sample_test.runpytest("-v")
#     result.stdout.fnmatch_lines(["*"])
#     assert result.ret == 1


# ### <END> Okken's stuff
# '''
# '''
# ### Following is all from cookie-cutter;
# ### needs refactoring for this plugin
# def test_bar_fixture(pytester):
#     """Make sure that pytest accepts our fixture."""

#     # create a temporary pytest test module
#     pytester.makepyfile(
#         """
#         def test_sth(bar):
#             assert bar == "europython2015"
#     """
#     )

#     # run pytest with the following cmd args
#     result = pytester.runpytest("--foo=europython2015", "-v")

#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines(
#         [
#             "*::test_sth PASSED*",
#         ]
#     )

#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0


# def test_help_message(pytester):
#     result = pytester.runpytest(
#         "--help",
#     )
#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines(
#         [
#             "fold:",
#             '*--foo=DEST_FOO*Set the value for the fixture "bar".',
#         ]
#     )


# def test_hello_ini_setting(pytester):
#     pytester.makeini(
#         """
#         [pytest]
#         FOLD = world
#     """
#     )

#     pytester.makepyfile(
#         """
#         import pytest

#         @pytest.fixture
#         def hello(request):
#             return request.config.getini('HELLO')

#         def test_hello_world(hello):
#             assert hello == 'world'
#     """
#     )

#     result = pytester.runpytest("-v")

#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines(
#         [
#             "*::test_hello_world PASSED*",
#         ]
#     )

#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0
