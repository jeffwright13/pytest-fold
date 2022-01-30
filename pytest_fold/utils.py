import re
from plugin import MARKERS


def sectionize(lines: str) -> dict:
    """
    Parse lines from a Pytest run's console output which are marked with Pytest-Fold
    markers, and build up a dictionary of ANSI text strings corresponding to individual
    sections of the output. This function is meant to be called from the Pytest-Fold
    TUI for interactive display.
    """
    p1 = re.compile(r".*(==>PYTEST_FOLD_MARKER_)+(.*)<==")
    p2 = re.compile(r"(.+)((_BEGIN)|(_END))")
    sections = []
    section = {"name": None, "content": ""}

    for _, line in enumerate(lines):
        search1 = re.search(p1, line)
        if search1:  # line contains a section marker
            search2 = re.search(p2, search1.groups()[1])
            if "BEGIN" in search2.groups()[1]:
                if section["name"] == "Unmarked":
                    sections.append(section.copy())
                section["name"] = search2.groups()[0]
                section["content"] = ""
                continue
            if "END" in search2.groups()[1]:
                sections.append(section.copy())
                section["name"] = None
                section["content"] = ""
                continue
        else:
            if not section["name"]:
                section["name"] = "Unmarked"
            section["content"] += line
            if _ == len(lines) - 1:
                section["name"] = "Final"
                sections.append(section.copy())
                break
            continue

    sections2 = []
    temp_name = None
    temp_content = ""
    for section in sections:
        if section["name"] in ["SESSION_START", "Final"]:
            sections2.append(section.copy())
        else:
            temp_content += section["content"]
            if section["name"] != "Unmarked":
                sections2.append({"name": section["name"], "content": temp_content})
                temp_content = ""

    return sections2
