import faker
import TermTk as ttk
import sys

from os import get_terminal_size
from rich import print
from rich.text import Text
from pytest_fold.utils import Results, MarkedSections

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

TEXT = faker.Faker().text(5000)
TERMINAL_SIZE = get_terminal_size()


def main():
    root = ttk.TTk()

    test_results = Results()
    unmarked_output = test_results._unmarked_output
    marked_sections = test_results._marked_output
    summary_text = (
        Text.from_ansi(marked_sections.get_section("LASTLINE")["content"])
        .markup.replace("=", "")
        .strip()
    )

    # top_window = ttk.TTkWindow(
    #     parent=root,
    #     pos=(0, 0),
    #     size=(TERMINAL_SIZE.columns - 10, 3),
    #     title = "Hi",,
    #     # title = Text.from_ansi(marked_sections.get_section("LASTLINE")["content"])
    #     # title = summary_text.print(),
    #     # title=marked_sections.get_section("LASTLINE")["content"].replace("=", ""),
    #     border=False,
    # )
    # # main_layout = ttk.TTkHBoxLayout()
    # top_window.setLayout(ttk.TTkHBoxLayout())

    results_summary_frame = ttk.TTkFrame(parent=root, pos=(0, 0), size=(TERMINAL_SIZE.columns - 10, 3), border=True)
    results_summary_label = ttk.TTkLabel(parent=results_summary_frame)
    results_summary_label.setText(r"""[31m==================== [31m[1m8 failed[0m, [32m4 passed[0m, [33m2 skipped[0m, [33m2 xfailed[0m, [33m2 xpassed[0m, [31m[1m3 errors[0m[31m in 2.02s[0m[31m ====================[0m""")

    quit_frame = ttk.TTkFrame(parent=root, pos=(TERMINAL_SIZE.columns - 10, 0), size=(10, 3), border=True)
    quit_button = ttk.TTkButton(parent=quit_frame, border=True, height=3)
    quit_button.text = "Hi"

    # main_frame = ttk.TTkFrame(parent=root, pos=(0, 3), height=(TERMINAL_SIZE.columns - 10), border=True)

    # tab_widget = ttk.TTkTabWidget(parent=main_frame, border = False, height=4)
    # for key, value in OUTPUT_SECTIONS.items():
    #     if key in ["FIRSTLINE", "ERRORS", "WARNINGS_SUMMARY"]:
    #         text = marked_sections.get_section(key)["content"]
    #         text_edit = ttk.TTkTextEdit(parent=tab_widget)
    #         text_edit.setText(text)
    #         tab_widget.addTab(text_edit, f"  {value}  ")
    #     elif key == "TERMINAL_SUMMARY":
    #         text = marked_sections.get_section(key)["content"]
    #         text += marked_sections.get_section("LASTLINE")["content"]
    #         text_edit = ttk.TTkTextEdit(parent=tab_widget)
    #         text_edit.setText(text)
    #         tab_widget.addTab(text_edit, f"  {value}  ")
    #     elif key == "RAW":
    #         text = unmarked_output
    #         text_edit = ttk.TTkTextEdit(parent=tab_widget)
    #         text_edit.setText(text)
    #         tab_widget.addTab(text_edit, f"  {value}  ")

    #     else:
    #         tab_widget.addTab(ttk.TTkTree(border=False, title=value), f"  {value}  ")



    root.mainloop()


if __name__ == "__main__":
    main()
