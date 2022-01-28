from pathlib import Path
from math import ceil
# from utils import tokenize
from plugin import MARKER1, MARKER2
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.event import KeyboardEvent
from asciimatics.parsers import AnsiTerminalParser
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, TextBox, Layout, CheckBox, Button


RESULTS_FILE = (
    "/Users/jwr003/coding/pytest-fold/output_files_to_analyze/outputvvfold.ansi"
)
DEBUG = True


def tokenize(lines: str, marker1: str=MARKER1, marker2: str=MARKER2) -> list[str]:
    sections = []
    section_content = ""
    marker1_seen = False
    for line in lines:
        if not marker1_seen:
            if marker1 in line:
                marker1_seen = True
                sections.append(section_content)
                section_content = ""
                continue
            section_content += line
            continue
        if marker1 in line:
            continue
        if marker2 in line:
            sections.append(section_content)
            section_content = ""
            continue
        section_content += line
    sections.append(section_content)
    return sections


class ResultsData:
    """
    Class to read in results from a 'pytest --fold' session (which inserts markers
    around each failed test), and tokenize the results into individual sections for
    display on the TUI
    """

    def __init__(self, path: Path = RESULTS_FILE) -> None:
        self.results_file = path
        self.sections = []
        self.parsed_sections = []

    def _tokenize_results(self) -> None:
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = tokenize(results_lines)

    def get_results(self) -> list:
        self._tokenize_results()
        return self.sections


class ResultsLayout(Layout):
    """
    This Layout handles both folded and unfolded results. There are two columns:
    1) a checkbox (height:1) to fold/unfold the results textbox
    2) a textbox (height:[1 | N]) to display data; height:1 => "folded" results,
       height:N => "unfolded" results
    """

    def __init__(
        self,
        screen: Screen,
        folded: bool = True,
        textboxheight: int = 4,
        value: str = "No data!",
    ) -> None:
        super(ResultsLayout, self).__init__(columns=[4, screen.width - 6])
        self.textboxheight = textboxheight
        self.value = value
        self.folded = folded
        self.parser = AnsiTerminalParser()

    def add_widgets(self) -> None:
        cb = CheckBox(text="", on_change=self._toggle_checkbox)
        self.add_widget(cb, column=0)
        ht = 1 if self.folded else self.textboxheight
        wrap = not self.folded
        tb = TextBox(
            height=ht,
            line_wrap=wrap,
            readonly=True,
            as_string=True,
            parser=self.parser,
        )
        tb.value = self.value
        self.add_widget(tb, column=1)

    def _toggle_checkbox(self) -> None:
        self.folded = not self.folded
        self.clear_widgets()
        self.add_widgets()
        self._frame.fix()


class QuitterLayout(Layout):
    """
    Layout class to quit the whole application
    """

    def __init__(self, screen: Screen) -> None:
        # 4 to make room for '[ ]' plus a space; -6 to offset from end of line in frame
        super(QuitterLayout, self).__init__(columns=[4, screen.width - 6])

    def add_widgets(self) -> None:
        self.add_widget(Button(text="Quit", on_click=self._quit), 1)

    def _quit(self) -> None:
        raise StopApplication("User requested exit by clicking 'Quit'")


class ResultsFrame(Frame):
    def __init__(self, screen: Screen) -> None:
        super(ResultsFrame, self).__init__(
            screen=screen, height=screen.height, width=screen.width, can_scroll=True
        )

        # Snarf data from results file, tokenize, then add Layout for the resulting
        # sections to the ResultsFrame
        results_data = ResultsData()
        sections = results_data.get_results()

        # First layout section: "header" info from Pytest
        self.add_layout(
            ResultsLayout(
                screen=screen,
                folded=False,
                textboxheight=ceil(len(sections[0]) / screen.width),
                value=sections[0],
            )
        )

        # Individual folded layouts, one per failure section from Pytest run
        for _ in range(1, len(sections) - 1):
            self.add_layout(
                ResultsLayout(
                    screen=screen,
                    folded=True,
                    textboxheight=ceil(len(sections[_]) / screen.width),
                    value=sections[_],
                )
            )

        # Last layout sections: "summary" info from Pytest, plus the quit button
        self.add_layout(
            ResultsLayout(
                screen=screen,
                folded=False,
                textboxheight=ceil(len(sections[-1]) / screen.width),
                value=sections[-1],
            )
        )
        self.add_layout(QuitterLayout(screen))

        # Add widgets to all layouts (needs to be done after layouts are added to frame)
        for layout in self._layouts:
            layout.add_widgets()

        # Set color theme; fix the layouts and calculate locations of all widgets
        self.set_theme("monochrome")
        self.fix()
        print("Stub")


def global_shortcuts(event):
    # Event handler for global keys, used here to quit app with Ctrl keys
    if isinstance(event, KeyboardEvent):
        code = event.key_code
        # Stop on ctrl+q or ctrl+x
        if code in (17, 24):
            raise StopApplication(f"User terminated app with {code}")


def demo(screen: Screen, scene: Scene) -> None:
    scenes = [Scene([ResultsFrame(screen)], duration=-1)]
    screen.play(
        scenes,
        stop_on_resize=True,
        start_scene=scenes[0],
        allow_int=True,
        unhandled_input=global_shortcuts,
    )


def main():
    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            quit()
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
