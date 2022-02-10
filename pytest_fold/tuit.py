from __future__ import annotations
import logging
from collections import Counter
from pathlib import Path
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import Header, Footer, Placeholder, ScrollView
from textual.reactive import Reactive

from pytest_fold.utils import MARKERS, OUTFILE, sectionize


class ResultsData():
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


class Hover(Widget):
    def __init__(self, size: tuple=(0,0), text: str="") -> None:
        super().__init__(size)
        self.text = text

    mouse_over = Reactive(False)

    def render(self) -> Panel:
        return Panel(self.text, style=("dim italic" if not self.mouse_over else ""))

    def on_enter(self) -> None:
        # self._update_size((0, 20))
        self.mouse_over = True

    # def on_click(self) -> None:
    #     width = 20 if self._size[1] == 1 else 1
    #     self._update_size((0, width))

    def on_leave(self) -> None:
        # self._update_size((0, 1))
        self.mouse_over = False


class HoverApp(App):
    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("t", "view.toggle('topbar')", "Toggle Overview")
        await self.bind("q", "quit", "Quit")


    async def on_mount(self) -> None:
        await self.view.dock(Header(), edge="top", size=1)
        await self.view.dock(Footer(), edge="bottom")
        sections = ResultsData().get_results()
        hovers = [Hover(text=Text.from_ansi(section["content"]), size=(10,20)) for section in sections]
        await self.view.dock(*hovers, edge="top", size=6)


# class Hover(Widget):
#     def __init__(self, text):
#         self.text = text

#     mouse_over = Reactive(False)

#     def render(self) -> Panel:
#         return Panel(self.text, style=("on red" if self.mouse_over else ""))

#     def on_enter(self) -> None:
#         self.mouse_over = True

#     def on_leave(self) -> None:
#         self.mouse_over = False

# class HoverApp(App):
#     def __init__(self) -> None:
#         # super().__init__()
#         self.sections = ResultsData().get_results()

    # async def on_load(self, event: events.Load) -> None:
    #     """Bind keys with the app loads (but before entering application mode)"""
    #     await self.bind("t", "view.toggle('topbar')", "Toggle Overview")
    #     await self.bind("q", "quit", "Quit")

    # async def on_mount(self, event: events.Mount) -> None:
    #     hover = Hover(self.sections[0]["content"])
    #     await self.view.dock(hover, edge="top")
        # for section in self.sections:
        #     hover = Hover()
        #     await self.view.dock(hover, edge="top")


        # async def get_ansi(filename: Path) -> None:
        #     with open(filename, "r") as fh:
        #         results = Text.from_ansi(fh.read())
        #     await body.update(results)
        # await self.call_later(get_ansi, OUTFILE)

class TestPanel1(Placeholder):
    def __init__(self, *, name: str | None = None, height: int | None = None, text: str | None = None) -> None:
        super().__init__(name=name)
        self.height = height
        self.text = text

class TestPanel2(ScrollView):
    def __init__(self, *, name: str | None = None, height: int | None = None, contents: str | None = None) -> None:
        super().__init__(name=name)
        self.height = height
        self.contents = contents

#
# class MyApp2(App):
#     async def on_load(self, event: events.Load) -> None:
#         """Bind keys with the app loads (but before entering application mode)"""
#         await self.bind("t", "view.toggle('topbar')", "Toggle Overview")
#         await self.bind("q", "quit", "Quit")

#     async def on_mount(self, event: events.Mount) -> None:
#         """Create and dock the widgets."""

#         sections = ResultsData().get_results()

#         tp2 = TestPanel2()
#         tp2.contents = sections[0]["content"]
#         tpc = Counter(tp2.contents)
#         tp2.height = tpc["\n"]

#         # Header / footer / dock
#         await self.view.dock(Header(), edge="top", size=1)
#         await self.view.dock(Footer(), edge="bottom")
#         # await self.view.dock(tp2)

#         # A scrollview to contain the markdown file
#         body1 = ScrollView(gutter=1)
#         body1.update(sections[0]["content"]
#         )
#         await self.view.dock(body1, edge="right")

#         async def get_ansi(filename: Path) -> None:
#             with open(filename, "r") as fh:
#                 results = Text.from_ansi(fh.read())
#             await body1.update(results)
#         await self.call_later(get_ansi, OUTFILE)



# class MyApp1(App):
#     """A Text User Interface (TUI) for displaying results of `pytest --fold`"""
#     # def __init__(self, sections) -> None:
#     #     super(MyApp, self).__init__()
#     #     self.sections = sections

#     async def on_load(self, event: events.Load) -> None:
#         """Bind keys with the app loads (but before entering application mode)"""
#         await self.bind("t", "view.toggle('topbar')", "Toggle Overview")
#         await self.bind("q", "quit", "Quit")

#     async def on_mount(self, event: events.Mount) -> None:
#         """Create and dock the widgets."""

#         sections = ResultsData().get_results()

#         tp1 = TestPanel1()
#         tp1.text = sections[0]["content"]
#         c = Counter(tp1.text)
#         tp1.height = c["\n"]

#         # A scrollview to contain the markdown file
#         body = ScrollView(gutter=1)

#         # Header / footer / dock
#         await self.view.dock(Header(), edge="top", size=1)
#         await self.view.dock(Footer(), edge="bottom")
#         await self.view.dock(tp1)

#         # Dock the body in the remaining space
#         await self.view.dock(body, edge="right")

#         async def get_ansi(filename: str) -> None:
#             with open(filename, "r") as fh:
#                 results = Text.from_ansi(fh.read())
#             await body.update(results)

#         # await self.call_later(get_ansi, OUTFILE)
#         await self.call_later(get_ansi, "/Users/jwr003/coding/pytest-fold/console_output.fold")


def main():
    logging.basicConfig(level=logging.DEBUG)
    HoverApp.run(log="textual.log")

if __name__ == "__main__":
    main()


"""
from rich.text import Text
with open("console_output.fold", "r") as f:
    t = f.read()
t1 = Text.from_ansi(t)
rich.print(t1)
"""
