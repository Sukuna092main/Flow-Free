class Solver:

    def __init__(self, board):
        self.board = board
        self.directions = [(0,1),(1,0),(0,-1),(-1,0)]

    # ========================
    # MAIN SOLVER
    # ========================

    def solve(self):

        # heuristic: giải màu gần nhau trước
        colors = sorted(
            self.board.pairs.keys(),
            key=lambda c: self.manhattan(
                self.board.pairs[c][0],
                self.board.pairs[c][1]
            )
        )

        return self.solve_color(0, colors)


    # ========================
    # BACKTRACKING (CSP style)
    # ========================

    def solve_color(self, idx, colors):

        if idx == len(colors):
            return self.board.is_full()

        color = colors[idx]
        start, end = self.board.pairs[color]

        if self.search_path(start, end, color):

            if self.solve_color(idx+1, colors):
                return True

            # nếu màu sau fail → rollback
            self.remove_color(color)

        return False


    # ========================
    # PATH SEARCH (A* idea)
    # ========================

    def search_path(self, start, end, color):

        return self.dfs(start[0], start[1], end, color)


    # ========================
    # DFS + HEURISTIC
    # ========================

    def dfs(self, r, c, end, color):

        if (r,c) == end:
            return True

        moves = []

        for dr,dc in self.directions:

            nr = r + dr
            nc = c + dc

            if self.board.is_valid(nr,nc,color):

                if self.board.is_empty(nr,nc) or (nr,nc)==end:

                    # A* heuristic
                    dist = self.manhattan((nr,nc), end)

                    moves.append((dist,nr,nc))

        # ưu tiên ô gần đích
        moves.sort()

        for _,nr,nc in moves:

            self.board.set_color(nr,nc,color)

            # =================
            # PRUNING
            # =================

            if not self.has_dead_end() and self.check_degree():

                if self.dfs(nr,nc,end,color):
                    return True

            self.board.clear_color(nr,nc)

        return False


    # ========================
    # HEURISTIC
    # ========================

    def manhattan(self, a, b):

        return abs(a[0]-b[0]) + abs(a[1]-b[1])


    # ========================
    # DEAD-END PRUNING
    # ========================

    def has_dead_end(self):

        for r in range(self.board.n):
            for c in range(self.board.n):

                if self.board.grid[r][c] == '.':

                    free = 0

                    for dr,dc in self.directions:

                        nr = r + dr
                        nc = c + dc

                        if 0<=nr<self.board.n and 0<=nc<self.board.n:

                            if self.board.grid[nr][nc] == '.':
                                free += 1

                    if free == 0:
                        return True

        return False


    # ========================
    # CSP CONSTRAINT
    # ========================

    def check_degree(self):

        for r in range(self.board.n):
            for c in range(self.board.n):

                color = self.board.grid[r][c]

                if color == '.':
                    continue

                count = 0

                for dr,dc in self.directions:

                    nr = r + dr
                    nc = c + dc

                    if 0<=nr<self.board.n and 0<=nc<self.board.n:

                        if self.board.grid[nr][nc] == color:
                            count += 1

                if (r,c) in self.board.endpoints:

                    if count > 1:
                        return False

                else:

                    if count > 2:
                        return False

        return True


    # ========================
    # REMOVE PATH
    # ========================

    def remove_color(self, color):

        for r in range(self.board.n):
            for c in range(self.board.n):

                if self.board.grid[r][c] == color:

                    if (r,c) not in self.board.endpoints:
                        self.board.grid[r][c] = '.'