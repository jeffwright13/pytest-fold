import utils

from pathlib import Path

from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, TextBox, Layout, Button, PopUpDialog
from asciimatics.exceptions import ResizeScreenError, StopApplication

RESULTS_FILE = "pytest_fold/console_output.fold"

class ResultsData:
    def __init__(self, path: Path):
        self.results_file = path
        self.sections = []

    def get_results(self):
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = utils.tokenize(results_lines)


class CollapsedResult(Frame):
    def __init__(self, screen: Screen):
        # self.screen = screen
        self.height = 1
        self.width = screen.width

        layout = Layout(1)
        self.add_layout(layout)
        layout.add_widget(TextBox(1))
        layout.add_widget(Button("Quit", self._quit, label="To exit:"), 1)
        self.fix()

    def _quit(self):
        popup = PopUpDialog(
            self._screen,
            "Quit?",
            ["Yes", "No"],
            has_shadow=True,
            on_close=self._quit_on_yes,
        )
        self._scene.add_effect(popup)

    @staticmethod
    def _quit_on_yes(selected):
        if selected == 0:
            raise StopApplication("User requested exit")


def demo(screen):
    scenes = [Scene([CollapsedResult(screen)], duration = -1)]
    # scenes = [Scene([CollapsedResult(screen) for _ in len(sections)], -1)]
    screen.play(scenes, stop_on_resize=True, start_scene=scenes[0], allow_int=True)


def main():
    resultsfile = Path.cwd() / RESULTS_FILE
    resultsdata = ResultsData(resultsfile)

    last_scene = None
    while True:
        try:
            Screen.wrapper(demo)
            quit()
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == "__main__":
    main()
