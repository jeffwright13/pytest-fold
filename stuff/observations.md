- Running "pytest /test/test_something.py" clearly ilustrates the problem we are trying to solve here: waaaaay too much output on the console.
- Regardless of console width at runtime, output seems the same, so presumably Pytest lets the console take care of formatting its output to the particular screen dimensions / settings. See files /stuff/pytest_output*.
✔︎ https://en.wikipedia.org/wiki/Code_folding
☐ I cannot figure out what the hell the travis_folding code is doing (appears o be nothing in my experiements), so I am putting it aside for now.
✔︎ To read for testing plugins: https://docs.pytest.org/en/6.2.x/writing_plugins.html
✔︎ Testing plugins: https://docs.pytest.org/en/6.2.x/writing_plugins.html#testing-plugins
- 'testdir' fixture now replaced by 'pytester' (as of 6.2)
- ^^^ https://github.com/pytest-dev/cookiecutter-pytest-plugin/issues/51 ^^^
☐ https://stackoverflow.com/questions/53637733/output-ascii-art-to-console-on-succesfull-pytest-run
- UTF-8 rightwards triangle: ▶ (https://codepoints.net/U+25B6)
- UTF-8 downwards triangle: ▼ (https://codepoints.net/U+25BC

- https://github.com/pytest-dev/pytest/blob/main/src/_pytest/terminal.py
- https://stackoverflow.com/questions/64812992/pytest-capture-stdout-of-a-certain-test/64822668#64822668
- https://stackoverflow.com/questions/46865816/read-py-tests-output-as-object/46867867#46867867

- Put the following text into conftest.py, then run some passing and some failing tests. Interesting observation: pytest *only* marks a specific test's TestReport.outcom attribute as "failed" during the call() phase. During setup() and teardown(), a failing test still has TestReport.outcome = "passed".
    @pytest.hookimpl(trylast=True, hookwrapper=True)
    def pytest_runtest_logreport(report):
        if report.when == "setup":
            print("\n")
        print(f"BEFORE_YIELD - when: {report.when.upper()} | location: {report.location} | outcome: {report.outcome}")
        yield
        if report.when == "call":
            print("\r")
        print(f"AFTER_YIELD - when: {report.when.upper()} | location: {report.location} | outcome: {report.outcome}")

- pytest-sugar psuedo-code for pytest_runtest_logreport:

    get (category, letter, word) from report   # e.g. passed, P, PASS
    append category to reports list
    if test outcome is failed:
        print newline
        call print_failure function
    if current test is in teardown phase:
        add 1 to 'number of tests taken' metric
        call insert_progress function
    if current test is in call phase, or if current test is marked 'skip':
        print/update some initial crap
        if test outcome is failed:
            print/update some other crap
        else:
            print/update some other, but different crap
    if not letter or word:
        return
    if verbose:
        do some verbose stuff on the terminal


- pytest-hidecaptured (https://pypi.org/project/pytest-hidecaptured/) has some interesting code, esp its main method (https://github.com/codeghar/pytest-hidecaptured/blob/master/pytest_hidecaptured.py), which squelches stdlog/stderr/stdout printing to console:

    @pytest.mark.tryfirst
    def pytest_runtest_logreport(report):
        """Overwrite report by removing any captured stderr."""
        sections = [
            item
            for item in report.sections
            if item[0] not in (
                "Captured stdout call",
                "Captured stderr call",
                "Captured stdout setup",
                "Captured stderr setup",
                "Captured stdout teardown",
                "Captured stderr teardown",
                "Captured log call",
            )
        ]
        report.sections = sections

- pytest-capturelog may be of interest: http://pypi.python.org/pypi/pytest-capturelog/
