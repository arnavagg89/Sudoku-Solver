# 🧩 Sudoku Solver (FastAPI + HTML UI)

A fast and flexible Sudoku solver built in Python, using multiple solving strategies.  
Includes a simple **FastAPI backend** and **HTML UI** to choose puzzle difficulty, solve it, and display the solution & solve time.

---

## 🚀 Features
- Multiple solving methods (e.g., heuristic, backtracking, etc.).
- Randomization option for improved solving efficiency.
- Difficulty presets: `Easy`, `Medium`, `Hard`, `Evil`.
- Web UI built with HTML + JavaScript served by FastAPI.
- API endpoint for integration with other apps.
- Clean, modular Python solver logic.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

git clone https://github.com/arnavagg89/Sudoku-Solver.git
cd Sudoku-Solver

### 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

### 3. Install Dependencies
pip install -r requirements.txt

### Run
uvicorn main:app --reload