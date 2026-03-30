class Environment:
    def __init__ (self, graph):
        self.graph = graph

    def getPercept (self, p):
        return p
    
class GoalBasedAgent:
    def __init__ (self, goal, dl):
        self.goal = goal
        self.depthLimit = dl

    def formulateGoal (self, percept):
        if percept == self.goal:
            return "Goal Found!"
        else:
            return "Searching..."
        
    def ids(self, graph, start, goal, depthLimit):
        def dls(graph, node, goal, path, depth):
            if node == goal:
                path.append(node)
                return True
            
            if depth == 0:
                return False
            
            if node not in graph:
                return False
            
            neighbours = graph.get(node)
            for neighbour in neighbours:
                if dls(graph, neighbour, goal, path, depth - 1):
                    path.append(node)
                    return True
        
            return False
    
        for depth in range(depthLimit + 1):
            path = [] 
            if dls(graph, start, goal, path, depth):
                path.reverse()
                return "Goal Found!", path

        return "Goal Not Found!", None
    
    def act(self, percept, graph):
        goalStatus = self.formulateGoal(percept)
        if goalStatus == "Goal Found!":
            return "Goal Reached!"
        else:
            goalStatus, path = self.ids(graph, percept, self.goal, self.depthLimit)
            if goalStatus == "Goal Found!" and path is not None:
                return f"Goal Found! Path: {' -> '.join(path)}"
        
def run_agent(env, agent, start):
    percept = env.getPercept(start)
    action = agent.act(percept, env.graph)
    print(action)

graph = {
    'R1': ['R2','R4'],
    'R2': ['R1','R3','R5'],
    'R3': ['R2','R6'],
    'R4': ['R1','R5','R7'],
    'R5': ['R3','R4','R6','R8'],
    'R6': ['R3','R5','R9'],
    'R7': ['R4','R8'],
    'R8': ['R5','R7','R9'],
    'R9': ['R6','R8']
}

start = 'R1'
goal = 'R8'

a = GoalBasedAgent(goal, 4)
env = Environment(graph)
run_agent(env, a, start)