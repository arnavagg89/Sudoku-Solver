# main.py
from typing import List, Optional
from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sudokuAPI import SudokuSolver

Row = Annotated[List[int], Field(min_length=9, max_length=9)]
Board = Annotated[List[Row], Field(min_length=9, max_length=9)]

class SolveRequest(BaseModel):
    board: Board
    method: Optional[str] = "heuristic"
    seed: Optional[int] = None

class SolveResponse(BaseModel):
    solved: bool
    board: Optional[Board] = None
    time_ms: Optional[float] = None
    nodes: Optional[int] = None
    message: Optional[str] = None

app = FastAPI(title="Sudoku Solver")

# (Optional) CORS if you open index.html directly via file:// or host elsewhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

@app.post("/solve", response_model=SolveResponse)
def solve(req: SolveRequest):
    try:
        s = SudokuSolver(req.board, seed=req.seed)
        board = s.solve(req.method or "heuristic")
        return SolveResponse(solved=True, board=board, time_ms=s.time_ms, nodes=s.counter)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Serve static frontend at /
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
