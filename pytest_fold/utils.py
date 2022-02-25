import pickle
from dataclasses import dataclass
from pathlib import Path
from _pytest.reports import TestReport

REPORTFILE = Path.cwd() / "pytest_report.bin"


@dataclass
class TestInfo:
    title: str = ""
    tag: str = ""
    outcome: str = ""
    caplog: str = ""
    capstderr: str = ""
    capstdout: str = ""
    text: str = ""


class Results:
    def __init__(self):
        self._reports = self._unpickle()
        self._test_info = self._parse_reports()
        self.sections = self._sectionalize()

    def _unpickle(self):
        with open(REPORTFILE, "rb") as rfile:
            return pickle.load(rfile)

    def _parse_reports(self):
        test_infos = []
        for report in self._reports:
            test_info = TestInfo()
            if (
                # passed test
                report.when == "call"
                and report.outcome == "passed"
                #  failed test
                or report.when == "setup"
                and report.outcome == "failed"
                # error
                or report.when == "call"
                and report.outcome == "failed"
                # marked skip
                or report.when == "setup"
                and report.outcome == "skipped"
                # marked xfail
                or report.when == "call"
                and report.outcome == "skipped"
            ):
                test_info.outcome = report.outcome
                test_info.caplog = report.caplog
                test_info.capstderr = report.capstderr
                test_info.capstdout = report.capstdout
                test_info.title = report.head_line
                test_info.text = report.longreprtext if report.outcome == "failed" else None
                test_infos.append(test_info)
        return test_infos

    def _sectionalize(self):
        return list({item.title:item for item in self._test_info}.values())

    def get_results(self) -> list:
        return self.sections


"""
if report.when == "call" and report.outcome == "skipped":
    report_info.append(TestReportInfo(report, report.outcome, report.caplog, report.capstderr, report.capstdout, report.head_line))
if report.when == "call":
    t = TestReportInfo(report, report.outcome, report.caplog, report.capstderr, report.capstdout, report.head_line)
    report_info.append(t)
    if report.outcome == "passed":
        report_info.append(t)
        return
"""
