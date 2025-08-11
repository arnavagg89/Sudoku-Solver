# sudoku_solver.py
from __future__ import annotations
from typing import List, Tuple, Optional
import time
import random
import copy

Board = List[List[int]]
Cell = Tuple[int, int]


class SudokuSolver:
    def __init__(self, board: Optional[Board] = None, *, seed: Optional[int] = None):
        self.board: Board = copy.deepcopy(board) if board is not None else [[0]*9 for _ in range(9)]
        self.seed = seed
        self.randomize = True
        self.counter = 0
        self.time_ms: float = 0.0
        if seed is not None:
            random.seed(seed)

    # ---------- Public API ----------
    def set_board(self, board: Board) -> None:
        self._validate_shape(board)
        self.board = copy.deepcopy(board)

    def get_board(self) -> Board:
        return copy.deepcopy(self.board)

    def solve(self, method: str = "heuristic") -> Board:
        """method: 'backtracking' | 'forward' | 'heuristic'"""
        self._validate_shape(self.board)
        self.counter = 0
        t0 = time.perf_counter()

        if method == "backtracking":
            empties = self._find_empty_blocks()
            ok = self._solve_backtracking(empties, 0)
        elif method == "forward":
            empties = self._find_empty_blocks()
            ok = self._solve_forwardchecking(empties, 0)
        elif method == "heuristic":
            ok = self._solve_heuristic()
        else:
            raise ValueError("Unknown method. Use 'backtracking', 'forward', or 'heuristic'.")

        self.time_ms = (time.perf_counter() - t0) * 1000.0
        if not ok:
            raise ValueError("No solution found.")
        return self.get_board()

    # ---------- Basics ----------
    def print_board(self) -> None:
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            line = []
            for j, v in enumerate(row):
                if j % 3 == 0 and j != 0:
                    line.append("|")
                line.append(str(v) if v != 0 else ".")
            print(" ".join(line))

    def valid(self, r: int, c: int, val: int) -> bool:
        # row
        for j in range(9):
            if self.board[r][j] == val:
                return False
        # col
        for i in range(9):
            if self.board[i][c] == val:
                return False
        # box
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if self.board[i][j] == val:
                    return False
        return True

    # ---------- Helpers ----------
    def _validate_shape(self, board: Board) -> None:
        if len(board) != 9 or any(len(r) != 9 for r in board):
            raise ValueError("Board must be 9x9.")
        for r in board:
            for x in r:
                if not isinstance(x, int) or not (0 <= x <= 9):
                    raise ValueError("Cells must be integers in 0..9.")

    def _find_empty_blocks(self) -> List[Cell]:
        cells = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        if self.randomize:
            random.shuffle(cells)
        return cells

    def _remaining_values(self, r: int, c: int) -> List[int]:
        if self.board[r][c] != 0:
            return []
        vals = [v for v in range(1, 10) if self.valid(r, c, v)]
        if self.randomize:
            random.shuffle(vals)
        return vals

    def _forward_check(self, empty_cells: List[Cell], position: int) -> bool:
        for k in range(position, len(empty_cells)):
            r, c = empty_cells[k]
            if self.board[r][c] == 0 and not self._remaining_values(r, c):
                return False
        return True

    # ---------- Backtracking ----------
    def _solve_backtracking(self, empty_cells: List[Cell], position: int) -> bool:
        if position == len(empty_cells):
            return True
        r, c = empty_cells[position]
        if self.board[r][c] != 0:
            return self._solve_backtracking(empty_cells, position + 1)

        for v in (self._remaining_values(r, c) or range(1, 10)):
            self.counter += 1
            if self.valid(r, c, v):
                self.board[r][c] = v
                if self._solve_backtracking(empty_cells, position + 1):
                    return True
                self.board[r][c] = 0
        return False

    # ---------- Forward Checking ----------
    def _solve_forwardchecking(self, empty_cells: List[Cell], position: int) -> bool:
        if position == len(empty_cells):
            return True
        r, c = empty_cells[position]
        if self.board[r][c] != 0:
            return self._solve_forwardchecking(empty_cells, position + 1)

        candidates = self._remaining_values(r, c) or list(range(1, 10))
        for v in candidates:
            self.counter += 1
            if self.valid(r, c, v):
                self.board[r][c] = v
                if self._forward_check(empty_cells, position + 1):
                    if self._solve_forwardchecking(empty_cells, position + 1):
                        return True
                self.board[r][c] = 0
        return False

    # ---------- Heuristic (MRV + LCV) ----------
    def _choose_cell_mrv(self) -> Optional[Cell]:
        best: Optional[Tuple[int, int, int]] = None  # (r, c, remaining_count)
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    rem = len(self._remaining_values(r, c))
                    if rem == 0:
                        return None
                    if best is None or rem < best[2]:
                        best = (r, c, rem)
                        if rem == 1:
                            return (r, c)
        return None if best is None else (best[0], best[1])

    def _lcv_order(self, r: int, c: int, candidates: List[int]) -> List[int]:
        impacts = []
        for v in candidates:
            self.board[r][c] = v
            impact = 0
            for rr in range(9):
                for cc in range(9):
                    if self.board[rr][cc] == 0:
                        impact += len(self._remaining_values(rr, cc))
            impacts.append((v, impact))
            self.board[r][c] = 0
        impacts.sort(key=lambda t: (-t[1], t[0]))  # more freedom first
        return [v for v, _ in impacts]

    def _solve_heuristic(self) -> bool:
        def dfs() -> bool:
            cell = self._choose_cell_mrv()
            if cell is None:
                # either solved (no empties) or dead (a cell had 0 options)
                return all(all(v != 0 for v in row) for row in self.board)

            r, c = cell
            candidates = self._remaining_values(r, c)
            if not candidates:
                return False

            for v in self._lcv_order(r, c, candidates):
                self.counter += 1
                self.board[r][c] = v
                if dfs():
                    return True
                self.board[r][c] = 0
            return False

        return dfs()
