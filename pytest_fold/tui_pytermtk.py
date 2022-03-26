import platform
import subprocess
import sys
import TermTk as ttk
from TermTk.TTkCore.constant import TTkK
from os import get_terminal_size
from pytest_fold.utils import Results

TERMINAL_SIZE = get_terminal_size()


class TkTui:
    def __init__(self):
        # Retrieve pytest results and extract summary results
        self.test_results = Results()
        self.summary_results = (
            self.test_results._marked_output.get_section("LAST_LINE")[
                "content"
            ].replace("=", "")
            # .rstrip("\n")
        )
        # Create root TTk object
        self.root = ttk.TTk()

    def create_main_frame(self):
        self.top_frame = ttk.TTkFrame(
            parent=self.root,
            pos=(0, 0),
            size=(TERMINAL_SIZE.columns - 10, 3),
            border=True,
            # layout=ttk.TTkLayout(),
        )
        self.top_label = ttk.TTkLabel(
            parent=self.top_frame, pos=(0, 0)  # , size=(TERMINAL_SIZE.columns - 10, 3)
        )
        self.top_label.setText(ttk.TTkString(self.summary_results))
        # top_label.setText(summary_results)

    def quit(self):
        # Quits app and resstores terminal for Windows, Mac, Linux
        ttk.TTkTimer.quitAll()
        if platform.system() == "Windows":
            subprocess.Popen("cls", shell=True).communicate()
        else:  # Linux and Mac
            print("\033c", end="")
        sys.exit()

    def create_quit_button(self):
        self.quit_button_frame = ttk.TTkFrame(
            parent=self.root,
            pos=(TERMINAL_SIZE.columns - 10, 0),
            size=(10, 3),
            border=True,
            layout=ttk.TTkVBoxLayout(),
        )
        self.quit_button = ttk.TTkButton(parent=self.quit_button_frame, text="Quit")
        self.quit_button.layout()
        self.quit_button.clicked.connect(self.quit)

    def create_main_window(self):
        # Main frame to hold tab and text widgets
        self.main_win = ttk.TTkFrame(
            parent=self.root,
            pos=(0, 3),
            size=(TERMINAL_SIZE.columns, TERMINAL_SIZE.lines - 3),
            border=True,
            layout=ttk.TTkVBoxLayout(),
        )

    def create_tabs(self):
        # Create tabs with results from individual sections
        tab_widget = ttk.TTkTabWidget(parent=self.main_win, border=True, height=4)

        text = (
            self.test_results._marked_output.get_section("TEST_SESSION_STARTS")[
                "content"
            ]
            + self.test_results._marked_output.get_section("SHORT_TEST_SUMMARY")[
                "content"
            ]
            + "\n"
            + self.test_results._marked_output.get_section("LAST_LINE")["content"]
        )
        value = "Session Summary"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        # text_area.lineWrapMode == TTkK.WidgetWidth
        text_area.setText(text)
        text_areas = {value: text_area}
        tab_widget.addTab(text_area, f"  {value}  ")

        text = "" + "\n".join(self.test_results.passes.keys()) + "\n"
        text += self.test_results._marked_output.get_section("PASSES_SECTION")[
            "content"
        ]
        value = "Pass"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        text_areas[value] = text_area
        tab_widget.addTab(text_area, f"  {value}  ")

        text = "" + "\n".join(self.test_results.failures.keys()) + "\n"
        text += self.test_results._marked_output.get_section("FAILURES_SECTION")[
            "content"
        ]
        value = "Fail"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        text_areas[value] = text_area
        tab_widget.addTab(text_area, f"  {value}  ")

        text = "" + "\n".join(self.test_results.errors.keys())
        value = "Error"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        text_areas[value] = text_area
        tab_widget.addTab(text_area, f"  {value}  ")

        text = self.test_results._marked_output.get_section("WARNINGS_SUMMARY")[
            "content"
        ]
        value = "Warning"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        text_areas[value] = text_area
        tab_widget.addTab(text_area, f"  {value}  ")

        text = "" + "\n".join(self.test_results.xpasses.keys())
        value = "Xpass"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        text_areas[value] = text_area
        tab_widget.addTab(text_area, f"  {value}  ")

        text = "" + "\n".join(self.test_results.xfails.keys())
        value = "Xfail"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        text_areas[value] = text_area
        tab_widget.addTab(text_area, f"  {value}  ")

        text = "" + "\n".join(self.test_results.skipped.keys())
        value = "Skipped"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        text_areas[value] = text_area
        tab_widget.addTab(text_area, f"  {value}  ")

        text = self.test_results._unmarked_output
        value = "Raw Output"
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_areas[value] = text_area
        text_area.setText(text)
        tab_widget.addTab(text_area, f"  {value}  ")


def main():
    tui = TkTui()

    tui.create_main_frame()
    tui.create_quit_button()
    tui.create_main_window()
    tui.create_tabs()

    tui.root.mainloop()


if __name__ == "__main__":
    main()
