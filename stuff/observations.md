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
