import sys
import time
import pytest


def test_capsys_output(capsys):
    time.sleep(1)
    print("hello")
    time.sleep(1)
    sys.stderr.write("world!\n")
    captured = capsys.readouterr()
    # breakpoint()
    assert captured.out == "hello\n"
    assert captured.err == "world!\n"

    time.sleep(1)
    print("next")
    captured = capsys.readouterr()
    time.sleep(1)
    # breakpoint()
    assert captured.out == "next\n"
    assert captured.err == ""


def test_3(capsys):
    # breakpoint()
    assert -1 == -1


def test_4(capsys):
    assert 0 == 1
    breakpoint()
