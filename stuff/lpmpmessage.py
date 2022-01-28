#!/usr/bin/env python
"""
lpmpmessage script will display the formatted merge commit message for the
chosen merge proposal

lpmpmessage depends on ``launchpadlib``, which isn't
necessarily up-to-date in PyPI, so we install it from the archive::

`sudo apt-get install python-launchpadlib` OR

`sudo apt-get install python3-launchpadlib` OR

As we're using ``launchpadlib`` from the archive (which is therefore
installed in the system), you'll need to create your virtualenvs
with the ``--system-site-packages`` option.

Activate your virtualenv and install the requirements::

`pip install -r requirements.txt`

"""
import click
from rich import box
from rich.style import Style
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from textual.app import App
from textual.events import Click, MouseDown
from textual.reactive import Reactive
from textual import events
from textual.widget import Widget
from textual.widgets import Header, Footer, Placeholder, ScrollView
from textual.widgets import Button
from typing import Optional

from lpshipit import (
    build_commit_msg,
    _format_git_branch_name,
    _get_launchpad_client,
    _set_urwid_widget,
)
# Global var to store the chosen MP's commit message
MP_MESSAGE_OUTPUT = None


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


class LPMPMessageApp(App):

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        """Create and dock the widgets."""

        # A scrollview to contain the markdown file
        self.body = body = ScrollView(auto_width=True)

        # Header / footer / dock
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(body)

        async def add_content():
            table = Table(title="Choose Merge Proposal", box=box.ASCII, show_header=True, expand=True,
                          row_styles=[Style(frame=True, bgcolor='red'), Style(frame=True, bgcolor='blue')])
            table.add_column("[cyan]author",
                             justify="left",
                             no_wrap=True,)
            table.add_column("[blue]repo",
                             justify="left",
                             no_wrap=False, )
            table.add_column("[blue]button",
                             justify="left",
                             no_wrap=False, )
            for i in range(19):

                table.add_row("repo", "test label in table", Panel("Choose"))

            await body.update(table)

        await self.call_later(add_content)


@click.command()
@click.option('--mp-owner', help='LP username of the owner of the MP '
                                 '(Defaults to system configured user)',
              default=None)
@click.option('--debug/--no-debug', default=False)
def lpmpmessage(mp_owner, debug):
    LPMPMessageApp.run(log="textual.log")


if __name__ == "__main__":
    lpmpmessage()
