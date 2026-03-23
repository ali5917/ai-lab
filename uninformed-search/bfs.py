# bfs algorithm

# 1. create a 'visited' set to track explored nodes for fast lookup
# 2. create a 'queue' (fifo) to control traversal order
# 3. add the start node to both 'visited' and 'queue'
# 4. repeat until the queue is empty:
#    - remove the front node from the queue
#    - process the node (e.g., print)
#    - if node is the goal → stop and return success
#    - otherwise, explore all neighbors
#    - for each neighbor not in visited:
#         → add to visited
#         → add to queue
# 5. if queue empties without finding goal → return failure

# bfs goal-based agent
class Environment:
    def __init__(self, graph):
        self.graph = graph

    def get_percept(self, node):
        return node

class GoalBasedAgent:
    def __init__(self, goal):
        self.goal = goal

    def formulate_goal(self, percept):
        # check if current percept is the goal
        if percept == self.goal:
            return "Goal reached"
        return "Searching"

    def bfs_search(self, graph, start, goal):
        visited = set()  
        queue = []       

        visited.add(start)
        queue.append(start)

        while queue:
            node = queue.pop(0)  
            print(f"Visiting node: {node}")

            if node == goal:      
                return f"Goal {goal} found!"

            for neighbour in graph.get(node, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return "Goal not found"


    def act(self, percept, graph):
        # decide what to do based on goal status
        goal_status = self.formulate_goal(percept)
        if goal_status == "Goal reached":
            return f"Goal {self.goal} found!"
        else:
            return self.bfs_search(graph, percept, self.goal)

def run_agent(agent, environment, start_node):
    percept = environment.get_percept(start_node)
    action = agent.act(percept, environment.graph) 
    print(action)

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}

start_node = 'A'
goal_node = 'I'

agent = GoalBasedAgent(goal_node)
environment = Environment(tree)

run_agent(agent, environment, start_node)


# maze grid example (1 = open, 0 = blocked)
maze = [
    [1, 1, 0],
    [1, 1, 0],
    [0, 1, 1]
]

# directions (right, down)
directions = [(0, 1), (1, 0)]

# convert maze to graph
def create_graph(maze):
    graph = {}
    rows = len(maze)
    cols = len(maze[0])

    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:  # open cell
                neighbors = []

                for dx, dy in directions:
                    nx, ny = i + dx, j + dy

                    if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                        neighbors.append((nx, ny))

                graph[(i, j)] = neighbors

    return graph

def bfs(graph, start, goal):
    visited = set()
    queue = []

    visited.add(start)
    queue.append(start)

    while queue:
        node = queue.pop(0)
        print(node, end=" ")

        if node == goal:
            print("\ngoal found!")
            return

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)


graph = create_graph(maze)

start_node = (0, 0)
goal_node = (2, 2)

print("Following is the Breadth-First Search (BFS):")
bfs(graph, start_node, goal_node)