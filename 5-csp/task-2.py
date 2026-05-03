from ortools.sat.python import cp_model

"""
Dressing Schedule: Assign one unique outfit per day (Mon-Fri) under constraints:
  - Monday & Thursday must wear Shirt-Pant
  - Friday must wear Shalwar Qamees
  - No outfit repeated across days (all-different)
"""

# variables
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# outfits (domain pool)
shirtPants = []                                     # 15 combos (index 0-14)
for s in range(1, 6):                   
    for p in range(1, 4):
        shirtPants.append(f'S{s}-P{p}')

shalwarQamees = ['SQ1', 'SQ2']                      # 2 sets    (index 15-16)
allOutfits    = shirtPants + shalwarQamees          # 17 total

model = cp_model.CpModel()

# assigning domain to each day
# Monday & Thursday → only shirt-pant indices (0-14)
# Friday → only shalwar-qamees indices (15-16)
# Tuesday/Wednesday → any outfit (0-16)
dayVars = {}
dayVars['Monday'] = model.new_int_var(0,  14, 'Monday')
dayVars['Tuesday'] = model.new_int_var(0,  16, 'Tuesday')
dayVars['Wednesday'] = model.new_int_var(0,  16, 'Wednesday')
dayVars['Thursday'] = model.new_int_var(0,  14, 'Thursday')
dayVars['Friday'] = model.new_int_var(15, 16, 'Friday')

# constraint (no outfit repeated — all days must have a different outfit)
model.add_all_different(dayVars.values())

# collect all solutions
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables                        # store dayVars
        self.solutions = []                                # list to collect all solutions

    def on_solution_callback(self):
        sol = {}
        for day, var in self._variables.items():           # for each day and its solver variable
            sol[day] = allOutfits[self.value(var)]         # self.value(var) → index → outfit name
        self.solutions.append(sol)

collector = SolutionCollector(dayVars)

solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True           # find every valid schedule

status = solver.solve(model, collector)

# output
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Total valid schedules: {len(collector.solutions)}\n")
    print("Showing first 5 solutions:")
    for i, sol in enumerate(collector.solutions[:5], 1):
        print(f"\n  Schedule {i}:")
        for day, outfit in sol.items():
            print(f"    {day:<12} : {outfit}")
else:
    print("No solution found.")