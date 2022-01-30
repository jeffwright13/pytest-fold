import os
import sys
import utils

from pathlib import Path
from typing import Optional

from rich.panel import Panel
from rich.console import Console, RenderableType
from rich.syntax import Syntax
from rich.traceback import Traceback
from rich import box
from rich.style import Style
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from textual.app import App
from textual.widgets import Header, Footer, ButtonPressed, Button
from textual.reactive import Reactive
from textual.widget import Widget
from textual.app import App
from textual.events import Click, MouseDown
from textual.reactive import Reactive
from textual import events
from textual.widget import Widget
from textual.widgets import Header, Footer, Placeholder, ScrollView
from textual.widgets import Button

RESULTS_FILE = "/Users/jwr003/coding/pytest-fold/output_files_to_analyze/outputvfold.ansi"
BORDER_COLOR = "#3399ff"

class ResultsData:
    def __init__(self, path: Path = RESULTS_FILE) -> None:
        self.results_file = path
        self.sections = []

    def _sectionize_results(self) -> None:
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = utils.sectionize(results_lines)

    def get_results(self) -> list:
        self._sectionize_results()
        return self.sections


class Label(Widget):
    label: Reactive[str] = Reactive('')

    def __init__(self, label: str, name: Optional[str] = None):
        super().__init__(name=name)
        self.label = label

    def render(self) -> Panel:
        return Panel(self.label, box=box.SQUARE)

    def on_click(self, event: Click) -> None:
        event.prevent_default().stop()
        self.label += 'clicked'


class PyfoldApp(App):
    """Create user interface"""

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

        # Create our widgets
        # In this a scroll view for the code and a directory tree
        # self.body = ScrollView()
        self.button = Button(label="Button1", name="MyButton", style="red")

        # Dock our widgets
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        # await self.view.dock(self.body, edge="top")
        await self.view.dock(self.button, edge="left")

        # async def add_content():
        #     results_data = ResultsData()
        #     sections = results_data.get_results()
        #     console = Console()
        #     console.clear()
        #     console.print(Panel(results_data.sections[0], title="▶ Pytest start info", border_style=BORDER_COLOR, title_align="left"))
        #     for _ in range(len(results_data.sections) - 1):
        #         console.print(Panel(results_data.sections[_], height=0, title=f"▶ Pytest test {_}", border_style=BORDER_COLOR, title_align="left"))
        #     console.print(Panel(results_data.sections[-1], title="▶ Pytest finish info", border_style=BORDER_COLOR, title_align="left"))

        # await self.call_later(add_content)


def main():
    results_data = ResultsData()
    sections = results_data.get_results()

    console = Console()
    console.clear()
    console.print(Panel(results_data.sections[0], title="▶ Pytest start info", border_style=BORDER_COLOR, title_align="left"))
    for _ in range(len(results_data.sections) - 1):
        console.print(Panel(results_data.sections[_], height=0, title=f"▶ Pytest test {_}", border_style=BORDER_COLOR, title_align="left"))
    console.print(Panel(results_data.sections[-1], title="▶ Pytest finish info", border_style=BORDER_COLOR, title_align="left"))

    PyfoldApp.run(title="Pyfold Viewer", log="textual.log")

if __name__ == "__main__":
    main()
