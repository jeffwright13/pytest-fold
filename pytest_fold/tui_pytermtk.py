import platform
import subprocess
import sys
import TermTk as ttk
from os import get_terminal_size
from pytest_fold.utils import Results, MarkedSections, SECTIONS

TERMINAL_SIZE = get_terminal_size()


def quit():
    ttk.TTkTimer.quitAll()
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:  # Linux and Mac
        print("\033c", end="")
    sys.exit()


def name_section(section):
    words = []
    for word in section.split("_"):
        word.lower().capitalize()
        words.append(word)
    return " ".join(words)


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
        layout=ttk.TTkGridLayout(),
    )

    # Create tabs with individual section results
    tab_widget = ttk.TTkTabWidget(parent=main_win, border=True, height=4)
    OUTPUT_SECTIONS = {k: name_section(k) for k in SECTIONS}
    for key, value in OUTPUT_SECTIONS.items():
        if key in ("LAST_LINE", "SHORT_TEST_SUMMARY"):
            continue  # combine these two into one tab
        text = test_results._marked_output.get_section(key)["content"]
        text_area = ttk.TTkTextEdit(parent=tab_widget)
        text_area.setText(text)
        tab_widget.addTab(text_area, f"  {value}  ")

    # Create tab for combined test summary and final results
    text = (
        test_results._marked_output.get_section("SHORT_TEST_SUMMARY")["content"]
        + test_results._marked_output.get_section("LAST_LINE")["content"]
    )
    value = "TEST SUMMARY"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    # Create tab for raw output
    text = test_results._unmarked_output
    value = "RAW OUTPUT"
    text_area = ttk.TTkTextEdit(parent=tab_widget)
    text_area.setText(text)
    tab_widget.addTab(text_area, f"  {value}  ")

    root.mainloop()


if __name__ == "__main__":
    main()

    # # Create main window
    # main_win = ttk.TTkFrame(
    #     parent=root,
    #     pos=(0, 0),
    #     size=(TERMINAL_SIZE.columns, TERMINAL_SIZE.lines),
    #     border=True,
    #     layout=ttk.TTkGridLayout(),
    # )
    # main_label = ttk.TTkLabel(
    #     parent=main_win,
    #     pos=(0, 0),
    #     size=(TERMINAL_SIZE.columns-10, 1),
    #     border=True,
    # )
    # main_label.setText(summary_results)

    # Create main window
    # main_win = ttk.TTkWindow(
    #     parent=root,
    #     pos=(0, 0),
    #     size=(TERMINAL_SIZE.columns, TERMINAL_SIZE.lines),
    #     title=summary_results,
    #     border=True,
    #     layout=ttk.TTkGridLayout(),
    # )

    # Create main window
    # main_win = ttk.TTkWindow(
    #     parent=root,
    #     pos=(0, 0),
    #     size=(TERMINAL_SIZE.columns, 3),
    #     title=summary_results,
    #     border=True,
    #     layout=ttk.TTkGridLayout(),
    # )
    # main_frame = ttk.TTkFrame(
    #     parent=root,
    #     pos=(0, 2),
    #     size=(TERMINAL_SIZE.columns, TERMINAL_SIZE.lines - 2),
    #     border=True,
    #     layout=ttk.TTkGridLayout(),
    # )
