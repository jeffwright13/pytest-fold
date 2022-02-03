import re
from plugin import MARKERS

foldmark_matcher = re.compile(r".*(~~>PYTEST_FOLD_MARKER_)+(.*)<~~")
fail_begin_end_matcher = re.compile(r"(.+)((_BEGIN)|(_END))")
section_name_matcher = re.compile(r"~~>PYTEST_FOLD_MARKER_(\w+)")


def line_is_a_marker(line: str) -> bool:
    if line.strip() == "":
        return False
    return line.strip() in (
        MARKERS["pytest_fold_firstline"],
        MARKERS["pytest_fold_errors"],
        MARKERS["pytest_fold_failures"],
        MARKERS["pytest_fold_failed_test"],
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
    section = {"name": None, "content": ""}
    lastline = False

    for line in lines:
        if line_is_a_marker(line):
            sections.append(section.copy()) if section["name"] else None
            section["content"] = ""
            section["name"] = re.search(section_name_matcher, line).groups()[0]
        elif line_is_lastline(line):
            lastline = True
            sections.append(section.copy())
            section["content"] = ""
            section["name"] = re.search(section_name_matcher, line).groups()[0]
        else:
            section["content"] += line
            sections.append(section.copy()) if lastline else None

    return sections
