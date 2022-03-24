import re
import pickle
from dataclasses import dataclass
from pathlib import Path
from strip_ansi import strip_ansi

REPORTFILE = Path.cwd() / "report_objects.bin"
MARKEDTERMINALOUTPUTFILE = Path.cwd() / "marked_output.bin"
UNMARKEDTERMINALOUTPUTFILE = Path.cwd() / "unmarked_output.bin"

test_session_starts_matcher = re.compile(r"^==.*\stest session starts\s==+")
errors_section_matcher = re.compile(r"^==.*\sERRORS\s==+")
failures_section_matcher = re.compile(r"^==.*\sFAILURES\s==+")
warnings_summary_matcher = re.compile(r"^==.*\swarnings summary\s.*==+")
passes_section_matcher = re.compile(r"^==.*\sPASSES\s==+")
short_test_summary_matcher = re.compile(r"^==.*\sshort test summary info\s.*==+")
lastline_matcher = re.compile(r"^==.*in\s\d+.\d+s.*==+")

section_name_matcher = re.compile(r"~~>PYTEST_FOLD_(\w+)")
test_title_matcher = re.compile(r"__.*\s(.*)\s__+")

test_outcome_matcher = re.compile(r".*::(.*)\s(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s.*\s\[\s.*\]")

MARKERS = {
    "pytest_fold_test_session_starts": "~~>PYTEST_FOLD_TEST_SESSION_STARTS<~~",
    "pytest_fold_errors_section": "~~>PYTEST_FOLD_ERRORS_SECTION<~~",
    "pytest_fold_passes_section": "~~>PYTEST_FOLD_PASSES_SECTION<~~",
    "pytest_fold_failures_section": "~~>PYTEST_FOLD_FAILURES_SECTION<~~",
    "pytest_fold_warnings_summary": "~~>PYTEST_FOLD_WARNINGS_SUMMARY<~~",
    "pytest_fold_short_test_summary": "~~>PYTEST_FOLD_SHORT_TEST_SUMMARY<~~",
    "pytest_fold_last_line": "~~>PYTEST_FOLD_LAST_LINE<~~",
}

SECTIONS = {
    "TEST_SESSION_STARTS": "Session Start",
    "ERRORS_SECTION": "Errors",
    "PASSES_SECTION": "Passes",
    "FAILURES_SECTION": "Failures",
    "WARNINGS_SUMMARY": "Warnings",
    "SHORT_TEST_SUMMARY": "Summary",
    "LAST_LINE": None,
}


@dataclass
class TestInfo:
    title: str = ""
    category: str = ""
    outcome: str = ""
    caplog: str = ""
    capstderr: str = ""
    capstdout: str = ""
    text: str = ""
    keywords: set = ()


class Results:
    def __init__(self):
        self._reports = self._unpickle()
        self._marked_output = MarkedSections()
        self._unmarked_output = self._get_unmarked_output()
        self._test_info = self._process_reports()

        self.test_results = self._deduplicate()
        self.test_session_starts = self.get_terminal_output()

        self.categorize_tests()
        self.errors = self.get_result_by_outcome("ERROR")
        self.failures = self.get_result_by_outcome("FAILED")
        self.passes = self.get_result_by_outcome("PASSED")
        self.xfails = self.get_result_by_outcome("XFAIL")
        self.skipped = self.get_result_by_outcome("SKIPPED")
        self.xpasses = self.get_result_by_outcome("XPASS")

    def update_test_result_by_testname(self, title: str, result: str) -> None:
        for test_result in self.test_results:
            if title == test_result.title:
                test_result.category = result

    def categorize_tests(self) -> None:
        for line in self.test_session_starts.split("\n"):
            possible_match = re.search(test_outcome_matcher, strip_ansi(line))
            if possible_match:
                title = possible_match.groups()[0]
                outcome = possible_match.groups()[1]
                self.update_test_result_by_testname(title, outcome)

    def get_result_by_outcome(self, outcome: str) -> None:
        return {
            test_result.title: test_result.caplog
            + test_result.capstderr
            + test_result.capstdout
            for test_result in self.test_results
            if test_result.category == outcome
        }

    def _get_test_details_by_test_name(self, testname: str) -> str:
        summary = strip_ansi(self.test_session_starts)

    def _get_unmarked_output(
        self, unmarked_file_path: Path = UNMARKEDTERMINALOUTPUTFILE
    ) -> list:
        with open(UNMARKEDTERMINALOUTPUTFILE, "r") as umfile:
            return umfile.read()

    def _unpickle(self):
        """Unpack pickled file from disk"""
        with open(REPORTFILE, "rb") as rfile:
            return pickle.load(rfile)

    def _deduplicate(self):
        """Remove duplicate _test_info to give 1:1 test-title:result"""
        return list({item.title: item for item in self._test_info}.values())

    def _process_reports(self):
        """Extract individual test results from the pytest marked output"""
        test_infos = []
        for report in self._reports:
            test_info = TestInfo()

            # populate the TestInfo instance with pertinent data from report
            test_info.outcome = report.outcome
            test_info.caplog = report.caplog
            test_info.capstderr = report.capstderr
            test_info.capstdout = report.capstdout
            test_info.title = report.head_line
            test_info.keywords = set(report.keywords)

            # categorize the TestInfo instance
            if (
                report.when in ("setup", "call", "teardown")
                and report.outcome == "failed"
            ):
                test_info.category = "error"
            elif (
                report.when in ("setup", "call", "teardown")
                and report.outcome == "skipped"
            ):
                test_info.category = "skipped"
            elif report.when == "call" and report.outcome == "failed":
                test_info.category = "failed"
            elif report.when == "call" and report.outcome == "passed":
                test_info.category = "passed"
            elif report.when == "setup" and report.outcome == "skipped":
                test_info.category = "skipped"
            elif report.when == "call" and report.outcome == "skipped":
                test_info.category = "xfail"
            else:
                continue

            # ...except for failures, wihch get ANSI-coded text from the marked sections
            if test_info.category == "failed":
                try:
                    test_info.text = (
                        self._marked_output.get_failed_test_text_by_test_name(
                            test_info.title
                        )
                    )
                except:
                    try:
                        test_info.text = report.longreprtext
                    except:
                        test_info.text == ""
            else:
                test_info.text == ""

            test_infos.append(test_info)

        return test_infos

        def get_marked_output(self):
            return self.marked_output

    # These functions combine all outputs from one test
    def get_errors(self):
        return {
            test_result.title: test_result.caplog
            + test_result.capstderr
            + test_result.capstdout
            for test_result in self.test_results
            if test_result.category == "error"
        }

    def get_failures(self):
        return {
            test_result.title: test_result.caplog
            + test_result.capstderr
            + test_result.capstdout
            + test_result.text
            for test_result in self.test_results
            if test_result.category == "failed"
        }

    def get_warnings(self):
        # currently un-implemented; need to figure out how to tell when individual
        # TestReport items indicate a test that has a warning
        return {}

    def get_passes(self):
        return {
            test_result.title: test_result.caplog
            + test_result.capstderr
            + test_result.capstdout
            for test_result in self.test_results
            if test_result.category == "passed"
        }

    def get_xfails(self):
        return {
            test_result.title: test_result.caplog
            + test_result.capstderr
            + test_result.capstdout
            for test_result in self.test_results
            if test_result.category == "xfail" and "xfail" not in test_result.keywords
        }

    def get_xpasses(self):
        return {
            test_result.title: test_result.caplog
            + test_result.capstderr
            + test_result.capstdout
            for test_result in self.test_results
            if test_result.category == "passed" and "xfail" in test_result.keywords
        }

    def get_skipped(self):
        return {
            test_result.title: test_result.caplog
            + test_result.capstderr
            + test_result.capstdout
            for test_result in self.test_results
            if test_result.outcome == "skipped"
        }

    def get_results(self) -> list:
        return self.test_results

    def get_terminal_output(self) -> bytes:
        for section in self._marked_output._sections:
            if section["name"] == "TEST_SESSION_STARTS":
                return section["content"]


