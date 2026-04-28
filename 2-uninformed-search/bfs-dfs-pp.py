# A maze is represented as a 2D grid where 0 indicates an open cell and 1 indicates a wall. 
# The objective is to navigate from a given start point to a goal point using BFS and DFS.

def bfs(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    frontier = []
    visited = set()
    cameFrom = {start: None}
    numNodes = 0

    frontier.append(start)
    visited.add(start)

    while frontier:
        currentPosition = frontier.pop(0)
        numNodes += 1

        if currentPosition == goal:
            path = []
            while currentPosition is not None:
                path.append(currentPosition)
                currentPosition = cameFrom[currentPosition]

            path.reverse()
            return path, numNodes
        
    
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            newPosition = (currentPosition[0] + dx, currentPosition[1] + dy)
            if (0 <= newPosition[0] < rows and 0 <= newPosition[1] < cols and 
                newPosition not in visited and grid[newPosition[0]][newPosition[1]] != 1
                ):
                    frontier.append(newPosition)
                    visited.add(newPosition)
                    cameFrom[newPosition] = currentPosition

    return None, 0

def dfs(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    frontier = []
    visited = set()
    cameFrom = {start: None}
    numNodes = 0

    frontier.append(start)
    visited.add(start)

    while frontier:
        currentPosition = frontier.pop()
        numNodes += 1

        if currentPosition == goal:
            path = []
            while currentPosition is not None:
                path.append(currentPosition)
                currentPosition = cameFrom[currentPosition]
            
            path.reverse()
            return path, numNodes
        
    
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            newPosition = (currentPosition[0] + dx, currentPosition[1] + dy)
            if (0 <= newPosition[0] < rows and 0 <= newPosition[1] < cols and 
                newPosition not in visited and grid[newPosition[0]][newPosition[1]] != 1
                ):
                    frontier.append(newPosition)
                    visited.add(newPosition)
                    cameFrom[newPosition] = currentPosition

    return None, 0


maze = [
    [0,1,0,0,0,0],
    [0,1,0,1,1,0],
    [0,0,0,0,1,0],
    [0,1,1,0,0,0],
    [0,0,1,0,1,0],
    [1,0,0,0,1,0]
]

start, goal = (0,0), (5,5)

bfsPath, bfsNodes = bfs(maze, start, goal) 
if bfsPath is not None:
    print(f"Goal Found using BFS! Total Nodes Explored: {bfsNodes}")
    print(f"{bfsPath}  Path Cost: {len(bfsPath)}")
else:
    print("Goal not found using BFS!")
     

dfsPath, dfsNodes = dfs(maze, start, goal) 
if dfsPath is not None:
    print(f"\nGoal Found using DFS! Total Nodes Explored: {dfsNodes}")
    print(f"{dfsPath}  Path Cost: {len(dfsPath)}")
else:
    print("Goal not found using DFS!")