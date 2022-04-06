from os import get_terminal_size
from pytest_fold.utils import OUTCOMES, Results

import platform
import subprocess
import sys
import TermTk as ttk

from time import sleep

TERMINAL_SIZE = get_terminal_size()


class TkTui:
    def __init__(self) -> None:
        self.test_results = Results()
        self.summary_results = self.test_results.Sections["LAST_LINE"].content.replace(
            "=", ""
        )

        # Create root TTk object
        self.root = ttk.TTk()

    def create_top_frame(self) -> None:
        self.top_frame = ttk.TTkFrame(
            parent=self.root,
            pos=(0, 0),
            size=(TERMINAL_SIZE.columns - 10, 3),
            border=True,
            layout=ttk.TTkHBoxLayout(),
        )
        self.top_label = ttk.TTkLabel(
            parent=self.top_frame, pos=(0, 0)  # , size=(TERMINAL_SIZE.columns - 10, 3)
        )
        self.top_label.setText(ttk.TTkString(self.summary_results))
        # top_label.setText(summary_results)

    def quit(self) -> None:
        # Quits app and restores terminal for Windows, Mac, Linux
        ttk.TTkTimer.quitAll()
        if platform.system() == "Windows":
            subprocess.Popen("cls", shell=True).communicate()
        else:  # Linux and Mac
            print("\033c", end="")
        sys.exit()

    def create_quit_button(self) -> None:
        self.quit_button_frame = ttk.TTkFrame(
            parent=self.root,
            pos=(TERMINAL_SIZE.columns - 10, 0),
            size=(10, 3),
            border=False,
            layout=ttk.TTkVBoxLayout(),
        )
        # self.quit_button_frame.setPadding(0,0,0,0)
        self.quit_button = ttk.TTkButton(
            parent=self.quit_button_frame, text="Quit", border=True
        )
        self.quit_button.layout()
        self.quit_button.clicked.connect(self.quit)

    def create_main_frame(self):
        # Main frame to hold tab and text widgets
        self.main_frame = ttk.TTkFrame(
            parent=self.root,
            pos=(0, 3),
            size=(TERMINAL_SIZE.columns, TERMINAL_SIZE.lines - 3),
            border=False,
            layout=ttk.TTkVBoxLayout(),
        )

    def create_section_tabs(self) -> None:
        # Create tabs with results from individual sections
        self.tab_widget = ttk.TTkTabWidget(
            parent=self.main_frame, border=False, height=4
        )
        self.tab_widget.setPadding(3, 0, 0, 0)

        text = (
            self.test_results.Sections["TEST_SESSION_STARTS"].content
            + self.test_results.Sections["SHORT_TEST_SUMMARY"].content
            + "\n"
            + self.test_results.Sections["LAST_LINE"].content
        )
        tab_label = "Summary"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        # text_area.lineWrapMode == TTkK.WidgetWidth
        text_area.setText(text)
        text_areas = {tab_label: text_area}
        self.tab_widget.addTab(text_area, f" {tab_label} ")

        text = self.test_results.unmarked_output
        tab_label = "Full Output"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_areas[tab_label] = text_area
        text_area.setText(text)
        self.tab_widget.addTab(text_area, f" {tab_label}")

        text = self.test_results.Sections["PASSES_SECTION"].content
        tab_label = "Passes Section"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_area.setText(text)
        text_areas[tab_label] = text_area
        self.tab_widget.addTab(text_area, f" {tab_label}")

        text = self.test_results.Sections["FAILURES_SECTION"].content
        tab_label = "Failures Section"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_area.setText(text)
        text_areas[tab_label] = text_area
        self.tab_widget.addTab(text_area, f" {tab_label}")

        text = self.test_results.Sections["ERRORS_SECTION"].content
        tab_label = "Errors Section"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_area.setText(text)
        text_areas[tab_label] = text_area
        self.tab_widget.addTab(text_area, f" {tab_label} ")

        text = self.test_results.Sections["WARNINGS_SUMMARY"].content
        tab_label = "Warnings"
        text_area = ttk.TTkTextEdit(parent=self.tab_widget)
        text_area.setText(text)
        text_areas[tab_label] = text_area
        self.tab_widget.addTab(text_area, f" {tab_label} ")

    def create_log_tab(self) -> None:
        # Create tab with TTkLog widget to log clicks from test tabs
        tab_label = "Click Log"
        log_viewer = ttk.TTkLogViewer()
        self.tab_widget.addTab(log_viewer, f" {tab_label} ")

    def create_test_result_tabs(self) -> None:
        # Create tabs with results from individual sections
        @ttk.pyTTkSlot(str)
        def callback1(test_name: str) -> None:
            ttk.TTkLog.info(f"Clicked test: {test_name}")
            result = self.test_results.tests_all[test_name]
            ttk.TTkLog.info(result)

        @ttk.pyTTkSlot(ttk.TTkWidget)
        def callback2(item: ttk.TTkWidget) -> None:
            item._visible = False
            sleep(1)
            item._visible = True

        for outcome in OUTCOMES:
            tab_label = outcome
            results_list = ttk.TTkList(
                selectionMode=ttk.TTkK.MultiSelection,
            )
            for result in eval(f"self.test_results.tests_{outcome.lower()}"):
                results_list.addItem(result)
                results_list.textClicked.connect(callback1)
                results_list.itemClicked.connect(callback2)
            self.tab_widget.addTab(results_list, f" {tab_label} ")


def main():
    tui = TkTui()

    tui.create_top_frame()
    tui.create_quit_button()
    tui.create_main_frame()
    tui.create_section_tabs()
    tui.create_log_tab()
    tui.create_test_result_tabs()

    tui.root.mainloop()


if __name__ == "__main__":
    main()
