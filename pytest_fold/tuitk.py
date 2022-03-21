import faker
import TermTk as ttk

from os import get_terminal_size
from pytest_fold.utils import Results, MarkedSections, SECTIONS
from rich import print
from rich.text import Text
from strip_ansi import strip_ansi

TERMINAL_SIZE = get_terminal_size()


def name_section(section):
    words = []
    for word in section.split("_"):
        word.lower().capitalize()
        words.append(word)
    phrase = " ".join(words)
    return phrase


def main():
    # Retrieve pytest results and extract summary results
    test_results = Results()
    summary_results = (
        test_results._marked_output.get_section("LAST_LINE")["content"]
        .replace("=", "")
        .rstrip("\n")
    )
    # h_offset = int((TERMINAL_SIZE.columns - len(strip_ansi(summary_results))) / 2)

    # Create root TTk object
    root = ttk.TTk()

    # Create main window
    main_win = ttk.TTkWindow(
        parent=root,
        pos=(0, 0),
        size=(TERMINAL_SIZE.columns, TERMINAL_SIZE.lines),
        title=summary_results,
        border=True,
        layout=ttk.TTkGridLayout(),
    )

    # Create tabs with individual section results
    tab_widget = ttk.TTkTabWidget(parent=main_win, border=True, height=4)
    OUTPUT_SECTIONS = {k: name_section(k) for k in SECTIONS}
    for key, value in OUTPUT_SECTIONS.items():
        text = test_results._marked_output.get_section(key)["content"]
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        tab_widget.addTab(text_area, f"  {value}  ")

    # Create tabs for raw output, etc.
    text = test_results._unmarked_output
    value = "RAW OUTPUT"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    root.mainloop()


if __name__ == "__main__":
    main()
