import pytest

collect_ignore = [
    "pytest_fold.py",
    "setup.py",
    "pytest_something.py",
    "pytest_capture.py",
    "*.yml",
]


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_logreport(report):
    yield
    if report.when == "call":
        if report.failed:
            # breakpoint()
            # if fold:
            #     print("Test failed; overridden by fold plugin.", file=sys.stderr)
            report.longrepr.chain[0][0].reprentries[0].lines.insert(0, "===MARKER1===")
            # report.longrepr.chain[0][0].reprentries[0].reprfileloc.message += "===MARKER2==="
            report.longrepr.chain[0][0].extraline = "===MARKER2==="
            pass
