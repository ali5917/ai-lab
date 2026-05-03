from ortools.sat.python import cp_model

"""
Graph Coloring: Assign Red/Green/Blue to each node (variable) so no two adjacent nodes share a color.

Graph: 
    A : B, C 
    B : A, D, E 
    C : A, D 
    D : B, C, E 
    E : B, D
"""

# variables
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'E'],
    'E': ['B', 'D']
}

# domain pool
colors = ['Red', 'Green', 'Blue']
nodes = list(graph.keys())                              # ['A','B','C','D','E']

model = cp_model.CpModel()

# assigning domain to nodes (0 = Red, 1 = Green, 2 = Blue)
nodeVars = {}
for node in nodes:
    nodeVars[node] = model.new_int_var(0, len(colors) - 1, node)

# constraint (adjacent nodes must have different colors)
for node, neighbors in graph.items():
    for neighbor in neighbors:
        if node < neighbor:                             # avoid adding duplicate edges
            model.add(nodeVars[node] != nodeVars[neighbor])

# collect all solutions
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)  
        self.variables = variables                        # store nodeVars
        self.solutions = []                                # list to collect all solutions

    def on_solution_callback(self):
        sol = {}
        for node, var in self.variables.items():          # for each node and its solver variable
            sol[node] = colors[self.value(var)]            # self.value(var) → 0/1/2 → color name
        self.solutions.append(sol)                        

collector = SolutionCollector(nodeVars)

solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True       # find every valid coloring 
status = solver.solve(model, collector)

# output
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Total valid colorings found: {len(collector.solutions)}\n")
    print("First 5 solutions:")
    for i, sol in enumerate(collector.solutions[:5]):
        print(f"Solution {i + 1}: {sol}")
else:
    print("No solution found.")