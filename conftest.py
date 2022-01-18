import pytest


collect_ignore = [
    "pytest_fold.py",
    "setup.py",
    "pytest_something.py",
    "pytest_capture.py",
    "*.yml",
]


# Register pytest-fold option (--fold)
def pytest_addoption(parser):
    group = parser.getgroup("fold")
    group.addoption(
        "--fold", action="store_true", help="fold: fold failed test output sections"
    )


@pytest.fixture(autouse=True)
def fold(request):
    return request.config.getoption("--fold")


# attach session info to report for later use in pytest_runtest_logreport
# https://stackoverflow.com/questions/54717786/access-pytest-session-or-arguments-in-pytest-runtest-logreport
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    out = yield
    report = out.get_result()
    report.session = item.session


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_logreport(report):
    yield
    if (
        report.when == "call"
        and report.failed
        and report.session.config.option.fold
    ):
        report.longrepr.chain[0][0].reprentries[0].lines.insert(0, "===MARKER1===")
        report.longrepr.chain[0][0].extraline = "===MARKER2==="
