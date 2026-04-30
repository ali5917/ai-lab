# A smart home cleaning robot is designed to keep a room clean by moving across all areas and collecting dirt. 
# The room is represented as a 4×4 grid, where each cell has a cleanliness score: 0 = clean, 1 dirty, 2 very dirty
# The robot can move up, down, left, or right to an adjacent cell in one move. 
# The robot has a limited energy, which allows it to make a maximum of 8 moves. 
# The robot's goal is to maximize the total cleanliness score collected in the given number of moves. 
# It must plan its path carefully to prioritize high-value cells while avoiding obstacles marked as X in the grid.
# This Utility-Based Agent, since it evaluates possible outcomes and chooses actions that maximize total utility 

class Environment:
    def __init__(self, grid):
        self.grid = grid

    def getPercept (self):
        return self.grid    

def getScore (grid, position):
    score = 0
    if grid[position[0]][position[1]] == "2":
        score += 2
    elif grid[position[0]][position[1]] == "1":
        score += 1
    else:
        score += 0
    return score

class UtilityBasedAgent:
    def computeUtility (self, score):
        return score * 10

    def selectAction (self, allPaths):
        maxUtility = float('-inf')
        bestPath = None

        for thisPath in allPaths:
            path, score = thisPath
            util = self.computeUtility(score)

            print(f"Path: {path}    Score: {score}  Utility: {util}")
            if util > maxUtility:
                maxUtility = util
                bestPath = thisPath
        
        return bestPath, maxUtility

    def bfsSearch (self, grid, start):
        rows = len(grid)
        cols = len(grid[0])
        frontier = []
        allPaths = []

        frontier.append(([start], 0, 0, [start])) # node, score, moves, visited

        moves = 0
        while frontier:
            currentPath, score, moves, visited = frontier.pop(0)
            currentPosition = currentPath[-1]

            if moves >= 8:
                allPaths.append((currentPath, score))
                continue
            
            expanded = False
            for dx, dy in ((0,1), (0,-1), (1,0), (-1,0)):
                newPosition = (currentPosition[0] + dx, currentPosition[1] + dy)

                if (
                    0 <= newPosition[0] < rows and 0 <= newPosition[1] < cols 
                    and grid[newPosition[0]][newPosition[1]] != "X" and newPosition not in visited
                ):
                    newScore = score + getScore(grid, newPosition)
                    newPath = currentPath + [newPosition]
                    newVisited = visited + [newPosition]
                    frontier.append((newPath, newScore, moves + 1, newVisited))
                    expanded = True

            if not expanded:
                allPaths.append((currentPath, score))

        return allPaths    

    def act(self, grid, start):
        result = self.bfsSearch(grid, start)
        return self.selectAction(result)    

grid = [
    ["S", "2", "0", "1"],
    ["1", "X", "0", "1"],
    ["0", "1", "X", "2"],
    ["1", "2", "0", "1"]
]

def run_agent(env, a, start):
    percept = env.getPercept()
    action, maxU = a.act(percept, start)
    print(f"\nChoosen Path (Best Utility): {action[0]}  Score: {action[1]}  Utility: {maxU}")

env = Environment(grid)
a = UtilityBasedAgent()

run_agent(env, a, (0,0))