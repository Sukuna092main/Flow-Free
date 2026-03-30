import tkinter as tk
from tkinter import simpledialog

from board import Board
from gui import FlowGUI


def create_empty_grid(size):
    return [["." for _ in range(size)] for _ in range(size)]


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    size = simpledialog.askinteger(
        "Board Size",
        "Nhập kích thước n để tạo board n x n:",
        minvalue=2,
        initialvalue=6,
        parent=root,
    )

    if size is None:
        root.destroy()
        raise SystemExit

    board = Board(create_empty_grid(size))

    root.deiconify()
    app = FlowGUI(root, board)

    root.mainloop()
