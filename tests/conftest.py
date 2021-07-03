import pytest

pytest_plugins = "pytester"


def pytest_addoption(parser):
    group = parser.getgroup("loser")
    group.addoption("--loser", action="store_true", help="loser: ya basic")


def pytest_report_header(config):
    """Override. Thank tester."""
    if config.getoption("loser"):
        return "Thanks for your service, Capt. Tester!"


def pytest_report_teststatus(config, report):
    if report.when == "call":
        if report.failed and config.getoption("--loser"):
            return (report.outcome, "L", "LOSER")
