# A project manager is scheduling a set of tasks represented as nodes in a dependency graph. 
# Some tasks depend on others and can only be completed after their predecessors. 
# Each task has a priority value in achieving the project goal (lower value = higher priority)
# The manager uses Best-First Search to decide the order of executing tasks. 
# At each step, the manager chooses the task with the highest priority (lowest heuristic value) among available tasks.
# Your task is to simulate Best-First Search on the task graph and determine the sequence of tasks selected.

heuristics = {"T0":5, "T1":3,"T2":4,"T3":2,"T4":1,"T5":2,"T6":0}

graph = {
    "T0": [("T1", 1), ("T2", 1)],
    "T1": [("T3", 1), ("T4", 1)],
    "T2": [("T5", 1)],
    "T3": [("T6", 1)],
    "T4": [("T6", 1)],
    "T5": [("T6", 1)],
    "T6": []
}

def bestFirst (graph, start):
    frontier = [([start], heuristics.get(start))]
    visited = set()
    order = []

    while frontier:
        frontier.sort(key=lambda x:x[1])
        currentPath, _ = frontier.pop(0)
        currentTask = currentPath[-1]

        if currentTask in visited:
            continue
        visited.add(currentTask)
        order.append(currentTask)
        
        neighbours = graph.get(currentTask)
        for neighbour, _ in neighbours:
            if neighbour not in visited:
                newPath = currentPath + [neighbour]
                frontier.append((newPath, heuristics.get(neighbour)))
        
    return order

res = bestFirst(graph, "T0")
if res is not None:
    print(" -> ".join(res))