# A software firm is developing an automated system to assign 6 developers to 
# 6 different project modules: AI, Web, Mobile, Cloud, Security, and Testing.

# Each developer must be assigned exactly one module, and 
# no module can be assigned to more than one developer.

# Due to expertise limitations, the following domain restrictions apply:
#   - Dev1 can only work on AI, Web, Mobile, or Cloud       
#   - Dev2 can only work on Web, Mobile, or Cloud           
#   - Dev3 can work on any module EXCEPT AI        

# In addition, the following conditional dependencies must be enforced:
#   1. If Dev1 is assigned to AI, then Dev4 must be assigned to Security.
#   2. If Dev3 is assigned to Web, then Dev5 must NOT be assigned to Testing.

from ortools.sat.python import cp_model

# variables
devs = ["Dev 1", "Dev 2", "Dev 3", "Dev 4", "Dev 5", "Dev 6"]

# domain
modules = ["AI", "Web", "Mobile", "Cloud", "Security", "Testing"]

# creating model
model = cp_model.CpModel()

# assigning domains
solVars = {}

for i in devs:
    solVars[i] = model.NewIntVar(0, len(modules) - 1, i)

# constraints
for m in [4,5]:
    model.add(solVars['Dev 1'] != m)

for m in [0,4,5]:
    model.add(solVars['Dev 2'] != m)

model.add(solVars['Dev 3'] != 0)

b1 = model.NewBoolVar("dev1 ai")
model.add(solVars["Dev 1"] == 0).only_enforce_if(b1)
model.add(solVars["Dev 1"] != 0).only_enforce_if(b1.Not())
model.add(solVars["Dev 4"] == 4).only_enforce_if(b1)

b2 = model.NewBoolVar("dev3 web")
model.add(solVars["Dev 3"] == 1).only_enforce_if(b2)
model.add(solVars["Dev 3"] != 1).only_enforce_if(b2.Not())
model.add(solVars["Dev 5"] != 5).only_enforce_if(b2)

model.add_all_different(solVars.values())

class SolutionCollector (cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.solutions = []


    def on_solution_callback(self):
        sol = {}
        for dev, var in self.variables.items():
            sol[dev] = modules[self.value(var)]
        
        self.solutions.append(sol)

collector = SolutionCollector(solVars)
solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True

status = solver.solve(model, collector)

if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    print("\nTotal Solutions: ", len(collector.solutions))
    print("\nFirst 5 solutions")
    for i, sol in enumerate(collector.solutions[:5]):
        print(f"\nSolution {i + 1}: ")
        for dev, mod in sol.items():
            print(f"    {dev}: {mod}")

else:
    print("\nNo Valid Solution!")