class MarkedSections:
    def __init__(self, marked_file_path: Path = MARKEDTERMINALOUTPUTFILE) -> None:
        self._marked_lines = self._get_marked_lines(marked_file_path)
        self._sections = self._sectionize(self._marked_lines)
        self._parsed_sections = []

    def get_section(self, name: str) -> str:
        # return marked section, or if not found (e.g. didn't occur in output),
        # return blank dict w/ /no section content
        if name in SECTIONS:
            return next(
                (section for section in self._sections if name == section["name"]),
                {"name": name, "test_title": "", "content": ""},
            )
        else:
            raise NameError(f"Cannot retrieve section by name: '{name}'")

    def get_failed_test_text_by_test_name(self, name: str) -> str:
        # sourcery skip: use-next
        for section in self._sections:
            if section["name"] == "FAILED_TEST" and name == section["test_title"]:
                return section["content"]
        return ""

    def _get_marked_lines(
        self, marked_file_path: Path = MARKEDTERMINALOUTPUTFILE
    ) -> list:
        """Return a list of all lines from the marked output file"""
        with open(MARKEDTERMINALOUTPUTFILE, "r") as mfile:
            return mfile.readlines()

    def _line_is_a_marker(self, line: str) -> bool:
        """Determine if the current line is a marker or part of Pytest output"""
        return line.strip() in (
            MARKERS["pytest_fold_test_session_starts"],
            MARKERS["pytest_fold_errors_section"],
            MARKERS["pytest_fold_failures_section"],
            MARKERS["pytest_fold_passes_section"],
            MARKERS["pytest_fold_warnings_summary"],
            MARKERS["pytest_fold_short_test_summary"],
        ) if line.strip() else False

    def _line_is_lastline(self, line: str) -> bool:
        # sourcery skip: assign-if-exp, reintroduce-else, simplify-empty-collection-comparison, swap-if-expression
        """Determine if the current line is the last line in Pytest's output"""
        if line.strip() == "":
            return False
        return line.strip() in MARKERS["pytest_fold_last_line"]

    def _sectionize(self, lines: list) -> dict:
        """
        Parse marked lines from a Pytest run's console output, and build up a 'section'
        dictionary corresponding to individual sections of the output.
        'section' dict: {name, test_title, content}
        """
        sections = []
        section = {"name": None, "test_title": "", "content": ""}
        lastline = False

        for line in lines:
            if self._line_is_a_marker(line):
                sections.append(section.copy()) if section["name"] else None
                section["name"] = re.search(section_name_matcher, line).groups()[0]
                section["test_title"] = ""
                section["content"] = ""
            elif self._line_is_lastline(line):
                lastline = True
                sections.append(section.copy())
                section["name"] = re.search(section_name_matcher, line).groups()[0]
                section["test_title"] = ""
                section["content"] = ""
            else:
                section["content"] += line
                if re.search(test_title_matcher, line):
                    section["test_title"] = re.search(
                        test_title_matcher, line
                    ).groups()[0]
                sections.append(section.copy()) if lastline else None
        return sections
