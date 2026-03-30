class Solver:

    def __init__(self, board):
        self.board = board
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.solution_paths = {}
        self.solution_segments = {}

    def solve(self):
        self.solution_paths = {}
        self.solution_segments = {}
        colors = sorted(
            self.board.pairs.keys(),
            key=lambda color: self.manhattan(
                self.board.pairs[color][0],
                self.board.pairs[color][1],
            ),
        )
        solved = self.solve_color(0, colors)

        if not solved:
            self.solution_paths = {}
            self.solution_segments = {}

        return solved

    def solve_color(self, idx, colors):
        if idx == len(colors):
            return self.board.is_full()

        color = colors[idx]
        start, end = self.board.pairs[color]
        return self.search_path(start, end, color, idx, colors)

    def search_path(self, start, end, color, idx, colors):
        path = [start]
        return self.dfs(start[0], start[1], end, color, idx, colors, path)

    def dfs(self, r, c, end, color, idx, colors, path):
        if (r, c) == end:
            self.solution_paths[color] = path[:]
            self.solution_segments[color] = self.path_to_segments(path)

            if self.solve_color(idx + 1, colors):
                return True

            self.solution_paths.pop(color, None)
            self.solution_segments.pop(color, None)
            return False

        moves = []

        for dr, dc in self.directions:
            nr = r + dr
            nc = c + dc

            if self.board.is_valid(nr, nc, color):
                if self.board.is_empty(nr, nc) or (nr, nc) == end:
                    dist = self.manhattan((nr, nc), end)
                    moves.append((dist, nr, nc))

        moves.sort()

        for _, nr, nc in moves:
            was_empty = self.board.is_empty(nr, nc)

            if was_empty:
                self.board.set_color(nr, nc, color)

            path.append((nr, nc))

            if self.check_degree():
                if self.dfs(nr, nc, end, color, idx, colors, path):
                    return True

            path.pop()

            if was_empty:
                self.board.clear_color(nr, nc)

        return False

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def check_degree(self):
        for r in range(self.board.n):
            for c in range(self.board.n):
                color = self.board.grid[r][c]

                if color == ".":
                    continue

                count = 0

                for dr, dc in self.directions:
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < self.board.n and 0 <= nc < self.board.n:
                        if self.board.grid[nr][nc] == color:
                            count += 1

                if (r, c) in self.board.endpoints:
                    if count > 1:
                        return False
                elif count > 2:
                    return False

        return True

    def path_to_segments(self, path):
        segments = []

        for index in range(len(path) - 1):
            segments.append((path[index], path[index + 1]))

        return segments
