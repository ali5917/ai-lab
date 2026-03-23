# UCS finds the least-cost path from start to goal

# 1. create a priority queue (pq) storing tuples (node, cumulative_cost)
# 2. create a 'visited' set to track explored nodes
# 3. create 'cost_so_far' dict to store minimum cost to reach each node
# 4. create 'came_from' dict to track parent for path reconstruction
# 5. add start node to pq with cost 0, mark cost_so_far[start] = 0, came_from[start] = None
# 6. repeat while pq is not empty:
#    - sort pq by cumulative cost to simulate priority queue
#    - pop node with lowest cost
#    - if node already visited → skip
#    - mark node as visited
#    - if node is goal → reconstruct path using came_from, print path and total cost, stop
#    - otherwise, explore neighbors:
#         - for each neighbor, compute new_cost = current_cost + edge_cost
#         - if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
#              → update cost_so_far[neighbor] = new_cost
#              → set came_from[neighbor] = current_node
#              → add (neighbor, new_cost) to pq
# 7. if pq empties without finding goal → print "goal not found"

def ucs(graph, start, goal):
    # pq is a list of (node, cumulative_cost)
    pq = [(start, 0)]
    visited = set()                 
    cost_so_far = {start: 0}        # min cost to reach each node
    came_from = {start: None}       # for path reconstruction

    while pq:
        # sort frontier by cost (simulate priority queue)
        pq.sort(key=lambda x: x[1])
        current_node, current_cost = pq.pop(0)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            # reconstruct path
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"Goal found with UCS. Path: {path}, Total Cost: {current_cost}")
            return

        # explore neighbors
        for neighbor, cost in graph.get(current_node, {}).items():
            new_cost = current_cost + cost
            # if neighbor not visited or we found cheaper path
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current_node
                pq.append((neighbor, new_cost))

    print("Goal not found")

graph = {
    'A': {'B': 2, 'C': 5},
    'B': {'D': 4, 'E': 1},
    'C': {'F': 2, 'G': 3},
    'D': {'H': 2},
    'E': {},
    'F': {'I': 3},
    'G': {},
    'H': {},
    'I': {}
}

ucs(graph, 'A', 'I')