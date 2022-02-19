import re
from pathlib import Path

from rich.console import RenderableType
from rich.text import Text
from rich import print
from rich.panel import Panel
from rich.style import Style

from textual import events
from textual.app import App
from textual.reactive import Reactive
from textual.views import DockView
from textual.widgets import Header, Footer, TreeControl, ScrollView, TreeClick

from pytest_fold.utils import MARKERS, OUTFILE, sectionize


class ResultsData:
    """
    Class to read in results from a 'pytest --fold' session (which inserts markers
    around each failed test), and sectionize the results into individual sections for
    display on the TUI. Relies on utils.py.
    """

    def __init__(self, path: Path = OUTFILE) -> None:
        self.results_file = path
        self.sections = []
        self.parsed_sections = []

    def _sectionize_results(self) -> None:
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = sectionize(results_lines)

    def get_results(self) -> list:
        self._sectionize_results()
        return self.sections

    def get_results_dict(self) -> dict:
        self.results = self.get_results()
        d = {}
        for section in self.results:
            if section["test_title"]:
                d[section["test_title"]] = section["content"]
            else:
                d[section["name"]] = section["content"]
        return d


class PytestFoldApp(App):
    async def on_load(self, event: events.Load) -> None:
        self.results = ResultsData().get_results_dict()
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        header = Header(tall=False)
        header.__setattr__("title", "Howdy")
        footer = Footer()
        await self.view.dock(header, edge="top", size=1)
        await self.view.dock(footer, edge="bottom")
        print("")

        tree = TreeControl("SESSION RESULTS:", {})
        for results_key in self.results.keys():
            await tree.add(tree.root.id, Text(results_key), {"results": self.results})
            if tree.nodes[tree.id].label.plain == "FIRSTLINE":
                tree.nodes[tree.id].label.stylize("bold blue")
            elif tree.nodes[tree.id].label.plain == "FAILURES":
                tree.nodes[tree.id].label.stylize("bold red")
            elif tree.nodes[tree.id].label.plain == "ERRORS":
                tree.nodes[tree.id].label.stylize("bold magenta")
            elif tree.nodes[tree.id].label.plain == "WARNINGS_SUMMARY":
                tree.nodes[tree.id].label.stylize("bold yellow")
            elif tree.nodes[tree.id].label.plain == "TERMINAL_SUMMARY":
                tree.nodes[tree.id].label.stylize("bold green")
            elif tree.nodes[tree.id].label.plain == "LASTLINE":
                tree.nodes[tree.id].label.stylize("bold blue")
            else:
                tree.nodes[tree.id].label.stylize("italic")
        await tree.root.expand()

        self.body = ScrollView()
        self.dock_view = DockView()
        await self.view.dock(ScrollView(tree), edge="left", size=48, name="sidebar")
        await self.view.dock(self.dock_view)
        await self.dock_view.dock(self.body, edge="top", size=48)

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        """Called in response to a tree click."""
        label = message.node.label
        self.text = message.node.data.get("results")[label._text[0]]

        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    PytestFoldApp(title="pytest --fold results").run()


if __name__ == "__main__":
    main()
