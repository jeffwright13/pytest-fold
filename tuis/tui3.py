import utils

from pathlib import Path
from pytermgui import Container, Label, InputField, MarkupFormatter, getch, alt_buffer, boxes

RESULTS_FILE = "pytest_fold/console_output.fold"

class ResultsData:
    def __init__(self, path: Path):
        self.results_file = path
        self.sections = []

    def get_results(self):
        with open(self.results_file, "r") as results_file:
            results_lines = results_file.readlines()
        self.sections = utils.sectionize(results_lines)



class TUI:
    results_data = ResultsData(RESULTS_FILE)
    results_data.get_results()

    border_corner_markup = MarkupFormatter("[60 bold]{item}")
    Container.set_style("border", border_corner_markup)
    Container.set_style("corner", border_corner_markup)
    boxes.SINGLE.set_chars_of(Container)

    root = Container()
    root.forced_width = 78

    boxes.DOUBLE_TOP.set_chars_of(root)
    # root += Label(f"[210 bold]{results_data.sections[0]}", align=Label.ALIGN_LEFT)
    root += Label(f'''{results_data.sections[0]}''')
    root += Label()

    field = InputField("Enter something!")
    field.set_style("value", MarkupFormatter("[italic 72]{item}"))
    field.set_style("cursor", MarkupFormatter("[@72]{item}"))

    field_container = Container(vert_align=Container.VERT_ALIGN_TOP) + field
    field_container.forced_height = 7
    root += field_container

    root += Label("[245 italic]> Press CTRL_C to exit...", align=Label.ALIGN_RIGHT)

    root.focus()

    with alt_buffer(cursor=False):
        root.center()
        root.print()

        while True:
            key = getch(interrupts=False)

            if key == chr(3):
                break

            field.send(key)
            root.center()
            root.print()

    print("Goodbye!")


def main():
    resultsfile = Path.cwd() / RESULTS_FILE
    resultsdata = ResultsData(resultsfile)

    TUI()

if __name__ == "__main__":
    main()
