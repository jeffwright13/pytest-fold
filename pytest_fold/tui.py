import itertools
from asciimatics.screen import Screen, Canvas


class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def is_same_as(self, other):
        return self.x == other.x and self.y == other.y


with open("/Users/jwr003/coding/pytest-fold/output.ansi", "r") as results_file:
    results_lines = results_file.readlines()
    results = "".join(results_lines)
    num_results_lines = len(results_lines)
    print(num_results_lines)
    fold_symbols = itertools.cycle(["▼", "▶"])

    def folder(screen):
        # Set up points denoting fold symbol, and first line of results text
        P1 = Point(0, 0)

        # Draw initially-unfolded results text ("▶")
        screen.clear()
        screen.print_at("▶", P1.x, P1.y)
        screen.refresh()

        # main loop
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

    Screen.wrapper(folder)
