# import os, sys

# file_path = "/Users/jwr003/coding/pyTermTk/TermTk"
# sys.path.append(os.path.dirname(file_path))

import faker
import TermTk as ttk

from os import get_terminal_size
from rich import print
from rich.text import Text
from pytest_fold.utils import Results, MarkedSections

TERMINAL_SIZE = get_terminal_size()
OUTPUT_SECTIONS = {
    "FIRSTLINE": "Session Start",
    "ERRORS": "Errors",
    "WARNINGS_SUMMARY": "Warnings",
    "PASS": "Pass",
    "FAIL": "Fail",
    "MISC": "Misc",
    "TERMINAL_SUMMARY": "Final Summary",
    "RAW": "Raw Output",
}


def main():
    test_results = Results()

    root = ttk.TTk()

    top_window = ttk.TTkWindow(
        parent=root,
        pos=(0, 0),
        size=(TERMINAL_SIZE.columns - 10, 3),
        title=test_results._marked_output.get_section("LASTLINE")["content"].replace(
            "=", ""
        ),
        border=False,
    )
    top_window.setLayout(ttk.TTkHBoxLayout())

    main_frame = ttk.TTkFrame(
        parent=root, pos=(0, 3), height=(TERMINAL_SIZE.columns - 10), border=True
    )

    tab_widget = ttk.TTkTabWidget(parent=main_frame, border=False, height=4)
    for key, value in OUTPUT_SECTIONS.items():
        if key in ["FIRSTLINE", "ERRORS", "WARNINGS_SUMMARY"]:
            text = test_results._marked_output.get_section(key)["content"]
            text_edit = ttk.TTkTextEdit(parent=tab_widget)
            text_edit.setText(text)
            tab_widget.addTab(text_edit, f"  {value}  ")
        elif key == "TERMINAL_SUMMARY":
            text = test_results._marked_output.get_section(key)["content"]
            text += test_results._marked_output.get_section("LASTLINE")["content"]
            text_edit = ttk.TTkTextEdit(parent=tab_widget)
            text_edit.setText(text)
            tab_widget.addTab(text_edit, f"  {value}  ")
        elif key == "RAW":
            text = test_results._unmarked_output
            text_edit = ttk.TTkTextEdit(parent=tab_widget)
            text_edit.setText(text)
            tab_widget.addTab(text_edit, f"  {value}  ")
        elif key == "FAIL":
            text = ""
            tests = test_results.failures
            for test in tests:
                text += test
            tab_widget.addTab(text_edit, f"  {value}  ")

    root.mainloop()


if __name__ == "__main__":
    main()
