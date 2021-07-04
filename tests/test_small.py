import pytest

@pytest.mark.cool
def test_1():
    assert 1 == 1


def test_2():
    assert 0 == 0


def test_3():
    assert -1 == -1


def test_4():
    assert 0 == 1
