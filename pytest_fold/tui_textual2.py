from pathlib import Path
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.app import App
from textual.views import DockView
from textual.widgets import Header, Footer, TreeControl, ScrollView, TreeClick
from pytest_fold.utils import Results

TREE_WIDTH = 30


# class ResultsData:
#     """
#     Class to read in results from a 'pytest --fold' session (which inserts markers
#     around each failed test), and sectionize the results into individual sections for
#     display on the TUI. Relies on utils.py.
#     """

#     def __init__(self, path: Path = OUTFILE) -> None:
#         self.results_file = path
#         self.sections = []
#         self.parsed_sections = []

#     def _sectionize_results(self) -> None:
#         with open(self.results_file, "r") as results_file:
#             results_lines = results_file.readlines()
#         self.sections = sectionize(results_lines)

#     def get_results(self) -> list:
#         self._sectionize_results()
#         return self.sections

#     def get_results_dict(self) -> dict:
#         self.results = self.get_results()
#         d = {}
#         for section in self.results:
#             if section["test_title"]:
#                 d[section["test_title"]] = section["content"]
#             else:
#                 d[section["name"]] = section["content"]
#         return d

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

SECTIONS = {
    "FAILURES": "bold red underline",
    "PASSES": "bold green underline",
    "ERRORS": "bold magenta underline",
    "WARNINGS_SUMMARY": "bold yellow underline",
}

class PytestFoldApp(App):
    async def on_load(self, event: events.Load) -> None:
        # Load results from OUTFILE; bind actions to heaader/footer widgets
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )
        self.unmarked_output = self.test_results.unmarked_output
        self.marked_output = self.test_results.marked_output
        await self.bind("b", "view.toggle('sidebar')", "Toggle Tree")
        await self.bind("q", "quit", "Quit")
        await self.bind("~", None, f"{self.summary_results}")

    async def on_mount(self) -> None:
        # Create and dock header and footer widgets
        header = Header(style="bold white on black")
        header.title = self.summary_results
        await self.view.dock(header, edge="top", size=1)

        footer = Footer()
        await self.view.dock(footer, edge="bottom")

        tree = TreeControl("SESSION RESULTS:", {})

        section = "FAILURES"
        section_text = Text(section)
        section_text.stylize(SECTIONS[section])
        await tree.add(tree.root.id, section_text, {"results": self.test_results.tests_failures})
        for testname in self.test_results.tests_failures:
            _test_text = Text(testname)
            _test_text.stylize("italic")
            await tree.add(tree.root.id, _test_text, {})

        section = "PASSES"
        section_text = Text(section)
        section_text.stylize(SECTIONS[section])
        await tree.add(tree.root.id, section_text, {"results": self.test_results.tests_passes})
        for testname in self.test_results.tests_passes:
            _text = Text(testname)
            _text.stylize("italic")
            await tree.add(tree.root.id, _text, {})

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
        # Display results in body when section header is clicked;
        # but don't try processing the section titles
        label = message.node.label
        if label.plain in SECTIONS:
            return

        for section in SECTIONS:
            try:
                test_section = f"tests_{section.lower()}"
                self.text = eval(f"self.test_results.{test_section}[message.node.label.plain]")
            except:
                pass

        text: RenderableType
        text = Text.from_ansi(self.text)
        await self.body.update(text)


def main():
    app = PytestFoldApp()
    app.run()


if __name__ == "__main__":
    main()
