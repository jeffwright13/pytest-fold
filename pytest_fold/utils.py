import re
import pickle
from dataclasses import dataclass
from pathlib import Path

REPORTFILE = Path.cwd() / "report_objects.bin"
MARKEDTERMINALOUTPUTFILE = Path.cwd() / "marked_output.bin"
UNMARKEDTERMINALOUTPUTFILE = Path.cwd() / "unmarked_output.bin"

test_session_starts_matcher = re.compile(r"^==.*\test session starts\s==+")
errors_section_matcher = re.compile(r"^==.*\sERRORS\s==+")
failures_section_matcher = re.compile(r"^==.*\sFAILURES\s==+")
warnings_summary_matcher = re.compile(r"^==.*warnings summary\s.*==+")
passes_section_matcher = re.compile(r"^==.*\sPASSES\s==+")
short_test_summary_matcher = re.compile(r"^==.*short test summary info\s.*==+")
lastline_matcher = re.compile(r"^==.*in\s\d+.\d+s.*==+")

section_name_matcher = re.compile(r"~~>PYTEST_FOLD_MARKER_(\w+)")
test_title_matcher = re.compile(r"__.*\s(.*)\s__+")

MARKERS = {
    "pytest_fold_test_session_starts": "~~>PYTEST_FOLD_TEST_SESSION_STARTS<~~",
    "pytest_fold_errors_section": "~~>PYTEST_FOLD_ERRORS_SECTION<~~",
    "pytest_fold_passes_section": "~~>PYTEST_FOLD_PASSES_SECTION<~~",
    "pytest_fold_failures_section": "~~>PYTEST_FOLD_FAILURES_SECTION<~~",
    "pytest_fold_warnings_summary": "~~>PYTEST_FOLD_WARNINGS_SUMMARY<~~",
    "pytest_fold_short_test_summary": "~~>PYTEST_FOLD_TERMINAL_SUMMARY<~~",
    "pytest_fold_lastline": "~~>PYTEST_FOLD_LASTLINE<~~",
}

KNOWN_TYPES = (
    "failed",
    "passed",
    "skipped",
    "deselected",
    "xfailed",
    "xpassed",
    "warnings",
    "error",
)


@dataclass
class TestInfo:
    title: str = ""
    category: str = ""
    outcome: str = ""
    caplog: str = ""
    capstderr: str = ""
    capstdout: str = ""
    text: str = ""


class Results:
    def __init__(self):
        self._reports = self._unpickle()
        self._marked_output = MarkedSections()
        self._unmarked_output = self._get_unmarked_output()
        self._test_info = self._process_reports()

        self.test_results = self._deduplicate()
        self.failures = self.get_failures()
        self.errors = self.get_errors()
        self.passes = self.get_passes()
        self.misc = self.get_misc()

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

            # categorize the TestInfo instance
            if (
                report.when in ("collect", "setup", "teardown")
                and report.outcome == "failed"
            ):
                test_info.category = "error"
            elif (
                report.when in ("collect", "setup", "teardown")
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
    def get_failures(self):
        return {
            entry.title: entry.caplog + entry.capstderr + entry.capstdout + entry.text
            for entry in self.test_results
            if entry.category == "failed"
        }

    def get_errors(self):
        return {
            entry.title: entry.caplog + entry.capstderr + entry.capstdout
            for entry in self.test_results
            if entry.category == "error"
        }

    def get_passes(self):
        return {
            entry.title: entry.caplog + entry.capstderr + entry.capstdout
            for entry in self.test_results
            if entry.category == "passed"
        }

    def get_misc(self):
        return {
            entry.title: entry.caplog + entry.capstderr + entry.capstdout
            for entry in self.test_results
            if entry.category in ("skipped", "xfail")
        }

    def get_results(self) -> list:
        return self.test_results

    def get_terminal_output(self) -> bytes:
        return self._terminal_output


class MarkedSections:
    def __init__(self, marked_file_path: Path = MARKEDTERMINALOUTPUTFILE) -> None:
        self._marked_lines = self._get_marked_lines(marked_file_path)
        self._sections = self._sectionize(self._marked_lines)
        self._parsed_sections = []

    def get_section(self, name: str) -> str:
        # return marked section, or if not found (e.g. didn't occur in output),
        # return blank dict w/ /no section content
        if name in {
            "FIRSTLINE",
            "ERRORS",
            "PASSES",
            "FAILURES",
            "WARNINGS_SUMMARY",
            "TERMINAL_SUMMARY",
            "LASTLINE",
        }:
            return next(
                (section for section in self._sections if name == section["name"]),
                {"name": name, "test_title": "", "content": ""},
            )

        else:
            raise Exception(f"Cannot retrieve section by name: '{name}'")

    def get_failed_test_text_by_test_name(self, name: str) -> str:
        for section in self._sections:
            if section["name"] == "FAILED_TEST" and name == section["test_title"]:
                return section["content"]
        return ""

    def _get_marked_lines(
        self, marked_file_path: Path = MARKEDTERMINALOUTPUTFILE
    ) -> list:
        with open(MARKEDTERMINALOUTPUTFILE, "r") as mfile:
            return mfile.readlines()

    def _line_is_a_marker(self, line: str) -> bool:
        if line.strip() == "":
            return False
        return line.strip() in (
            MARKERS["pytest_fold_test_session_starts"],
            MARKERS["pytest_fold_errors_section"],
            MARKERS["pytest_fold_failures_section"],
            MARKERS["pytest_fold_failed_test"],
            MARKERS["pytest_fold_warnings_summary"],
            MARKERS["pytest_fold_short_test_summary"],
        )pytest_fold_short_test_summary

    def _line_is_lastline(self, line: str) -> bool:
        if line.strip() == "":
            return False
        return line.strip() in MARKERS["pytest_fold_lastline"]

    def _sectionize(self, lines: list) -> dict:
        """
        Parse lines from a Pytest run's console output which are marked with Pytest-Fold
        markers, and build up a dictionary of ANSI text strings corresponding to individual
        sections of the output. This function is meant to be called from the Pytest-Fold
        TUI for interactive display.
        """
        sections = []
        section = {"name": None, "test_title": "", "content": ""}
        lastline = False

        for line in lines:
            if self._line_is_a_marker(line):
                sections.append(section.copy()) if section["name"] else None
                section["test_title"] = ""
                section["content"] = ""
                section["name"] = re.search(section_name_matcher, line).groups()[0]
            elif self._line_is_lastline(line):
                lastline = True
                sections.append(section.copy())
                section["content"] = ""
                section["name"] = re.search(section_name_matcher, line).groups()[0]
            else:
                section["content"] += line
                if re.search(test_title_matcher, line):
                    section["test_title"] = re.search(
                        test_title_matcher, line
                    ).groups()[0]
                sections.append(section.copy()) if lastline else None
        return sections
