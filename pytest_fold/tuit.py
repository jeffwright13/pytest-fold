from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.views import DockView
from textual.widgets import Header, Footer, TreeControl, ScrollView, TreeClick
from pytest_fold.utils import Results

TREE_WIDTH = 30
SECTIONS = {
    "FIRSTLINE": "bold blue underline",
    "FAILURES": "bold red underline",
    "ERRORS": "bold magenta underline",
    "WARNINGS_SUMMARY": "bold yellow underline",
    "TERMINAL_SUMMARY": "bold green underline",
    "LASTLINE": "bold blue underline",
}


class FoldApp(App):
    async def on_load(self, event: events.Load) -> None:
        # Load results from OUTFILE; bind actions to heaader/footer widgets
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )
        self.unmarked_output = self.test_results.unmarked_output
        self.marked_output = self.test_results.marked_output
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", f"Quit        {self.summary_results}")

    async def on_mount(self) -> None:
        # Create and dock header and footer widgets
        # header = Header(tall=False)
        # header.title = "bar"
        # footer = Footer()
        # footer.title = "Woof!"
        # await self.view.dock(header, edge="top", size=1)
        # await self.view.dock(footer, edge="bottom")
        header1 = Header(style="bold white on black")
        header1.title = self.summary_results
        await self.view.dock(header1, edge="top", size=1)
        footer = Footer()
        await self.view.dock(footer, edge="bottom")

        # Stylize the results tree section headers
        # tree = TreeControl("SESSION RESULTS:", {})
        # for results_key in self.results.keys():
        #     await tree.add(tree.root.id, Text(results_key), {"results": self.results})
        #     for k, v in SECTIONS.items():
        #         if tree.nodes[tree.id].label.plain == k:
        #             tree.nodes[tree.id].label.stylize(v)
        #         else:
        #             tree.nodes[tree.id].label.stylize("italic")
        # await tree.root.expand()
        tree = TreeControl("SESSION RESULTS:", {})
        for results_key in self.results.keys():
            await tree.add("Fail", Text(results_key), {"results": self.results})
            await tree.add(tree.root.id, Text(results_key), {"results": self.results})
            for k, v in SECTIONS.items():
                if tree.nodes[tree.id].label.plain == k:
                    tree.nodes[tree.id].label.stylize(v)
                else:
                    tree.nodes[tree.id].label.stylize("italic")
        await tree.root.expand()

        # Create and dock the results header tree, and individual results
        self.body = ScrollView()
        self.dock_view = DockView()
        await self.view.dock(
            ScrollView(tree), edge="left", size=TREE_WIDTH, name="sidebar"
        )
        await self.view.dock(self.dock_view)
        await self.dock_view.dock(self.body, edge="top")

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        # Display results in body when section header is clicked
        label = message.node.label
        self.text = message.node.data.get("results")[label._text[0]]
        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    app = FoldApp()
    app.run()


if __name__ == "__main__":
    main()
