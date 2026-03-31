# A firefighter agent must rescue a trapped person (P) in a burning building represented as a grid. 
# The grid contains safe rooms (0), fire (F), walls (#), the agent's starting position (A), and the trapped person (P). 
# You can only move through safe rooms (0) and must use DFS to find the shortest path to the person.

def computeSteps (path):
    count = 0
    for p in path:
        count += 1
    return count

def dfs (grid, start):
    rows = len(grid)
    cols = len(grid[0])
    frontier =  []
    frontier.append((start, [start], [start]))  # node, path, visited
    shortestPath = None

    while frontier:
        position, path, visited = frontier.pop()
        if grid[position[0]][position[1]] == 'P':
            
            if shortestPath is not None:
                if computeSteps(path) < computeSteps(shortestPath):
                    shortestPath = path
            else: 
                shortestPath = path
        
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            newPosition = (position[0] + dx, position[1] + dy)

            if (
                0 <= newPosition[0] < rows and 0 <= newPosition[1] < cols 
                and grid[newPosition[0]][newPosition[1]] != '#' and grid[newPosition[0]][newPosition[1]] != 'F' 
                and newPosition not in visited
            ):  
                newPath = path + [newPosition]
                newVisited = visited + [newPosition]
                frontier.append((newPosition, newPath, newVisited))
    
    return shortestPath

grid = [
    ['A', '0', '0', '#', '#'],
    ['#', 'F', '0', '#', 'P'],
    ['0', '0', '0', 'F', '0'],
    ['0', '#', 'F', '#', '0'],
    ['0', '0', '0', '0', '0'],
]
start = (0,0)

res = dfs(grid, start)
if res is not None:
    print(f"Path found: {res}")