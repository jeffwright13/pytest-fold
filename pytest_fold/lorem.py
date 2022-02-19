from __future__ import annotations

import lorem
from ansi.colour import fg
from ansi.colour.fx import reset

from random import choice
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import Header, Footer
from textual.reactive import Reactive

sections = 4 * [lorem.paragraph(), lorem.sentence(), lorem.text()]
colours = ["red", "yellow", "green", "blue", "cyan", "magenta"]
coloured_sections = []
for section in sections:
    foreground = choice(colours)
    coloured_section = (eval(f"fg.{foreground}"), section, reset)
    coloured_sections.append("".join(map(str, coloured_section)))


class Hover(Widget):
    mouse_over = Reactive(False)
    folded = Reactive(False)

    def __init__(self, size: tuple = (0, 0), text: str = "") -> None:
        super().__init__(size)
        self.text = text
        self.panel = Panel(self.text)
        self.folded = True
        self.collapsed_size = 4
        self.full_size = 6

    def render(self) -> Panel:
        return Panel(
            self.text,
            style=("italic" if not self.mouse_over else "bold"),
            height=self.collapsed_size if self.folded else self.full_size,
        )

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_click(self) -> None:
        self.folded = not (self.folded)

    def on_leave(self) -> None:
        self.mouse_over = False


class HoverApp(App):
    async def on_load(self, event: events.Load) -> None:
        await self.bind("t", "view.toggle('topbar')", "Toggle Overview")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        await self.view.dock(Header(), edge="top", size=1)
        await self.view.dock(Footer(), edge="bottom")

        hovers = [
            Hover(text=Text.from_ansi(coloured_section))
            for coloured_section in coloured_sections
        ]
        await self.view.dock(*hovers, edge="top")


def main():
    HoverApp.run(log="textual.log")


if __name__ == "__main__":
    main()
