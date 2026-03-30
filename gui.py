import colorsys
import tkinter as tk
from tkinter import messagebox

from board import Board
from sat_solver import SATSolver
from solve import Solver


class FlowGUI:
    def __init__(self, root, board):
        self.root = root
        self.size = board.n
        self.edit_grid = board.copy_grid()
        self.board = Board(self.edit_grid)
        self.solution_segments = {}
        self.canvas_size = 500
        self.color_map = self.build_color_map()

        self.root.title("Flow Puzzle")
        self.root.resizable(False, False)

        self.controls = tk.Frame(root)
        self.controls.pack(padx=12, pady=(12, 8), fill="x")

        self.color_label = tk.Label(self.controls, text="Màu:")
        self.color_label.pack(side="left")

        self.color_entry = tk.Entry(self.controls, width=14)
        self.color_entry.pack(side="left", padx=(6, 10))
        self.color_entry.insert(0, "red")

        self.solve_button = tk.Button(self.controls, text="Solve", command=self.solve)
        self.solve_button.pack(side="left")

        self.solve_sat_button = tk.Button(
            self.controls,
            text="Solve SAT",
            command=self.solve_sat,
        )
        self.solve_sat_button.pack(side="left", padx=(6, 0))

        self.reset_button = tk.Button(
            self.controls,
            text="Reset Path",
            command=self.reset_to_endpoints,
        )
        self.reset_button.pack(side="left", padx=6)

        self.clear_button = tk.Button(
            self.controls,
            text="Clear Board",
            command=self.clear_board,
        )
        self.clear_button.pack(side="left")

        self.help_label = tk.Label(
            root,
            text="Nhập tên màu rồi nhấn lên 2 ô để đặt endpoint. Click lại cùng màu để xóa endpoint.",
            anchor="w",
        )
        self.help_label.pack(padx=12, fill="x")

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(padx=12, pady=(8, 12))
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def handle_click(self, event):
        cell_size = self.canvas_size / self.size
        row = int(event.y // cell_size)
        col = int(event.x // cell_size)

        if not (0 <= row < self.size and 0 <= col < self.size):
            return

        color = self.color_entry.get().strip()

        if not color:
            messagebox.showwarning("Màu", "Hãy nhập tên màu trước khi đặt ô.")
            return

        current = self.edit_grid[row][col]

        if current == color:
            self.edit_grid[row][col] = "."
        else:
            count = self.count_endpoints(color)

            if count >= 2:
                messagebox.showwarning(
                    "Màu",
                    f"Màu '{color}' đã có 2 endpoint. Hãy xóa 1 ô trước khi đặt thêm.",
                )
                return

            self.edit_grid[row][col] = color

        self.sync_board()

    def solve(self):
        self.solve_with(Solver, "DFS")

    def solve_sat(self):
        self.solve_with(SATSolver, "SAT")

    def solve_with(self, solver_class, solver_name):
        issue = self.validate_input()

        if issue is not None:
            messagebox.showwarning("Board", issue)
            return

        board = Board(self.copy_grid(self.edit_grid))
        solver = solver_class(board)
        solved = solver.solve()
        self.board = board
        self.solution_segments = getattr(solver, "solution_segments", {}) if solved else {}
        self.draw_board()

        if solved:
            messagebox.showinfo("Solve", f"Đã tìm thấy lời giải bằng {solver_name}.")
        else:
            messagebox.showwarning(
                "Solve",
                f"Board hiện tại không có lời giải bằng {solver_name}.",
            )

    def reset_to_endpoints(self):
        self.sync_board()

    def clear_board(self):
        self.edit_grid = [["." for _ in range(self.size)] for _ in range(self.size)]
        self.sync_board()

    def sync_board(self):
        self.board = Board(self.copy_grid(self.edit_grid))
        self.solution_segments = {}
        self.color_map = self.build_color_map()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = self.canvas_size / self.size
        line_width = max(6, int(cell_size * 0.28))
        endpoint_radius = cell_size * 0.24
        font_size = max(8, int(cell_size * 0.18))

        for r in range(self.size):
            for c in range(self.size):
                label = self.board.grid[r][c]

                x1 = c * cell_size
                y1 = r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self.cell_fill(label),
                    outline="#2c2c2c",
                    width=1,
                )

        for label, segments in self.solution_segments.items():
            for start, end in segments:
                self.draw_path_segment(start, end, label, cell_size, line_width)

        for r in range(self.size):
            for c in range(self.size):
                endpoint_label = self.edit_grid[r][c]

                if endpoint_label == ".":
                    continue

                self.draw_endpoint(
                    r,
                    c,
                    endpoint_label,
                    cell_size,
                    endpoint_radius,
                    font_size,
                )

    def validate_input(self):
        if not self.board.pairs:
            return "Board đang trống. Hãy đặt các endpoint trước khi solve."

        invalid = []

        for color, cells in sorted(self.board.pairs.items()):
            if len(cells) != 2:
                invalid.append(f"{color} ({len(cells)} o)")

        if invalid:
            return "Mỗi màu phải có dùng 2 endpoint: " + ", ".join(invalid)

        return None

    def count_endpoints(self, color):
        total = 0

        for row in self.edit_grid:
            for value in row:
                if value == color:
                    total += 1

        return total

    def build_color_map(self):
        color_map = {".": "white"}
        labels = sorted(self.board.pairs.keys())

        for index, label in enumerate(labels):
            color_map[label] = self.resolve_color(label, index, len(labels))

        return color_map

    def resolve_color(self, label, index, total):
        try:
            self.root.winfo_rgb(label)
            return label
        except tk.TclError:
            hue = index / max(1, total)
            red, green, blue = colorsys.hsv_to_rgb(hue, 0.65, 0.95)
            return self.rgb_to_hex(red, green, blue)

    def rgb_to_hex(self, red, green, blue):
        return "#{:02x}{:02x}{:02x}".format(
            int(red * 255),
            int(green * 255),
            int(blue * 255),
        )

    def cell_fill(self, label):
        if label == ".":
            return "#fafafa"

        return self.mix_with_white(self.color_map[label], 0.75)

    def draw_path_segment(self, start, end, label, cell_size, line_width):
        row, col = start
        nr, nc = end
        cx = col * cell_size + cell_size / 2
        cy = row * cell_size + cell_size / 2
        nx = nc * cell_size + cell_size / 2
        ny = nr * cell_size + cell_size / 2
        path_color = self.color_map[label]

        self.canvas.create_line(
            cx,
            cy,
            nx,
            ny,
            fill=path_color,
            width=line_width,
            capstyle=tk.ROUND,
        )

    def draw_endpoint(self, row, col, label, cell_size, endpoint_radius, font_size):
        cx = col * cell_size + cell_size / 2
        cy = row * cell_size + cell_size / 2
        endpoint_color = self.color_map[label]
        outline_color = self.mix_with_black(endpoint_color, 0.35)

        self.canvas.create_oval(
            cx - endpoint_radius,
            cy - endpoint_radius,
            cx + endpoint_radius,
            cy + endpoint_radius,
            fill=endpoint_color,
            outline=outline_color,
            width=max(2, int(cell_size * 0.05)),
        )

        self.canvas.create_text(
            cx,
            cy,
            text=self.endpoint_text(label),
            fill=self.text_color(endpoint_color),
            font=("Arial", font_size, "bold"),
        )

    def endpoint_text(self, label):
        short = str(label).strip()

        if len(short) <= 3:
            return short

        return short[:2].upper()

    def text_color(self, color):
        red, green, blue = self.root.winfo_rgb(color)
        luminance = (
            0.2126 * (red / 65535)
            + 0.7152 * (green / 65535)
            + 0.0722 * (blue / 65535)
        )
        return "#111111" if luminance > 0.6 else "white"

    def mix_with_white(self, color, ratio):
        red, green, blue = self.root.winfo_rgb(color)
        return self.rgb_to_hex(
            (red / 65535) * (1 - ratio) + ratio,
            (green / 65535) * (1 - ratio) + ratio,
            (blue / 65535) * (1 - ratio) + ratio,
        )

    def mix_with_black(self, color, ratio):
        red, green, blue = self.root.winfo_rgb(color)
        return self.rgb_to_hex(
            (red / 65535) * (1 - ratio),
            (green / 65535) * (1 - ratio),
            (blue / 65535) * (1 - ratio),
        )

    def copy_grid(self, grid):
        return [row[:] for row in grid]
