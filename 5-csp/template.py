from ortools.sat.python import cp_model

"""
CSP universal template (OR-Tools CP-SAT)

Steps:
1. Define variables: the things you need to assign values to (e.g. nodes, days, cells)
2. Define domain: the valid values each variable can take (encoded as integers)
3. Create solver variables: one IntVar per variable, with domain range baked in
4. Add constraints: rules the solver must satisfy
5. Collect solutions via callback (or read directly if single solution expected)
6. Run the solver and print results
"""

# step 1 — variables
variables = ['A', 'B', 'C']                             # things to assign values to

# step 2 — domain pool
domain = ['Red', 'Green', 'Blue']                       # possible values (will be encoded as 0, 1, 2...)

# step 3 — create model and solver variables
model = cp_model.CpModel()

# each variable gets an IntVar (solver variable) with range 0 to len(domain)-1
# the integer maps back to domain[i]
solverVars = {}
for var in variables:
   solverVars[var] = model.new_int_var(0, len(domain) - 1, var)

# step 4 — add constraints

# example: all variables must have different values
model.add_all_different(solverVars.values())

# example: two specific variables must differ
model.add(solverVars['A'] != solverVars['B'])

# example: fix a variable to a specific value
model.add(solverVars['A'] == 0)

# step 5 — collect solutions via callback (use when multiple solutions needed)
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables                     # store solverVars
        self.solutions = []                             # list to collect all solutions

    def on_solution_callback(self):                     # auto-called on each valid solution
        sol = {}
        for var, intVar in self._variables.items():     # for each variable and its solver handle
            sol[var] = domain[self.value(intVar)]       # self.value() -> index -> domain value
        self.solutions.append(sol)

collector = SolutionCollector(solverVars)

# step 6 — run solver and print results
solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True        # find every valid assignment

status = solver.solve(model, collector)

# output
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Total solutions found: {len(collector.solutions)}\n")
    for i, sol in enumerate(collector.solutions, 1):
        print(f"Solution {i}: {sol}")
else:
    print("No solution found.")

# cheat sheet: what changes per question
"""
Question        Variables                   Constraints to add
-----------     -------------------------   -------------------------------------------
Graph Coloring  nodes of graph              model.add(nodeVars[a] != nodeVars[b]) per edge
Map Coloring    regions of map              model.add(regionVars[a] != regionVars[b]) per border
Scheduling      time slots / days           model.add_all_different(...) + narrow domain per variable
Sudoku          cells (row, col)            add_all_different per row, per col, per 3x3 box
N-Queens        rows (1 queen per row)      col != same, |row1-row2| != |col1-col2| for diagonals

solver structure is always the same — only the variables, domain, and constraints change.
"""