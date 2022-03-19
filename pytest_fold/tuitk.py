import TermTk as ttk
from os import get_terminal_size
from rich.text import Text
from pytest_fold.utils import Results, MarkedSections
import faker
OUTPUT_SECTIONS = {
    "START": "Session Start",
    "ERR": "Errors",
    "WARN": "Warnings",
    "PASS": "Pass",
    "FAIL": "Fail",
    "MISC": "Misc",
    "FINAL": "Final Summary",
    "RAW": "Raw_Out",
}

TEXT = faker.Faker().text(900)

def main():
    root = ttk.TTk()
    term_size = get_terminal_size()

    test_results = Results()
    unmarked_output = test_results._unmarked_output
    marked_sections = MarkedSections()
    summary_text = (
        Text.from_ansi(marked_sections.get_section("LASTLINE")["content"])
        .markup.replace("=", "")
        .strip()
    )

    main_window = ttk.TTkWindow(
        parent=root,
        pos=(0, 0),
        size=(term_size.columns, term_size.lines),
        title=marked_sections.get_section("LASTLINE")["content"].replace("=", ""),
        border=True,
    )
    main_layout = ttk.TTkHBoxLayout()
    main_window.setLayout(main_layout)

    tab_widget = ttk.TTkTabWidget(parent=main_window)
    for section in OUTPUT_SECTIONS:
        if section in ["START", "FINAL", "RAW"]:
            # scroller = ttk.TTkScrollArea(border=False, title=section)
            text_edit = ttk.TTkTextEdit(parent=tab_widget, text=TEXT)
            # t,_,l,_ = scroller.getPadding()
            tab_widget.addTab(text_edit, f"  {section}  ")
        else:
            tab_widget.addTab(ttk.TTkTree(border=False, title=section), f"  {section}  ")

    root.mainloop()


if __name__ == "__main__":
    main()
