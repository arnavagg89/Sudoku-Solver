# app.py
import time
import random
import numpy as np
import streamlit as st

# import your existing code
import sudoku as sdk  # make sure sudoku.py is in the same folder

st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="centered")
st.title("🧩 Sudoku Solver (Local)")

# ---------- helper utils ----------
EXAMPLES = {
    "Easy": [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9],
    ],
    "Hard": [
        [0,0,0, 0,0,0, 0,1,2],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,1, 0,9,4, 0,0,0],
        [0,0,0, 0,0,0, 3,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,8, 0,0,0, 0,0,0],
        [0,0,0, 7,0,0, 2,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [7,2,0, 0,0,0, 0,0,0],
    ],
}

def is_valid_grid(grid):
    """Validate current grid: non-zero entries must not violate row/col/box rules."""
    def ok(nums):
        seen = [n for n in nums if n != 0]
        return len(seen) == len(set(seen))
    # rows
    for r in range(9):
        if not ok(grid[r]): return False
    # cols
    for c in range(9):
        if not ok([grid[r][c] for r in range(9)]): return False
    # boxes
    for br in range(0,9,3):
        for bc in range(0,9,3):
            box = [grid[r][c] for r in range(br,br+3) for c in range(bc,bc+3)]
            if not ok(box): return False
    return True

def run_solver(board, method, seed=None):
    """
    Normalize calls to your existing API.
    - Heuristic likely works with board only.
    - Backtracking/Forward Checking need the empty cell list and a start index.
    Handles both 'return solved board' and 'mutate-in-place' styles.
    """
    if seed is not None:
        random.seed(seed)
    b = [row[:] for row in board]

    if method == "Heuristic":
        res = sdk.solve_heuristic(b)
        # If function returns None/False but mutates, use b; if it returns a board, prefer that
        if isinstance(res, list):
            return res
        return b
    elif method == "Forward Checking":
        empties = sdk.find_empty_blocks(b)
        _ = sdk.solve_forwardchecking(b, empties, 0)
        return b
    else:  # "Backtracking"
        empties = sdk.find_empty_blocks(b)
        _ = sdk.solve_backtracking(b, empties, 0)
        return b

# ---------- sidebar ----------
with st.sidebar:
    st.header("Controls")
    method = st.selectbox("Method", ["Heuristic", "Forward Checking", "Backtracking"])
    set_seed = st.toggle("Deterministic (set seed)", value=True)
    seed = st.number_input("Seed", min_value=0, max_value=10_000_000, value=42, step=1, disabled=not set_seed)
    example_choice = st.selectbox("Load example", ["—", *EXAMPLES.keys()])
    if st.button("Load Example"):
        st.session_state.grid = np.array(EXAMPLES.get(example_choice, EXAMPLES["Easy"]), dtype=int)
    if st.button("Clear Grid"):
        st.session_state.grid[:] = 0

# ---------- grid state ----------
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((9, 9), dtype=int)

st.caption("Tip: Use 0 (or blank) for empty cells.")
grid = st.data_editor(
    st.session_state.grid,
    num_rows=9,
    use_container_width=True,
    disabled=False,
    key="editor",
)

# Ensure integers 0..9
grid = np.array([[int(x or 0) for x in row] for row in grid], dtype=int)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Validate"):
        if is_valid_grid(grid.tolist()):
            st.success("Grid is valid so far (no conflicts).")
        else:
            st.error("There are rule conflicts in the current grid.")
with col2:
    if st.button("Solve"):
        if not is_valid_grid(grid.tolist()):
            st.error("Grid has conflicts. Fix them before solving.")
        else:
            t0 = time.perf_counter()
            try:
                solved = run_solver(grid.tolist(), method, seed=seed if set_seed else None)
                dt = (time.perf_counter() - t0) * 1000
                if solved and all(all(v != 0 for v in row) for row in solved):
                    st.session_state.grid = np.array(solved, dtype=int)
                    st.success(f"Solved with {method} in {dt:.1f} ms")
                else:
                    st.warning("No solution found (or solver did not fill all cells).")
            except Exception as e:
                st.exception(e)
with col3:
    if st.button("Copy as CSV"):
        csv = "\n".join(",".join(str(v) for v in row) for row in st.session_state.grid.tolist())
        st.code(csv, language="text")

st.write("### Current Board")
st.dataframe(st.session_state.grid, use_container_width=True)
