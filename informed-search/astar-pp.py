# Find the shortest path in an N × M grid, where
# each cell contains a numerical value representing its movement cost. 
# Some cells are blocked (#), meaning they cannot be traversed. 
# The heuristic function should use the Manhattan distance
# Return both the optimal path and the total cost from the start to target.

def getHeuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def getStart(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                return (r, c)

def getGoal(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'T':
                return (r, c)

def astar(grid):
    rows = len(grid)
    cols = len(grid[0])
    start = getStart(grid)
    goal = getGoal(grid)
    gCosts = {start: 0}
    visited = set()
    cameFrom = {start: None}
    frontier = [(start, getHeuristic(start, goal) + 0)]

    while frontier:
        frontier.sort(key = lambda x: x[1])
        currentPosition, _ = frontier.pop(0)

        if currentPosition in visited:
            continue

        visited.add(currentPosition)

        if currentPosition == goal:
            totalCost = gCosts[currentPosition]
            path = []
            while currentPosition is not None:
                path.append(currentPosition)
                currentPosition = cameFrom[currentPosition]

            path.reverse()
            print("Goal Found!")
            return path, totalCost

        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            newPosition = (currentPosition[0] + dx, currentPosition[1] + dy)
            if  (
                    newPosition[0] >= 0 and newPosition[0] < rows and 
                    newPosition[1] >= 0 and newPosition[1] < cols and
                    grid[newPosition[0]][newPosition[1]] != '#'
                ):
                    value = grid[newPosition[0]][newPosition[1]]
                    if value == 'T':
                        newGCost = gCosts[currentPosition] + 1
                    elif value != 'S':
                        newGCost = gCosts[currentPosition] + int(value)
                    
                    fCost = newGCost + getHeuristic(newPosition, goal)

                    if newPosition not in visited or newGCost < gCosts[newPosition]:
                        gCosts[newPosition] = newGCost
                        cameFrom[newPosition] = currentPosition
                        frontier.append((newPosition, fCost))
   

grid = [
    ['S','1','2','#','3'],
    ['1','#','2','#','#'],
    ['1','2','1','2','#'],
    ['#','#','1','#','#'],
    ['1','1','1','2','T'],
]

path, totalCost = astar(grid)
print(f"Path: {path}")
print(f"Total Cost: {totalCost}")