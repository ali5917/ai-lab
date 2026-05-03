from ortools.sat.python import cp_model

"""
Dressing Schedule 

Resources:
    Shalwar Qamees (SQ): 2 distinct sets.
    Shirts (S): 5 distinct shirts;
    Pants (P): 3 distinct pants.

Assign one unique outfit per day (Mon-Fri) under constraints:
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
dayVars = {}
for day in days:
    dayVars[day] = model.new_int_var(0, len(allOutfits) - 1, day)

# constraint 1 - Monday must be Shirt-Pant (0-14)
model.add(dayVars['Monday'] <= 14)      

# constraint 2 - Thursday must be Shirt-Pant (0-14)
model.add(dayVars['Thursday'] <= 14)    

# constraint 3 - Friday must be Shalwar Qamees (15-16)
model.add(dayVars['Friday'] >= 15)      

# constraint 4 - no outfit repeated (all days must have a different outfit)
model.add_all_different(dayVars.values())

# collect all solutions
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables                        # store dayVars
        self.solutions = []                               # list to collect all solutions

    def on_solution_callback(self):
        sol = {}
        for day, var in self.variables.items():           # for each day and its solver variable
            sol[day] = allOutfits[self.value(var)]        # self.value(var) → index → outfit name
        self.solutions.append(sol)

collector = SolutionCollector(dayVars)

solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True           # find every valid schedule
status = solver.solve(model, collector)

# output
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Total valid schedules: {len(collector.solutions)}\n")
    print("First 5 solutions:")
    for i, sol in enumerate(collector.solutions[:5]):
        print(f"\n  Schedule {i}:")
        for day, outfit in sol.items():
            print(f"    {day:<12} : {outfit}")
else:
    print("No solution found.")