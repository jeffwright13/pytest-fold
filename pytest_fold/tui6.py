import os
import sys
import utils
from pathlib import Path
from rich.console import RenderableType
from rich.syntax import Syntax
from rich.traceback import Traceback
from textual.app import App
from textual.widgets import Header, Footer
from pynput import mouse, keyboard

RESULTS_FILE = "pytest_fold/console_output.fold"


class ResultsData:
    def __init__(self, path: Path = RESULTS_FILE):
        self.results_file = path
        self.sections = []

    def get_results(self):
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = utils.tokenize(results_lines)


class MyApp(App):
    # super().__init__(title = "Pytest-Fold")
    def __init__(self):
        App.__init__(self, title="Pytest-Fold")

    results_data = ResultsData(RESULTS_FILE)
    results_data.get_results()

    async def on_load(self) -> None:
        """Sent before going in to application mode."""

        # Bind our basic keys
        await self.bind("q", "quit", "Quit")

        # Get path to show
        try:
            self.path = sys.argv[1]
        except IndexError:
            self.path = os.path.abspath(
                os.path.join(os.path.basename(__file__), "../../")
            )

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""

        # Dock our widgets
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")


def main():
    my_app = MyApp()
    my_app.title = "Pytest-Fold"
    my_app._title = "Pytest-Fold"
    my_app.run()


if __name__ == "__main__":
    main()
