"""
Performance benchmark comparing DFS Backtracking vs SAT Solver (Z3)
on predefined Flow Free puzzles.
"""

import time

from board import Board
from puzzles import PUZZLES
from sat_solver import SATSolver
from solve import Solver


def benchmark_solver(solver_class, board, solver_name):
    """Run a solver and return (solved, elapsed_seconds)."""
    fresh_board = Board([row[:] for row in board.grid])
    solver = solver_class(fresh_board)

    start = time.perf_counter()
    solved = solver.solve()
    elapsed = time.perf_counter() - start

    return solved, elapsed


def run_benchmarks():
    """Run both solvers on all predefined puzzles and print results."""
    header = f"{'Puzzle':<18} {'Size':>4}  {'DFS Result':>10} {'DFS Time':>10}  {'SAT Result':>10} {'SAT Time':>10}  {'Faster':>8}"
    separator = "-" * len(header)

    print()
    print("=" * len(header))
    print("  Flow Free Solver — Performance Benchmark")
    print("=" * len(header))
    print()
    print(header)
    print(separator)

    results = []

    for name, grid in PUZZLES.items():
        size = len(grid)
        board = Board([row[:] for row in grid])

        # DFS
        dfs_solved, dfs_time = benchmark_solver(Solver, board, "DFS")

        # SAT
        sat_solved, sat_time = benchmark_solver(SATSolver, board, "SAT")

        # Determine faster
        if dfs_solved and sat_solved:
            if dfs_time < sat_time:
                faster = "DFS"
            elif sat_time < dfs_time:
                faster = "SAT"
            else:
                faster = "Tie"
        elif dfs_solved:
            faster = "DFS"
        elif sat_solved:
            faster = "SAT"
        else:
            faster = "N/A"

        dfs_result = "Solved" if dfs_solved else "Failed"
        sat_result = "Solved" if sat_solved else "Failed"

        print(
            f"{name:<18} {size:>3}x{size:<1} {dfs_result:>10} {dfs_time:>9.4f}s  {sat_result:>10} {sat_time:>9.4f}s  {faster:>8}"
        )

        results.append({
            "name": name,
            "size": size,
            "dfs_solved": dfs_solved,
            "dfs_time": dfs_time,
            "sat_solved": sat_solved,
            "sat_time": sat_time,
            "faster": faster,
        })

    print(separator)
    print()

    # Summary
    dfs_wins = sum(1 for r in results if r["faster"] == "DFS")
    sat_wins = sum(1 for r in results if r["faster"] == "SAT")
    total_dfs = sum(r["dfs_time"] for r in results)
    total_sat = sum(r["sat_time"] for r in results)

    print("Summary:")
    print(f"  DFS faster in {dfs_wins}/{len(results)} puzzles")
    print(f"  SAT faster in {sat_wins}/{len(results)} puzzles")
    print(f"  Total DFS time: {total_dfs:.4f}s")
    print(f"  Total SAT time: {total_sat:.4f}s")
    print()

    return results


if __name__ == "__main__":
    run_benchmarks()
