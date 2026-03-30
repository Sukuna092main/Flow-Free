class Board:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.n = len(self.grid)
        self.pairs = {}
        self.endpoints = set()
        self.rebuild_metadata()

    def rebuild_metadata(self):
        self.pairs = {}
        self.endpoints = set()

        for r in range(self.n):
            for c in range(self.n):
                color = self.grid[r][c]

                if color != ".":
                    self.endpoints.add((r, c))

                    if color not in self.pairs:
                        self.pairs[color] = [(r, c)]
                    else:
                        self.pairs[color].append((r, c))

    def copy_grid(self):
        return [row[:] for row in self.grid]

    def is_valid(self, r, c, color):
        if not (0 <= r < self.n and 0 <= c < self.n):
            return False
        if self.grid[r][c] != '.' and self.grid[r][c] != color:
            return False
        return True

    def is_empty(self, r, c):
        return self.grid[r][c] == '.'

    def set_color(self, r, c, color):
        self.grid[r][c] = color

    def clear_color(self, r, c):
        self.grid[r][c] = '.'
    
    def is_full(self):
        for row in self.grid:
            if '.' in row:
                return False
        return True

    def __str__(self):
        result = ""
        for row in self.grid:
            result += " ".join(row) + "\n"
        return result

        
