import pytest


pytest_plugins = "pytester"


collect_ignore = [
    "pytest_fold.py",
    "setup.py",
    "pytest_something.py",
    "pytest_capture.py",
    "*.yml",
]


def pytest_configure(config):
    config.addinivalue_line("markers", "cool: this one is for cool tests.")


def pytest_runtest_setup(item):
    print("/tests: setting up:", item)


def pytest_runtest_call(item):
    print("/tests: calling:", item)


def pytest_runtest_teardown(item):
    print("/tests: tearing down:", item)


def pytest_addoption(parser):
    group = parser.getgroup("helloworld")
    group.addoption(
        "--name",
        action="store",
        dest="name",
        default="World",
        help="Default 'name' for hello().",
    )


@pytest.fixture
def hello(request):
    name = request.config.getoption("name")

    def _hello(name=None):
        if not name:
            name = request.config.getoption("name")
        return "Hello, {name}!".format(name=name)

    return _hello
