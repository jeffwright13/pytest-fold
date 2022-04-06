import pytest
import logging
import sys

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
logger.propagate = True
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logging.getLogger('faker').setLevel(logging.ERROR)

@pytest.fixture
def error_fixture():
    assert 0

def test_i_ok():
    print("ok")


def test_ii_fail():
    assert 0


def test_iii_error(error_fixture):
    pass


def test_iv_skip():
    pytest.skip("skipping this test")


def test_v_xfail():
    pytest.xfail("xfailing this test")


@pytest.mark.xfail(reason="always xfail")
def test_vi_xpass():
    pass
