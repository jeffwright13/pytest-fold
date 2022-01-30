# from curses.textpad import Textbox
import itertools
import utils

from pathlib import Path
from asciimatics.screen import Screen, ManagedScreen
from asciimatics.widgets import Frame, Layout, Text, TextBox



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
        self.section_points = []
        self.sections = utils.sectionize(self.results_lines)

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
                if "KeyboardEvent" in repr(type(event)) and event.key_code in (
                    ord("Q"),
                    ord("q"),
                ):
                    return


class Pyfold_TUI:
    def __init__(self, screen):
        frame = Frame(screen, 80, 20, has_border=False)
        layout = Layout([1, 1, 1, 1])
        frame.add_layout(layout)
        # layout.add_widget(Textbox(5, line_wrap=True, readonly=True))
        layout.add_widget(Textbox())

def main():
    # F = Fold(Path.cwd() / "pytest_fold/console_output.fold")
    # F.render()
    # Screen.wrapper(F.render)
    # T = Pyfold_TUI()
    # Screen.wrapper(Pyfold_TUI)
    with ManagedScreen() as ms:
        frame = Frame(ms, 5, 8)
        layout = Layout([1, 1, 1, 1])
        frame.add_layout(layout)
        pass


if __name__ == "__main__":
    main()
