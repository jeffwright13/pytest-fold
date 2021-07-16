write_fspath_result




======================= FAILURES ========================
_______________________ test_fail _______________________

    def test_fail():
        time.sleep(3)
>       assert False
E       assert False

tests/test_pytest_fold.py:71: AssertionError

=============== 1 failed, 1 passed in 6.25s =============



(Pdb) report
<TestReport 'tests/test_pytest_fold.py::test_fail' when='call' outcome='failed'>
(Pdb) report.longrepr
ExceptionChainRepr(chain=[(ReprTraceback(reprentries=[ReprEntry(lines=['    def test_fail():', '        time.sleep(3)', '>       assert False', 'E       assert False'], reprfuncargs=ReprFuncArgs(args=[]), reprlocals=None, reprfileloc=ReprFileLocation(path='tests/test_pytest_fold.py', lineno=71, message='AssertionError'), style='long')], extraline=None, style='long'), ReprFileLocation(path='/Users/jeff/coding/pytest-fold/tests/test_pytest_fold.py', lineno=71, message='assert False'), None)])

report.longrepr:
----------------
ExceptionChainRepr(
    chain=[
        (
            ReprTraceback(
                reprentries=[
                    ReprEntry(
                        lines=[
                            "    def test_fail():",
                            "        time.sleep(3)",
                            ">       assert False",
                            "E       assert False",
                        ],
                        reprfuncargs=ReprFuncArgs(args=[]),
                        reprlocals=None,
                        reprfileloc=ReprFileLocation(
                            path="tests/test_pytest_fold.py",
                            lineno=71,
                            message="AssertionError",
                        ),
                        style="long",
                    )
                ],
                extraline=None,
                style="long",
            ),
            ReprFileLocation(
                path="/Users/jeff/coding/pytest-fold/tests/test_pytest_fold.py",
                lineno=71,
                message="assert False",
            ),
            None,
        )
    ]
)

report.longrepr.chain:
---------------------
[
    (
        ReprTraceback(
            reprentries=[
                ReprEntry(
                    lines=[
                        "    def test_fail():",
                        "        time.sleep(3)",
                        ">       assert False",
                        "E       assert False",
                    ],
                    reprfuncargs=ReprFuncArgs(args=[]),
                    reprlocals=None,
                    reprfileloc=ReprFileLocation(
                        path="tests/test_pytest_fold.py",
                        lineno=71,
                        message="AssertionError",
                    ),
                    style="long",
                )
            ],
            extraline=None,
            style="long",
        ),
        ReprFileLocation(
            path="/Users/jeff/coding/pytest-fold/tests/test_pytest_fold.py",
            lineno=71,
            message="assert False",
        ),
        None,
    )
]


list(report.longrepr.chain[0]).insert(0, "MARKER")





@attr.s(eq=False)
class ExceptionChainRepr(ExceptionRepr):
    chain = attr.ib(
        type=Sequence[
            Tuple["ReprTraceback", Optional["ReprFileLocation"], Optional[str]]
        ]
    )



