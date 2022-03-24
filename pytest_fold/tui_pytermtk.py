import platform
import subprocess
import sys
import TermTk as ttk
from os import get_terminal_size
from pytest_fold.utils import Results, MarkedSections, SECTIONS

TERMINAL_SIZE = get_terminal_size()


def quit():
    # Quits app and resstores terminal fo Windows, Mac, Linux
    ttk.TTkTimer.quitAll()
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:  # Linux and Mac
        print("\033c", end="")
    sys.exit()


def main():
    # Retrieve pytest results and extract summary results
    test_results = Results()
    summary_results = (
        test_results._marked_output.get_section("LAST_LINE")["content"].replace("=", "")
        # .rstrip("\n")
    )
    # Create root TTk object
    root = ttk.TTk()

    # Create main window
    top_frame = ttk.TTkFrame(
        parent=root,
        pos=(0, 0),
        size=(TERMINAL_SIZE.columns - 10, 3),
        border=True,
        # layout=ttk.TTkLayout(),
    )
    top_label = ttk.TTkLabel(
        parent=top_frame, pos=(0, 0)  # , size=(TERMINAL_SIZE.columns - 10, 3)
    )
    # top_label.setText(ttk.TTkString(summary_results))
    top_label.setText(summary_results)

    # Create Quit button
    button_frame = ttk.TTkFrame(
        parent=root,
        pos=(TERMINAL_SIZE.columns - 10, 0),
        size=(10, 3),
        border=True,
        layout=ttk.TTkVBoxLayout(),
    )
    quit_button = ttk.TTkButton(parent=button_frame, text="Quit")
    quit_button.layout()
    quit_button.clicked.connect(quit)

    # Main frame to hold tab and text widgets
    main_win = ttk.TTkFrame(
        parent=root,
        pos=(0, 3),
        size=(TERMINAL_SIZE.columns, TERMINAL_SIZE.lines - 3),
        border=True,
        layout=ttk.TTkVBoxLayout(),
    )

    # Create tabs with results from individual sections
    tab_widget = ttk.TTkTabWidget(parent=main_win, border=True, height=4)
    text_area_handles = {}
    for key, value in SECTIONS.items():
        if key in ("SHORT_TEST_SUMMARY", "LAST_LINE"):
            continue  # combine these two into one tab later
        text = test_results._marked_output.get_section(key)["content"]
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area_handles[value] = text_area
        text_area.setText(text)
        tab_widget.addTab(text_area, f"  {value}  ")

    # Create tabs for XPass, XFail, Skipped tests
    text = ""
    text += "\n".join(k for k in test_results.xpasses.keys())
    value = "Xpass"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    text_area_handles[value] = text_area
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    text = ""
    text += "\n".join(k for k in test_results.xfails.keys())
    value = "Xfail"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    text_area_handles[value] = text_area
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    text = ""
    text += "\n".join(k for k in test_results.skipped.keys())
    value = "Skipped"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    text_area_handles[value] = text_area
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    # Create tab for combined test summary and final results
    text = (
        test_results._marked_output.get_section("SHORT_TEST_SUMMARY")["content"]
        + test_results._marked_output.get_section("LAST_LINE")["content"]
    )
    value = "Summary"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    text_area_handles[value] = text_area
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    # Create tab for raw output
    text = test_results._unmarked_output
    value = "Raw Output"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    # text_area_handles[value] = text_area
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    root.mainloop()


if __name__ == "__main__":
    main()
