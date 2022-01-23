starter = "==>MARKER1<=="
stopper = "==>MARKER2<=="

def tokenize(lines: str, marker1: str=starter, marker2: str=stopper) -> list[str]:
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
