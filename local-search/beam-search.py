"""
Beam Search explores a graph/tree by keeping only the best 'k' paths at each level (beam width).

1. Initialize the beam with the start node as a path with cumulative cost 0.
2. While the beam is not empty:
    Initialize an empty list of candidate paths.
    For each path in the beam:
        Check the last node:
            - If it is the goal, return the path and cost.
            Expand the node to generate successors:
            - For each neighbor, create new path & cumulative cost.
            - Add it to candidates.
    Keep only the top 'k' paths with lowest cumulative cost.
3. If the beam empties without reaching the goal, return failure.
"""

# Graph representation (adjacency list with edge costs)
graph = {
    'S': [('A', 3), ('B', 6), ('C', 5)],
    'A': [('D', 9), ('E', 8)],
    'B': [('F', 12), ('G', 14)],
    'C': [('H', 7)],
    'H': [('I', 5), ('J', 6)],
    'I': [('K', 1), ('L', 10), ('M', 2)],
    'D': [], 'E': [],
    'F': [], 'G': [],
    'J': [], 'K': [],
    'L': [], 'M': []
}

def beam_search(start, goal, beam_width = 2):
    beam = [(0, [start])]  # (cumulative_cost, path)
    
    while beam:
        candidates = []
        
        # expand each path in the current beam
        for cost, path in beam:
            current_node = path[-1]
            
            # goal check
            if current_node == goal:
                return path, cost
            
            # generate successors
            for neighbor, edge_cost in graph.get(current_node, []):
                new_cost = cost + edge_cost
                new_path = path + [neighbor]
                candidates.append((new_cost, new_path))
        
        # sort candidates by cumulative cost and keep top-k
        candidates.sort(key = lambda x: x[0])
        beam = candidates[:beam_width]
    
    # goal not found
    return None, float('inf')

start_node = 'S'
goal_node = 'L'
beam_width = 3

path, cost = beam_search(start_node, goal_node, beam_width)

if path:
    print(f"Path found: {' → '.join(path)} with total cost: {cost}")
else:
    print("No path found.")