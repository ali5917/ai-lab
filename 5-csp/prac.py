# 6 developers → 6 modules: AI, Web, Mobile, Cloud, Security, Testing

# Constraints to Implement:
#     Uniqueness: no two developers share a module (all-different)
#     Expertise restrictions: some developers are blocked from specific modules
#     Limited subsets: some developers can only be assigned from a small set of allowed modules
#     Conditional dependencies: assigning developer X to module A may enforce or restrict developer Y's assignment to module B

# Implementation Requirements
#     Apply all constraints (uniqueness + conditional) using a constraint solver
#     Demonstrate how conditional constraints are enforced programmatically
#     Ensure no invalid combinations appear in output
#     Search for a valid solution
#     Print the final assignment in human-readable format (developer → module name)

from ortools.sat.python import cp_model

# 1. Variables
developers = ['Dev1', 'Dev2', 'Dev3', 'Dev4', 'Dev5', 'Dev6']

# 2. Domain pool (Represented numerically 0-5)
# 0: AI, 1: Web, 2: Mobile, 3: Cloud, 4: Security, 5: Testing
modules = ['AI', 'Web', 'Mobile', 'Cloud', 'Security', 'Testing']

model = cp_model.CpModel()

# 3. Create solver variables
devVars = {}
for dev in developers:
    devVars[dev] = model.new_int_var(0, len(modules) - 1, dev)

# 4. Constraints

# Constraint 1: Uniqueness - each developer gets exactly one unique module
model.add_all_different(devVars.values())

# Constraint 2: Restrictions - some restricted from specific modules
# Example: Dev1 cannot work on 'Web' (1) or 'Mobile' (2)
model.add(devVars['Dev1'] != 1)
model.add(devVars['Dev1'] != 2)

# Constraint 3: Limited Subset - some can only be assigned to a limited subset
# Example: Dev2 can only work on 'Cloud' (3) or 'Security' (4)
# We enforce this by forbidding all other modules (0, 1, 2, 5)
for m in [0, 1, 2, 5]:
    model.add(devVars['Dev2'] != m)

# Constraint 4: Conditional dependencies
# Example: If Dev3 works on 'AI' (0), then Dev4 MUST work on 'Testing' (5)
b1 = model.new_bool_var('dev3_ai')
model.add(devVars['Dev3'] == 0).only_enforce_if(b1)
model.add(devVars['Dev3'] != 0).only_enforce_if(b1.Not())
model.add(devVars['Dev4'] == 5).only_enforce_if(b1)

# Example: If Dev5 works on 'Cloud' (3), then Dev6 CANNOT work on 'Security' (4)
b2 = model.new_bool_var('dev5_cloud')
model.add(devVars['Dev5'] == 3).only_enforce_if(b2)
model.add(devVars['Dev5'] != 3).only_enforce_if(b2.Not())
model.add(devVars['Dev6'] != 4).only_enforce_if(b2)

# 5. Collect solutions via callback
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.solutions = []

    def on_solution_callback(self):
        sol = {}
        for dev, var in self.variables.items():
            sol[dev] = modules[self.value(var)]
        self.solutions.append(sol)

collector = SolutionCollector(devVars)

# 6. Run solver and print results
solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True
status = solver.solve(model, collector)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Total valid assignments found: {len(collector.solutions)}\n")
    print("First 5 solutions:")
    for i, sol in enumerate(collector.solutions[:5]):
        print(f"\n  Assignment {i + 1}:")
        for dev, mod in sol.items():
            print(f"    {dev:}: {mod}")
else:
    print("No solution found.")