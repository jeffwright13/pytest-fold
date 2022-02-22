import sys
import time
import logging
import faker
import pytest
from random import sample
# from . import __version__

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
logger.propagate = True
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

# def test_version():
#     assert __version__ == "0.1.0"


def test_which_passes_and_has_lots_of_logging_output():
    text = faker.Faker().text(2000)
    logger.critical(text)
    logger.error(text)
    logger.warning(text)
    logger.info(text)
    logger.debug(text)
    assert 1 == 1

def test_which_fails_and_has_lots_of_logging_output():
    text = faker.Faker().text(3000)
    logger.critical(text)
    logger.error(text)
    logger.warning(text)
    logger.info(text)
    logger.debug(text)
    assert 0 == 1


def test_which_fails_1():
    assert 0


def test_which_passes_1():
    assert 1 == 1


# def test_which_fails_2():
#     assert 0


# def test_which_passes_2():
#     assert 1 == 1


@pytest.mark.skip
def test_which_is_marked_SKIP():
    assert 1


@pytest.mark.xfail
def test_flaky_XPASS():
    assert 1


@pytest.mark.xfail
def test_which_is_marked_XFAIL():
    assert 0


# def test_which_passes_3():
#     assert 1 == 1


# Method and its test that causes warnings
def api_v1():
    import warnings
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1
def test_which_causes_a_warning():
    assert api_v1() == 1


# # These tests are helpful in showing how pytest deals with various types
# # of output (stdout, stderr, log)
def test_lorem(capsys):
    lorem = """"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?

    At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."""
    print(lorem)
    assert False

def test_fail_capturing(capsys):
    print("FAIL this stdout is captured")
    print("FAIL this stderr is captured", file=sys.stderr)
    logger.warning("FAIL this log is captured")
    with capsys.disabled():
        print("FAIL stdout not captured, going directly to sys.stdout")
        print("FAIL stderr not captured, going directly to sys.stderr", file=sys.stderr)
        logger.warning("FAIL is this log captured?")
    print("FAIL this stdout is also captured")
    print("FAIL this stderr is also captured", file=sys.stderr)
    logger.warning("FAIL this log is also captured")
    assert False

def test_pass_capturing(capsys):
    print("\nPASS this stdout is captured")
    print("PASS this stderr is captured", file=sys.stderr)
    logger.warning("PASS this log is captured")
    with capsys.disabled():
        print("PASS stdout not captured, going directly to sys.stdout")
        print("PASS stderr not captured, going directly to sys.stderr", file=sys.stderr)
        logger.warning("is this log captured?")
    print("PASS this stdout is also captured")
    print("PASS this stderr is also captured", file=sys.stderr)
    logger.warning("PASS this log is also captured")
    assert True


# def test_fail_1():
#     a = 0
#     time.sleep(0.05)
#     assert False


# def test_pass_1():
#     a = 0
#     time.sleep(0.05)
#     assert True


# def test_fail_2():
#     a = 0
#     time.sleep(0.05)
#     assert False


# def test_pass_2():
#     a = 0
#     time.sleep(0.05)
#     assert True


# def test_fail_3():
#     a = 0
#     time.sleep(0.05)
#     assert False


# def test_pass_3():
#     a = 0
#     time.sleep(0.05)
#     assert True


def test_which_fails_and_has_stdout(capsys):
    print("this test fails")
    assert 0 == 1


# def test_which_pauses_and_fails_and_has_stdout_1(capsys):
#     print("this test pauses, then fails")
#     # time.sleep(2)
#     assert 0 == -11


def test_which_passes_and_has_stdout(capsys):
    print("this test passes")  # stdout is consumed by pytest
    assert "a" == "a"


# def test_summary():
#     assert "a" == "a"

# This test can intentionally cause an error - useful for testing output of
# folding - if the fixture is commented out, the test throws an error at setup.
# @pytest.fixture()
# def fixture_for_fun():
#     pass

def test_which_causes_error_pass(fixture_for_fun):
    assert 1

def test_which_causes_error_fail(fixture_for_fun):
    assert 0


# def test_hello(hello):
#     assert "hello" == "hello"

### Following few tests takn from Okken's book
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
