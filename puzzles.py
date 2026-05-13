"""
Predefined Flow Free puzzles for testing and demonstration.
Each puzzle is a 2D grid where '.' means empty and color names are endpoints.
"""

PUZZLES = {
    "5x5 Easy": [
        ["red", ".", ".", ".", "blue"],
        [".", ".", "green", ".", "."],
        [".", ".", ".", ".", "."],
        [".", ".", ".", ".", "."],
        ["blue", ".", "green", ".", "red"],
    ],
    "5x5 Medium": [
        ["red", ".", ".", "blue", "."],
        [".", ".", ".", ".", "green"],
        [".", "yellow", ".", ".", "."],
        [".", ".", ".", "yellow", "."],
        ["green", ".", ".", "red", "blue"],
    ],
    "6x6 Easy": [
        ["red", ".", ".", ".", ".", "blue"],
        [".", ".", ".", ".", ".", "."],
        [".", "green", ".", ".", ".", "."],
        [".", ".", ".", ".", "green", "."],
        [".", ".", ".", ".", ".", "."],
        ["blue", ".", ".", ".", ".", "red"],
    ],
    "6x6 Medium": [
        ["red", ".", "blue", ".", ".", "."],
        [".", ".", ".", ".", "green", "."],
        [".", "yellow", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "orange"],
        [".", "green", ".", "yellow", ".", "."],
        ["orange", ".", ".", ".", "blue", "red"],
    ],
    "7x7 Hard": [
        ["red", ".", ".", "blue", ".", ".", "."],
        [".", ".", ".", ".", ".", "green", "."],
        [".", "yellow", ".", ".", ".", ".", "."],
        [".", ".", ".", "purple", ".", ".", "orange"],
        [".", ".", ".", ".", ".", ".", "."],
        [".", "green", ".", "yellow", ".", "purple", "."],
        ["orange", ".", ".", ".", "blue", ".", "red"],
    ],
    "8x8 Expert": [
        ["red", ".", ".", ".", "blue", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "green", "."],
        [".", "yellow", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", "purple", ".", ".", "."],
        [".", ".", "orange", ".", ".", ".", ".", "cyan"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", "green", ".", "yellow", ".", "purple", ".", "."],
        ["cyan", ".", "orange", ".", ".", "blue", ".", "red"],
    ],
}


def get_puzzle_names():
    """Return list of available puzzle names."""
    return list(PUZZLES.keys())


def get_puzzle(name):
    """Return a deep copy of the puzzle grid."""
    if name not in PUZZLES:
        return None
    return [row[:] for row in PUZZLES[name]]


def grid_to_text(grid):
    """Convert a grid to a saveable text format."""
    lines = []
    for row in grid:
        lines.append(",".join(row))
    return "\n".join(lines)


def text_to_grid(text):
    """Parse a text format back into a grid."""
    lines = text.strip().split("\n")
    grid = []
    for line in lines:
        row = [cell.strip() for cell in line.split(",")]
        grid.append(row)
    return grid


def save_puzzle(filepath, grid):
    """Save a puzzle grid to a file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(grid_to_text(grid))


def load_puzzle(filepath):
    """Load a puzzle grid from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return text_to_grid(f.read())
