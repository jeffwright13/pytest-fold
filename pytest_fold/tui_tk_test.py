import TermTk as ttk

summary_results = "test \033[42;1;30mANSI\033[44;1;33m TTkString"


def main():
    root = ttk.TTk(layout=ttk.TTkGridLayout())

    # I don't define the parent now because I will add the widget to
    # the "root" grid layout later in order to place it in the proper grid position
    top_frame = ttk.TTkFrame(border=True, layout=ttk.TTkHBoxLayout())

    top_label = ttk.TTkLabel(parent=top_frame)
    top_label.setText(ttk.TTkString(summary_results))

    # It is ok to add the button inside a frame,
    # but you can also place the button straight to the grid
    button_frame = ttk.TTkFrame(
        border=True,
        layout=ttk.TTkVBoxLayout(),
    )
    quit_button = ttk.TTkButton(parent=button_frame, text="Quit", maxWidth=6)
    # the root object has a quit method you can use
    quit_button.clicked.connect(root.quit)

    # As example this button i am going to attach this button straight to the grid
    quit_button_2 = ttk.TTkButton(text="Quit2", maxWidth=7, border=True)
    quit_button_2.clicked.connect(root.quit)

    # This frame is just to mimic your layout
    bottom_frame = ttk.TTkFrame(border=True, title="Bottom Frame")

    # root grid layout
    #   ┌─────────────┬──────┬───────┐
    #   │ 0,0         │0,1   │0,2    │
    #   ├─────────────┴──────┴───────┤
    #   │ gridpos = 1,0              │
    #   │ colspan=3                  │
    #   │ rowspan=1                  │
    #   └────────────────────────────┘

    root.layout().addWidget(top_frame, 0, 0)
    root.layout().addWidget(button_frame, 0, 1)
    root.layout().addWidget(quit_button_2, 0, 2)
    root.layout().addWidget(bottom_frame, 1, 0, 1, 3)  # colspan = 1, rowspan = 3

    root.mainloop()


if __name__ == "__main__":
    main()
