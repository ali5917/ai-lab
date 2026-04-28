"""
A*  finds the **shortest path** from a start node to a goal node.
- It uses both 
    g(n) = actual cost from start to current node
    h(n) = heuristic estimate of cost from current node to goal
- Total cost: f(n) = g(n) + h(n)

1. Initialize the frontier with the start node and f(n) = g + h.
2. Initialize a visited set to track explored nodes.
3. Initialize g_costs dictionary to store the lowest cost to reach each node.
4. Initialize came_from dictionary to reconstruct the path.
5. While the frontier is not empty:
    a. Sort the frontier by lowest f(n) and pop the node with the smallest f(n).
    b. If this node is the goal:
        - Reconstruct the path using came_from and return it.
    c. Mark the node as visited.
    d. For each neighbor:
        - Calculate new g(n) cost from start.
        - Calculate f(n) = g(n) + h(n)
        - If neighbor not visited or new g(n) is lower than previous:
            - Update g_costs and came_from
            - Add neighbor to frontier
6. If frontier empties without finding goal, return "Goal not found".
"""

# Graph with edge costs
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

# Heuristic estimates to goal 'I'
heuristic = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 7, 'F': 3, 'G': 6, 'H': 2, 'I': 0}

def a_star(graph, start, goal):
    frontier = [(start, 0 + heuristic[start])]  # list of tuples (node, f_cost)
    visited = set()  # To track explored nodes
    g_costs = {start: 0}  # Min Cost to reach each node from start
    came_from = {start: None}  # To reconstruct the path

    while frontier:
        frontier.sort(key=lambda x: x[1])
        current_node, current_f = frontier.pop(0) 
        
        if current_node in visited:
            continue
        
        print(current_node, end=" ") 
        visited.add(current_node)
        
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"\nGoal found with A*. Path: {path}")
            return
        
        # Explore neighbors
        for neighbor, cost in graph[current_node].items():
            new_g_cost = g_costs[current_node] + cost
            f_cost = new_g_cost + heuristic[neighbor]  # f(n) = g(n) + h(n)
            
            # Update if this path to neighbor is better
            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                came_from[neighbor] = current_node
                frontier.append((neighbor, f_cost))
    
    print("\nGoal not found")

print("A* Search Traversal:")
a_star(graph, 'A', 'I')