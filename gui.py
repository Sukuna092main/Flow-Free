import tkinter as tk
from solve import Solver

class FlowGUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.size = board.n

        self.root.title("Flow Puzzle")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.solve_button = tk.Button(root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=10)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 400 // self.size

        for r in range(self.size):
            for c in range(self.size):
                color = self.board.grid[r][c]

                x1 = c * cell_size
                y1 = r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_map.get(color, "white"),
    outline="black")


    def solve(self):
        solver = Solver(self.board)
        solver.solve()
        self.draw_board()

    def update_board(self):
        self.draw_board()
        self.root.update()

color_map = {
    'R' : "red",
    'G' : "green",
    'B' : "blue",
    '.': "white"
 }  

 
