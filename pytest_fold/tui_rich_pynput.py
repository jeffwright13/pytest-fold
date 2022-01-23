import os
import sys
import utils
from math import ceil
from pathlib import Path

from rich import print, box
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from pynput import keyboard, mouse

# RESULTS_FILE = "/Users/jwr003/coding/pytest-fold/output_files_to_analyze/outputtblongfold.ansi"
RESULTS_FILE = "/Users/jwr003/coding/pytest-fold/output_files_to_analyze/outputvfold.ansi"
BORDER_COLOR = "#3399ff"

class ResultsData:
    def __init__(self, path: Path = RESULTS_FILE):
        self.results_file = path
        self.sections = []

    def get_results(self):
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = utils.tokenize(results_lines)


def main():
    results_data = ResultsData()
    results_data.get_results()

    console = Console()
    console.clear()
    console.print(Panel(results_data.sections[0], title="▶ Pytest start info", border_style=BORDER_COLOR, title_align="left"))
    for _ in range(len(results_data.sections) - 1):
        console.print(Panel(results_data.sections[_], height=0, title=f"▶ Pytest test {_}", border_style=BORDER_COLOR, title_align="left"))
    console.print(Panel(results_data.sections[-1], title="▶ Pytest finish info", border_style=BORDER_COLOR, title_align="left"))



    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    # Collect events until released
    with mouse.Listener(
            on_move=None,
            on_click=on_click,
            on_scroll=None) as listener:
        listener.join()


if __name__ == "__main__":
    main()
