from pathlib import Path
from rich.text import Text
from rich.markdown import Markdown
from textual import events
from textual.app import App
from textual.widgets import Header, Footer, Placeholder, ScrollView
from pytest_fold.utils import MARKERS, OUTFILE, sectionize


class ResultsData:
    """
    Class to read in results from a 'pytest --fold' session (which inserts markers
    around each failed test), and sectionize the results into individual sections for
    display on the TUI
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


class MyApp(App):
    """A Text User Interface (TUI) for displaying results of `pytest --fold`"""
    # def __init__(self, sections) -> None:
    #     super(MyApp, self).__init__()
    #     self.sections = sections

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("t", "view.toggle('topbar')", "Toggle Overview")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""

        sections = ResultsData().get_results()

        # A scrollview to contain the markdown file
        body = ScrollView(gutter=1)

        # Header / footer / dock
        await self.view.dock(Header(), edge="top", size=1)
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(Placeholder(), edge="top", size=len(sections), name="topbar")

        # Dock the body in the remaining space
        await self.view.dock(body, edge="right")

        async def get_ansi(filename: str) -> None:
            with open(filename, "r") as fh:
                results = Text.from_ansi(fh.read())
            await body.update(results)

        # await self.call_later(get_ansi, OUTFILE)
        await self.call_later(get_ansi, "/Users/jwr003/coding/pytest-fold/console_output.fold")


def main():
    MyApp.run()

if __name__ == "__main__":
    main()


"""
from rich.text import Text
with open("console_output.fold", "r") as f:
    t = f.read()
t1 = Text.from_ansi(t)
rich.print(t1)
"""
