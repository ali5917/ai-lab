class Environment:
    def __init__ (self, graph):
        self.graph = graph

    def getPercept (self, p):
        return p
    
class GoalBasedAgent:
    def __init__ (self, goal):
        self.goal = goal

    def formulateGoal(self, percept):
        if percept == self.goal:
            return "Goal Found!"
        else:
            return "Searching..."
        
    def UCS (self, graph, start, goal):
        frontier = [(start, 0)]
        visited = set()
        cameFrom = {start: None}
        costs = {start: 0}

        while frontier:
            frontier.sort(key=lambda x:x[1])
            currentNode, cost = frontier.pop(0)

            if currentNode in visited:
                continue

            visited.add(currentNode)

            if currentNode == goal:
                path = []
                while currentNode is not None:
                    path.append(currentNode)
                    currentNode = cameFrom[currentNode]
                
                path.reverse()
                print(f"Path: {' -> '.join(path)}")
                print(f"Total Cost: {cost}")
                return "Goal Found!"
            
            neighbours = graph.get(currentNode, [])
            for thisCost, neighbour in neighbours:
                newCost = cost + thisCost
                if newCost < costs[neighbour]:
                    costs[neighbour] = newCost
                    cameFrom[neighbour] = currentNode
                    frontier.append((neighbour, newCost))

        return "Goal not Found!"
    
    def act (self, percept, graph):
        if percept == self.goal:
            return "Goal Found!"
        else:
            return self.UCS(graph, percept, self.goal)
        
def run_agent (env, agent, start):
    percept = env.getPercept(start)
    action = agent.act(percept, env.graph)
    print(action)

graph = {
    'A': [(3, 'C'), (4, 'B')],
    'B': [(4, 'A'), (2, 'C'), (6,'E'), (3, 'D')],
    'C': [(3, 'A'), (2, 'B'), (1, 'D')],
    'D': [(3, 'F'), (1, 'C'), (3, 'B')],
    'E': [(6, 'B'), (4, 'I')],
    'F': [(3, 'D'), (2, 'H')],
    'H': [(2, 'F'), (4, 'I')],
    'I': [(4, 'H'), (4, 'E')],
}

start = 'A'
goal = 'I'

env = Environment(graph)
a = GoalBasedAgent(goal)
run_agent(env, a, start)