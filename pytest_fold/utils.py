from plugin import MARKERS

def tokenize(lines: str) -> list[str]:
    """
    Parse lines from a Pytest run's console output which are marked with Pytest-Fold
    markers, and build up a list of ANSI text strings corresponding to individual sections of the output. This function is meant to be called from the Pytest-Fold
    TUI for interactive display.
    """
    sections = []
    section_content = ""
    marker1_seen = False

    for line in lines:
        if not marker1_seen:
            if marker1 in line:
                marker1_seen = True
                sections.append(section_content)
                section_content = ""
                continue
            section_content += line
            continue
        if marker1 in line:
            continue
        if marker2 in line:
            sections.append(section_content)
            section_content = ""
            continue
        section_content += line
    sections.append(section_content)
    return sections


def tokenize_orig(lines: str, marker1: str=MARKER1, marker2: str=MARKER2) -> list[str]:
    sections = []
    section_content = ""
    marker1_seen = False
    for line in lines:
        if not marker1_seen:
            if marker1 in line:
                marker1_seen = True
                sections.append(section_content)
                section_content = ""
                continue
            section_content += line
            continue
        if marker1 in line:
            continue
        if marker2 in line:
            sections.append(section_content)
            section_content = ""
            continue
        section_content += line
    sections.append(section_content)
    return sections
