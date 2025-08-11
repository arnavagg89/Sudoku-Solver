# run_solver.py
import argparse, time
from sudokuAPI import SudokuSolver

EXAMPLES = {
    "easy": [
        [0,5,8,0,6,2,1,0,0],
        [0,0,2,7,0,0,4,0,0],
        [0,6,7,9,0,1,2,5,0],
        [0,8,6,3,4,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,7,6,8,9,0],
        [0,2,9,6,0,8,7,4,0],
        [0,0,3,0,0,4,9,0,0],
        [0,0,5,2,9,0,3,8,0]
    ],
    "medium":[
        [8,3,0,6,0,0,0,0,7],
        [0,0,7,0,2,0,0,5,0],
        [0,2,1,0,0,9,0,8,0],
        [6,0,0,0,8,0,0,0,9],
        [0,0,0,4,6,5,0,0,0],
        [3,0,0,0,9,0,0,0,2],
        [0,8,0,2,0,0,3,9,0],
        [0,5,0,0,4,0,2,0,0],
        [2,0,0,0,0,8,0,1,6]
    ],
    "hard": [
        [1,0,0,0,3,0,0,0,0],
        [0,6,2,0,0,0,0,0,0],
        [0,0,0,7,0,2,8,0,4],
        [0,7,0,1,4,0,0,0,2],
        [0,4,0,0,0,0,0,9,0],
        [8,0,0,0,5,6,0,7,0],
        [6,0,9,8,0,7,0,0,0],
        [0,0,0,0,0,0,2,1,0],
        [0,0,0,0,6,0,0,0,9]
    ],
    "evil": [
        [0,1,0,0,0,0,0,0,6],
        [9,0,0,2,0,0,0,0,0],
        [7,3,2,0,4,0,0,1,0],
        [0,4,8,3,0,0,0,0,2],
        [0,0,0,0,0,0,0,0,0],
        [3,0,0,0,0,4,6,7,0],
        [0,9,0,0,3,0,5,6,8],
        [0,0,0,0,0,2,0,0,1],
        [6,0,0,0,0,0,0,3,0]
    ],
    
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", choices=["backtracking","forward","heuristic"], default="heuristic")
    ap.add_argument("--level", choices=list(EXAMPLES.keys()), default="easy")
    ap.add_argument("--trials", type=int, default=1)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    times = []
    moves = []

    for _ in range(args.trials):
        solver = SudokuSolver(EXAMPLES[args.level], seed=args.seed)
        solved = solver.solve(method=args.method)
        times.append(solver.time_ms)
        moves.append(solver.counter)

    # pretty print
    for row in solved:
        print(" ".join(str(x) if x else "." for x in row))
    print(f"\nmethod={args.method} trials={args.trials}")
    print(f"avg_time_ms={sum(times)/len(times):.2f}  min={min(times):.2f}  max={max(times):.2f}")
    print(f"avg_nodes={sum(moves)/len(moves):.0f}   min={min(moves)}   max={max(moves)}")

if __name__ == "__main__":
    main()
