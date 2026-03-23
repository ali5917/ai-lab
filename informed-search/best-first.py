"""
- GBFS explores paths by choosing the node according to a heuristic

1. Initialize a frontier (priority queue) with the start node.
2. Initialize a visited set to track explored nodes.
3. While the frontier is not empty:
    Pop the node with the smallest heuristic value from the frontier.
    If this node is the goal, reconstruct the path by following parent pointers and return it.
    Mark the node as visited.
    Generate all valid neighbors of the current node:
        - If neighbor is not visited:
            - Calculate heuristic h(n) for the neighbor.
            - Add neighbor to the frontier with its heuristic.
4.  If frontier empties without finding the goal, return "No path found".
"""

# GBFS on a Grid Maze
from queue import PriorityQueue

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # cost from start (not used in GBFS)
        self.h = 0  # heuristic: estimated distance to goal
        self.f = 0  # f = h for GBFS

    def __lt__(self, other):
        return self.f < other.f  # Needed for PriorityQueue

def heuristic(current_pos, end_pos):
    """Manhattan distance heuristic for grid"""
    return abs(current_pos[0] - end_pos[0]) + abs(current_pos[1] - end_pos[1])

def gbfs_grid(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    start_node = Node(start)
    end_node = Node(end)
    
    frontier = PriorityQueue()
    frontier.put(start_node)
    visited = set()
    
    while not frontier.empty():
        current_node = frontier.get()
        current_pos = current_node.position
        
        if current_pos == end:
            # Reconstruct path
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        visited.add(current_pos)
        
        # Explore neighbors (up, down, left, right)
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            new_pos = (current_pos[0]+dx, current_pos[1]+dy)
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                maze[new_pos[0]][new_pos[1]] == 0 and new_pos not in visited):
                
                new_node = Node(new_pos, current_node)
                new_node.g = current_node.g + 1
                new_node.h = heuristic(new_pos, end)
                new_node.f = new_node.h  # GBFS uses only heuristic
                frontier.put(new_node)
                visited.add(new_pos)
    return None

maze = [
    [0,0,1,0,0],
    [0,0,0,0,0],
    [0,0,1,0,1],
    [0,0,1,0,0],
    [0,0,0,1,0]
]
start = (0,0)
end = (4,4)
path = gbfs_grid(maze, start, end)
print("GBFS on Grid Maze Path:", path)


# GBFS on a Graph
graph = {
    'A': {'B': 2, 'C': 1},
    'B': {'D': 4, 'E': 3},
    'C': {'F': 1, 'G': 5},
    'D': {'H': 2},
    'E': {},
    'F': {'I': 6},
    'G': {},
    'H': {},
    'I': {}
}

# Heuristic function (estimated cost to goal 'I')
heuristic_graph = {'A': 7,'B': 6,'C': 5,'D': 4,'E': 7,'F': 3,'G': 6,'H': 2,'I': 0}

def gbfs_graph(graph, start, goal):
    frontier = [(start, heuristic_graph[start])]  # priority queue as list
    visited = set()
    came_from = {start: None}
    
    while frontier:
        # sort by heuristic value
        frontier.sort(key=lambda x: x[1])
        current_node, _ = frontier.pop(0)
        
        if current_node in visited:
            continue
        visited.add(current_node)
        print(current_node, end=" ")
        
        if current_node == goal:
            # Reconstruct path
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"\nGoal found! Path: {path}")
            return
        
        # Expand neighbors
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                came_from[neighbor] = current_node
                frontier.append((neighbor, heuristic_graph[neighbor]))
    
    print("\nGoal not found")

print("\nGBFS on Graph:")
gbfs_graph(graph, 'A', 'I')