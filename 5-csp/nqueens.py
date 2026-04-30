from ortools.sat.python import cp_model

"""
N-Queens: Place N queens on an NxN board so no two queens attack each other.
Variables: one per row — which column does the queen in this row go in?
Domain: 0 to N-1 (column index)
Constraints:
  - all columns different (no two queens share a column)
  - all (col - row) different (no two queens share a down-diagonal)
  - all (col + row) different (no two queens share an up-diagonal)
"""

N = 4

model = cp_model.CpModel()

# assigning domain to each row (which column does that row's queen go in?)
queenVars = {}
for row in range(N):
    queenVars[row] = model.new_int_var(0, N - 1, f'row_{row}')

# constraint: no two queens in the same column
model.add_all_different(queenVars.values())

# constraint: no two queens on the same diagonal
# classic formula: |col1 - col2| != |row1 - row2|
# split into two cases — same down-diagonal and same up-diagonal
for r1 in range(N):
    for r2 in range(r1 + 1, N):
        model.add(queenVars[r1] - queenVars[r2] != r1 - r2)   # down-diagonal: col-row must differ
        model.add(queenVars[r1] - queenVars[r2] != r2 - r1)   # up-diagonal:   col+row must differ

# collect all solutions
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables                     # store queenVars
        self.solutions = []                             # list to collect all solutions

    def on_solution_callback(self):                     # auto-called on each valid solution
        sol = {}
        for row, var in self._variables.items():        # for each row and its solver variable
            sol[row] = self.value(var)                  # self.value(var) -> column index
        self.solutions.append(sol)

collector = SolutionCollector(queenVars)

solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True       # find every valid placement

status = solver.solve(model, collector)

# pretty print helper (. = empty, Q = queen)
def printBoard(sol):
    for row in range(N):
        line = ""
        for col in range(N):
            if sol[row] == col:
                line += "Q "
            else:
                line += ". "
        print(f"  {line}")
    print()

# output
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Total solutions for {N}-queens: {len(collector.solutions)}\n")
    print("Showing first 3 solutions:\n")
    for i, sol in enumerate(collector.solutions[:3], 1):
        print(f"Solution {i}:")
        printBoard(sol)
else:
    print("No solution found.")
