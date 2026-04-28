# dfs algorithm

# 1. create a 'visited' set to track explored nodes for fast lookup
# 2. create a 'stack' (lifo) to control traversal order
# 3. add the start node to both 'visited' and 'stack'
# 4. repeat until the stack is empty:
#    - remove the top node from the stack
#    - process the node (e.g., print)
#    - if node is the goal → stop and return success
#    - otherwise, explore all neighbors in reverse order
#    - for each neighbor not in visited:
#         → add to visited
#         → add to stack
# 5. if stack empties without finding goal → return failure

# dfs goal-based agent
class Environment:
    def __init__(self, graph):
        self.graph = graph

    def get_percept(self, node):
        return node  

class GoalBasedAgent:
    def __init__(self, goal):
        self.goal = goal

    def formulate_goal(self, percept):
        if percept == self.goal:
            return "Goal reached"
        return "Searching"

    def dfs_search(self, graph, start, goal):
        visited = set()
        stack = []

        visited.add(start)
        stack.append(start)

        while stack:
            node = stack.pop() 
            print(f"Visiting: {node}")

            if node == goal:
                return f"Goal {goal} found!"

            # reverse to maintain correct DFS order
            for neighbour in reversed(graph.get(node, [])):
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append(neighbour)

        return "Goal not found"

    def act(self, percept, graph):
        goal_status = self.formulate_goal(percept)

        if goal_status == "Goal reached":
            return f"Goal {self.goal} found!"
        else:
            return self.dfs_search(graph, percept, self.goal)

def run_agent(agent, environment, start_node):
    percept = environment.get_percept(start_node)
    action = agent.act(percept, environment.graph)
    print(action)


# Tree
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

# depth-limited dfs algorithm

# 1. define a recursive dfs function with parameters:
#       node, goal, current depth, path, visited set
# 2. if current depth exceeds depth_limit → stop recursion
# 3. mark current node as visited and add to path
# 4. process the node (e.g., print with depth)
# 5. if node is the goal → return current path
# 6. if depth < depth_limit:
#       - for each neighbor not in visited:
#           → recursively call dfs with depth + 1
#           → if goal found in recursion → return path
# 7. if no goal found at this branch → backtrack:
#       - remove node from path and visited
#       - return None
# 8. after recursion finishes:
#       - if result_path exists → print goal and path
#       - else → print goal not found within depth limit

def dls(graph, start, goal, depth_limit):
    def dfs(node, goal, depth, path, visited):
        if depth > depth_limit:
            return None

        visited.add(node)
        path.append(node)

        print(f"Visiting: {node} at depth {depth}")

        if node == goal:
            return path

        # expand only if depth < limit
        if depth < depth_limit:
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    result = dfs(neighbor, goal, depth + 1, path, visited)
                    if result:
                        return result

        # backtrack
        path.pop()
        visited.remove(node)
        return None

    result_path = dfs(start, goal, 0, [], set())

    if result_path:
        print(f"\nGoal found! Path: {' -> '.join(result_path)}")
    else:
        print(f"\nGoal not found within depth limit {depth_limit}")