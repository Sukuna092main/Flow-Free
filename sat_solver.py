from z3 import And, Bool, If, Implies, Int, Not, Or, PbEq, Solver, sat


class SATSolver:
    def __init__(self, board):
        self.board = board
        self.n = board.n
        self.colors = sorted(board.pairs.keys())
        self.color_ids = {color: index for index, color in enumerate(self.colors)}
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.max_rank = self.n * self.n - 1

        self.cell_color = {}
        self.edge_used = {}
        self.rank = {}
        self.solution_segments = {}

    def solve(self):
        self.solution_segments = {}
        if not self.is_valid_input():
            return False

        solver = Solver()
        self.create_variables()
        self.add_cell_constraints(solver)
        self.add_endpoint_constraints(solver)
        self.add_path_constraints(solver)
        self.add_rank_constraints(solver)

        if solver.check() != sat:
            return False

        model = solver.model()
        self.apply_model(model)
        return True

    def is_valid_input(self):
        if not self.colors:
            return False

        for color in self.colors:
            if len(self.board.pairs[color]) != 2:
                return False

        return True

    def create_variables(self):
        for r in range(self.n):
            for c in range(self.n):
                for color in self.colors:
                    key = (r, c, color)
                    color_id = self.color_ids[color]
                    self.cell_color[key] = Bool(f"cell_{r}_{c}_k{color_id}")
                    self.rank[key] = Int(f"rank_{r}_{c}_k{color_id}")

                    for nr, nc in self.neighbors(r, c):
                        edge_key = (r, c, nr, nc, color)
                        edge_name = f"edge_{r}_{c}_{nr}_{nc}_k{color_id}"
                        self.edge_used[edge_key] = Bool(edge_name)

    def add_cell_constraints(self, solver):
        for r in range(self.n):
            for c in range(self.n):
                literals = [(self.cell_color[(r, c, color)], 1) for color in self.colors]
                solver.add(PbEq(literals, 1))

    def add_endpoint_constraints(self, solver):
        for color in self.colors:
            start, end = self.board.pairs[color]

            for r in range(self.n):
                for c in range(self.n):
                    cell_var = self.cell_color[(r, c, color)]

                    if (r, c) == start:
                        solver.add(cell_var)
                    elif (r, c) == end:
                        solver.add(cell_var)
                    elif (r, c) in self.board.endpoints:
                        solver.add(Not(cell_var))

    def add_path_constraints(self, solver):
        for color in self.colors:
            start, end = self.board.pairs[color]

            for r in range(self.n):
                for c in range(self.n):
                    for nr, nc in self.neighbors(r, c):
                        edge_var = self.edge_used[(r, c, nr, nc, color)]
                        solver.add(
                            Implies(
                                edge_var,
                                And(
                                    self.cell_color[(r, c, color)],
                                    self.cell_color[(nr, nc, color)],
                                ),
                            )
                        )

            for r in range(self.n):
                for c in range(self.n):
                    cell_var = self.cell_color[(r, c, color)]
                    incoming = self.incoming_edges(r, c, color)
                    outgoing = self.outgoing_edges(r, c, color)
                    in_count = self.bool_sum(incoming)
                    out_count = self.bool_sum(outgoing)

                    if (r, c) == start:
                        solver.add(in_count == 0)
                        solver.add(out_count == 1)
                    elif (r, c) == end:
                        solver.add(in_count == 1)
                        solver.add(out_count == 0)
                    else:
                        solver.add(If(cell_var, in_count == 1, in_count == 0))
                        solver.add(If(cell_var, out_count == 1, out_count == 0))

    def add_rank_constraints(self, solver):
        for color in self.colors:
            start, _ = self.board.pairs[color]
            start_rank = self.rank[(start[0], start[1], color)]
            solver.add(start_rank == 0)

            for r in range(self.n):
                for c in range(self.n):
                    cell_var = self.cell_color[(r, c, color)]
                    rank_var = self.rank[(r, c, color)]

                    if (r, c) != start:
                        solver.add(If(cell_var, rank_var >= 1, rank_var == 0))

                    solver.add(rank_var >= 0)
                    solver.add(rank_var <= self.max_rank)

                    for nr, nc in self.neighbors(r, c):
                        edge_var = self.edge_used[(r, c, nr, nc, color)]
                        solver.add(
                            Implies(
                                edge_var,
                                self.rank[(nr, nc, color)] == rank_var + 1,
                            )
                        )

    def apply_model(self, model):
        solved_grid = []
        solution_segments = {color: [] for color in self.colors}

        for r in range(self.n):
            row = []

            for c in range(self.n):
                chosen = "."

                for color in self.colors:
                    if model.evaluate(self.cell_color[(r, c, color)], model_completion=True):
                        chosen = color
                        break

                row.append(chosen)

            solved_grid.append(row)

        for color in self.colors:
            for r in range(self.n):
                for c in range(self.n):
                    for nr, nc in self.neighbors(r, c):
                        edge_var = self.edge_used[(r, c, nr, nc, color)]

                        if model.evaluate(edge_var, model_completion=True):
                            solution_segments[color].append(((r, c), (nr, nc)))

        self.board.grid = solved_grid
        self.solution_segments = solution_segments

    def neighbors(self, r, c):
        result = []

        for dr, dc in self.directions:
            nr = r + dr
            nc = c + dc

            if 0 <= nr < self.n and 0 <= nc < self.n:
                result.append((nr, nc))

        return result

    def incoming_edges(self, r, c, color):
        edges = []

        for nr, nc in self.neighbors(r, c):
            edges.append(self.edge_used[(nr, nc, r, c, color)])

        return edges

    def outgoing_edges(self, r, c, color):
        edges = []

        for nr, nc in self.neighbors(r, c):
            edges.append(self.edge_used[(r, c, nr, nc, color)])

        return edges

    def bool_sum(self, variables):
        return sum(If(var, 1, 0) for var in variables)
