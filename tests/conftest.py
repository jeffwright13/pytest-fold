pytest_plugins = 'pytester'

def pytest_runtest_setup(item):
    print("setting up:", item)

def pytest_runtest_call(item):
    print("calling:", item)

def pytest_runtest_collect(item):
    print("collecting:", item)

def pytest_runtest_teardown(item):
    print("tearing down:", item)

