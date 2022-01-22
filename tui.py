from pathlib import Path
import itertools
from asciimatics.screen import Screen

starter = "==>MARKER1<=="
stopper = "==>MARKER2<=="


class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def is_same_as(self, other):
        return self.x == other.x and self.y == other.y


class Fold:
    def __init__(self, filepath: Path):
        self.resultsfile = filepath
        with open(self.resultsfile, "r") as results_file:
            self.results_lines = results_file.readlines()
        self.sections = None
        self.section_points = []

    def tokenize(self) -> list[str]:
        sections = []
        section_content = ""
        first_marker_seen = False
        for line in self.results_lines:
            if not first_marker_seen:
                if starter in line:
                    first_marker_seen = True
                    sections.append(section_content)
                    section_content = ""
                    continue
                section_content += line
                continue
            if starter in line:
                continue
            if stopper in line:
                sections.append(section_content)
                section_content = ""
                continue
            section_content += line
        sections.append(section_content)
        self.sections = sections

    def render(self, screen):
        screen.clear()
        for _ in range(len(self.sections)):
            P = Point(0, _)
            self.section_points.append(P)
            screen.print_at("▶", P.x, P.y)
        screen.refresh()

        while True:
            event = screen.get_event()
            if event:
                if "MouseEvent" in repr(type(event)):
                    ClickPoint = Point(event.x, event.y)
                    for point in self.section_points:
                        if ClickPoint.is_same_as(point):
                            if screen.get_from(point.x, point.y)[0] == ord("▶"):
                                screen.print_at("▼", point.x, point.y)
                                for _, line in enumerate(self.sections, start=1):
                                    screen.print_at(line, point.x, point.y + _)
                                    screen.refresh()
                            else:
                                screen.print_at("▶", point.x, point.y)
                    # screen.clear()
                    screen.refresh()
                if "KeyboardEvent" in repr(type(event)):
                    if event.key_code in (ord("Q"), ord("q")):
                        return
                else:
                    continue



def main():
    F = Fold(Path.cwd() / "console_output.fold")
    F.tokenize()
    # F.render()
    Screen.wrapper(F.render)


def main_orig(
    inp_file: str = "/Users/jwr003/coding/pytest-fold/output_files_to_analyze/outputfulltracefold.ansi",
):
    with open(inp_file, "r") as results_file:
        results_lines = results_file.readlines()
        fold_symbols = itertools.cycle(["▼", "▶"])

        def folder(screen):
            # Set up points denoting fold symbol, and first line of results text
            P1 = Point(0, 0)

            # Draw initially-unfolded results text ("▶")
            screen.clear()
            screen.print_at("▶", P1.x, P1.y)
            screen.refresh()

            # main loop; looks for mouse click on folding-arrow to fold/collapse
            # the Pytest output text; or a "q" to quit the program
            while True:
                event = screen.get_event()

                if event:
                    if "MouseEvent" in repr(type(event)):
                        ClickPoint = Point(event.x, event.y)
                        if ClickPoint.is_same_as(P1):
                            if screen.get_from(P1.x, P1.y)[0] == ord("▶"):
                                screen.print_at(next(fold_symbols), P1.x, P1.y)
                                for _, result_line in enumerate(results_lines, start=1):
                                    screen.print_at(result_line, P1.x, P1.y + _)
                                    screen.refresh()
                            else:
                                screen.clear()
                                screen.print_at(next(fold_symbols), P1.x, P1.y)
                                screen.refresh()

                    elif "KeyboardEvent" in repr(type(event)):
                        if event.key_code in (ord("Q"), ord("q")):
                            return

                    else:
                        continue

        # Kick off the asciimatics Screen instance
        Screen.wrapper(folder)


if __name__ == "__main__":
    main()
