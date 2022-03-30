from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.view import messages
from textual.views import DockView, GridView
from textual.widgets import Header, Footer, TreeControl, ScrollView, TreeClick
from pytest_fold.utils import Results


class FoldFooter(Footer):
    # Override default Footer method 'make_key_text' to allow customizations
    def make_key_text(self) -> Text:
        """Create text containing all the keys."""
        text = Text(
            style="bold encircle white on black",
            no_wrap=True,
            overflow="ellipsis",
            justify="center",
            end="",
        )
        for binding in self.app.bindings.shown_keys:
            key_display = (
                binding.key.upper()
                if binding.key_display is None
                else binding.key_display
            )
            hovered = self.highlight_key == binding.key
            key_text = Text.assemble(
                (f" {key_display} ", "reverse" if hovered else "default on default"),
                f" {binding.description} ",
                meta={"@click": f"app.press('{binding.key}')", "key": binding.key},
            )
            text.append_text(key_text)
        return text


class FoldApp(App):
    """
    Textual class inherited from App
    Provides docking and data population for test session headers and results
    """

    async def action_toggle_tree(self, names: list) -> None:
        # self.trees = {child.name: child for child in self.children}
        if type(names) == str:
            names = [names]
        for name in names:
            widget = self.view.named_widgets[
                name
            ]  # <= self here is View; see end of view.py
            widget.visible = not widget.visible  # <= 'visible' is attr on Widget class
            await self.post_message(messages.Layout(self))

    async def on_load(self, event: events.Load) -> None:
        # Populate footer with quit and toggle info
        await self.bind("u", "toggle_tree('unmarked')", "Toggle Unmarked  ⁞")
        await self.bind("1", "toggle_tree('summary')", "Toggle Summary  ⁞")
        await self.bind("f", "toggle_tree('fail_tree')", "Toggle Fail  ⁞")
        await self.bind("p", "toggle_tree('pass_tree')", "Toggle Pass  ⁞")
        await self.bind("e", "toggle_tree('error_tree')", "Toggle Error  ⁞")
        await self.bind("f", "toggle_tree('skip_tree')", "Toggle Skipped  ⁞")
        await self.bind("p", "toggle_tree('xpass_tree')", "Toggle Xpass  ⁞")
        await self.bind("e", "toggle_tree('xfail_tree')", "Toggle Xfail  ⁞")
        await self.bind(
            "a",
            "toggle_tree(['unmarked', 'summary', 'error_tree', 'pass_tree', 'fail_tree', 'skip_tree', 'xpass_tree', 'xfail_tree'])",
            "Toggle All  ⁞",
        )
        await self.bind("q", "quit", "Quit")

        # Get test result sections
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )
        self.unmarked_output = self.test_results.unmarked_output
        self.marked_output = self.test_results.marked_output

    async def on_mount(self) -> None:
        # Create and dock header and footer widgets
        self.title = self.summary_results
        header1 = Header(style="bold white on black")
        header1.title = self.summary_results
        await self.view.dock(header1, edge="top", size=1)
        footer = FoldFooter()
        await self.view.dock(footer, edge="bottom")

        # Stylize the results-tree section headers
        self.unmarked = TreeControl(
            Text("Full Output", style="dark_slate_gray2 underline"),
            {"results": self.test_results.unmarked_output},
            name="unmarked",
        )
        self.summary = TreeControl(
            Text("Summary", style="bold white underline"),
            {"results": self.test_results.Sections['TEST_SESSION_STARTS'].content},
            name="summary",
        )
        self.fail_tree = TreeControl(
            Text("Failures:", style="bold red underline"), {}, name="fail_tree"
        )
        self.pass_tree = TreeControl(
            Text("Passes:", style="bold green underline"), {}, name="pass_tree"
        )
        self.error_tree = TreeControl(
            Text("Errors:", style="bold magenta underline"), {}, name="error_tree"
        )
        self.skip_tree = TreeControl(
            Text("Skips:", style="bold red underline"), {}, name="skip_tree"
        )
        self.xpass_tree = TreeControl(
            Text("Xpasses:", style="bold green underline"), {}, name="xpass_tree"
        )
        self.xfail_tree = TreeControl(
            Text("Xfails:", style="bold magenta underline"), {}, name="xfail_tree"
        )

        for failed in self.test_results.tests_failures:
            await self.fail_tree.add(
                self.fail_tree.root.id,
                Text(failed),
                {"results": self.test_results.tests_failures},
            )
        for errored in self.test_results.tests_errors:
            await self.error_tree.add(
                self.error_tree.root.id,
                Text(errored),
                {"results": self.test_results.tests_errors},
            )
        for passed in self.test_results.tests_passes:
            await self.pass_tree.add(
                self.pass_tree.root.id,
                Text(passed),
                {"results": self.test_results.tests_passes},
            )
        for skipped in self.test_results.tests_skipped:
            await self.skip_tree.add(
                self.skip_tree.root.id,
                Text(skipped),
                {"results": self.test_results.tests_skipped},
            )
        for xpassed in self.test_results.tests_xpasses:
            await self.xpass_tree.add(
                self.xpass_tree.root.id,
                Text(xpassed),
                {"results": self.test_results.tests_xpasses},
            )
        for xfailed in self.test_results.tests_xfails:
            await self.xfail_tree.add(
                self.xfail_tree.root.id,
                Text(xfailed),
                {"results": self.test_results.tests_xfails},
            )

        await self.unmarked.root.expand()
        await self.summary.root.expand()
        await self.fail_tree.root.expand()
        await self.pass_tree.root.expand()
        await self.error_tree.root.expand()
        await self.skip_tree.root.expand()
        await self.xpass_tree.root.expand()
        await self.xfail_tree.root.expand()

        # Create and dock the results tree
        await self.view.dock(
            ScrollView(self.unmarked),
            edge="top",
            size=len(self.unmarked.nodes) + 2,
            # edge="left",
            # size = 25,
            name="unmarked",
        )
        await self.view.dock(
            ScrollView(self.summary),
            edge="top",
            size=len(self.summary.nodes) + 2,
            # edge="left",
            # size = 25,
            name="summary",
        )
        await self.view.dock(
            ScrollView(self.pass_tree),
            edge="top",
            size=len(self.pass_tree.nodes) + 2,
            # edge="left",
            # size = 25,
            name="pass_tree",
        )
        await self.view.dock(
            ScrollView(self.fail_tree),
            edge="top",
            size=len(self.fail_tree.nodes) + 2,
            # edge="left",
            # size = 25,
            name="fail_tree",
        )
        await self.view.dock(
            ScrollView(self.error_tree),
            edge="top",
            size=len(self.error_tree.nodes) + 2,
            # edge="left",
            # size = 25,
            name="error_tree",
        )
        await self.view.dock(
            ScrollView(self.skip_tree),
            edge="top",
            size=len(self.skip_tree.nodes) + 2,
            # edge="left",
            # size = 25,
            name="skip_tree",
        )
        await self.view.dock(
            ScrollView(self.xfail_tree),
            edge="top",
            size=len(self.xfail_tree.nodes) + 2,
            # edge="left",
            # size = 25,
            name="xfail_tree",
        )
        await self.view.dock(
            ScrollView(self.xpass_tree),
            edge="top",
            size=len(self.xpass_tree.nodes) + 2,
            # edge="left",
            # size = 25,
            name="xpass_tree",
        )

        self.dockview = DockView()
        self.gridview = GridView()
        await self.view.dock(self.dockview)

        # Create and dock the test result ('body') view
        self.body = ScrollView()
        self.body.border = 1
        self.body.border_style = "green"
        await self.dockview.dock(self.body, edge="right")

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        label = message.node.label.plain

        # Click the category headers to toggle on/off (future;
        # right now, just ignore those clicks)
        if label in ("Failures:", "Passes:", "Errors:", "Skipped:", "Xpasses:", "Xfails:"):
            return

        # Display results when test name is clicked
        if "Full Output" in label or "Summary" in label:
            self.text = message.node.data.get("results")
        else:
            self.text = message.node.data.get("results")[label]

        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    app = FoldApp()
    app.run()


if __name__ == "__main__":
    main()
