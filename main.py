import tkinter as tk
from board import Board
from gui import FlowGUI

if __name__ == "__main__":

    grid = [
        ['R', '.', '.', '.', 'B'], 
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['R', '.', '.', '.', 'B']
    ]

    board = Board(grid)

    root = tk.Tk()

    app = FlowGUI(root, board)

    root.mainloop()