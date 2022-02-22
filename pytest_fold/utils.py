import re
from pathlib import Path

failures_matcher = re.compile(r"^==.*\sFAILURES\s==+")
errors_matcher = re.compile(r"^==.*\sERRORS\s==+")
failed_test_marker = re.compile(r"^__.*\s(.*)\s__+")
warnings_summary_matcher = re.compile(r"^==.*warnings summary\s.*==+")
summary_matcher = re.compile(r"^==.*short test summary info\s.*==+")
lastline_matcher = re.compile(r"^==.*in\s\d+.\d+s.*==+")

foldmark_matcher = re.compile(r".*(~~>PYTEST_FOLD_MARKER_)+(.*)<~~")
section_name_matcher = re.compile(r"~~>PYTEST_FOLD_MARKER_(\w+)")
test_title_matcher = re.compile(r"__.*\s(.*)\s__+")

OUTFILE = Path.cwd() / "console_output.fold"
PICKLEFILE = Path.cwd() / "console_output.pickle"
MARKERS = {
    "pytest_fold_firstline": "~~>PYTEST_FOLD_MARKER_FIRSTLINE<~~",
    "pytest_fold_errors": "~~>PYTEST_FOLD_MARKER_ERRORS<~~",
    "pytest_fold_failures": "~~>PYTEST_FOLD_MARKER_FAILURES<~~",
    "pytest_fold_failed_test": "~~>PYTEST_FOLD_MARKER_FAILED_TEST<~~",
    "pytest_fold_warnings_summary": "~~>PYTEST_FOLD_MARKER_WARNINGS_SUMMARY<~~",
    "pytest_fold_lastline": "~~>PYTEST_FOLD_MARKER_LASTLINE<~~",
    "pytest_fold_terminal_summary": "~~>PYTEST_FOLD_MARKER_TERMINAL_SUMMARY<~~",
}


def line_is_a_marker(line: str) -> bool:
    if line.strip() == "":
        return False
    return line.strip() in (
        MARKERS["pytest_fold_firstline"],
        MARKERS["pytest_fold_errors"],
        MARKERS["pytest_fold_failures"],
        MARKERS["pytest_fold_failed_test"],
        MARKERS["pytest_fold_warnings_summary"],
        MARKERS["pytest_fold_terminal_summary"],
    )


def line_is_lastline(line: str) -> bool:
    if line.strip() == "":
        return False
    return line.strip() in MARKERS["pytest_fold_lastline"]


def sectionize(lines: str) -> dict:
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
        if line_is_a_marker(line):
            sections.append(section.copy()) if section["name"] else None
            section["test_title"] = ""
            section["content"] = ""
            section["name"] = re.search(section_name_matcher, line).groups()[0]
        elif line_is_lastline(line):
            lastline = True
            sections.append(section.copy())
            section["content"] = ""
            section["name"] = re.search(section_name_matcher, line).groups()[0]
        else:
            section["content"] += line
            if re.search(test_title_matcher, line):
                section["test_title"] = re.search(test_title_matcher, line).groups()[0]
            sections.append(section.copy()) if lastline else None

    return sections
