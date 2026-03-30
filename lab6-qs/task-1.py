"""
Task 1

- Start Beam Search with beam width = 2.
- Explore level by level, keeping only top-k (lowest cost) paths.
- If goal is NOT found after every 3 levels:
    → increase beam width by 1
- Maximum beam width allowed = 5.

At each level:
- Print current beam
- Print current beam width

- If goal found → print path and total cost
"""

# graph representation (adjacency list with edge costs)
graph = {
    'S': [('A', 3), ('B', 5), ('C', 1)],      
    'A': [('D', 4), ('E', 5), ('F1', 2)],     
    'B': [('F', 6), ('G', 7), ('H1', 3)],
    'C': [('H', 1), ('I1', 2)],               
    'D': [('I', 2), ('J1', 3)],               
    'E': [('J', 2), ('K1', 3)],
    'F1': [('L1', 2)],
    'F': [('K', 1)], 'G': [('L', 1)], 'H1': [('M1', 2)],
    'H': [('M', 1), ('N1', 2)],               
    'I1': [('O1', 2)],
    'I': [], 'J': [], 'K': [], 'L': [], 'M': [],
    'J1': [], 'K1': [], 'L1': [], 'M1': [], 'N1': [], 'O1': []
}   

def beamSearch (start, goal, beamWidth = 2):
    print(f"Start = {start}, Goal = {goal}\n")

    # initializing beam 
    beam = [([start], 0)]
    level = 1;

    while beam and beamWidth <= 5:
        # displaying beam at each level
        print (f"Level: {level} - Current Beam Width: {beamWidth}")
        print("Nodes:", end=" ")
        for path, cost in beam:
            print(" -> ".join(path), end="    ")
        print("\n" + 15*"---")

        candidates = []
        for path, cost in beam:
            currentNode = path[-1]

            if currentNode == goal:
                return path, cost
            
            neighbours = graph.get(currentNode, [])
            for thisNode, thisCost in neighbours:
                newCost = cost + thisCost
                newPath = path + [thisNode]

                candidates.append((newPath, newCost))

        candidates.sort(key = lambda x: x[1])
        beam = candidates[:beamWidth]

        if level % 3 == 0:
            beamWidth += 1

        level += 1     

    return None, float('inf')

start = 'S'
goal = 'M'
beamWidth = 2

finalPath, finalCost = beamSearch(start, goal, beamWidth)
if finalPath:
    print(f"Final Path: {" -> ".join(finalPath)}\nCost: {finalCost}")
else:
    print("Goal not found!")