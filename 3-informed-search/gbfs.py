# A robot is placed in a grid environment containing multiple objects.
# The robot must collect the closest object first based on heuristic distance.

def getHeuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

def GBFS (grid, start, objects):
    rows = len(grid)
    cols = len(grid[0])

    # frontier = [(start, 0)]
    currentPosition = start

    while objects:
        # choosing nearest objects
        choosenObject = objects[0]
        for obj in objects:
            if getHeuristic(currentPosition, obj) < getHeuristic(currentPosition, choosenObject):
                choosenObject = obj

        frontier = [(currentPosition, getHeuristic(currentPosition, choosenObject))] 
        visited = set()

        while frontier:
            frontier.sort(key = lambda x:x[1])
            currentPosition, _ = frontier.pop(0)

            if currentPosition in visited:
                continue

            visited.add(currentPosition)

            if currentPosition == choosenObject:
                print(f"Object Found at {currentPosition}")
                objects.remove(choosenObject)
                break   

            for dx, dy in [(0,1),(0,-1),(-1,0),(1,0)]:
                newPosition = (currentPosition[0] + dx, currentPosition[1] + dy)

                if (
                    newPosition[0] >= 0 and newPosition[0] < rows and 
                    newPosition[1] >= 0 and newPosition[1] < cols and
                    grid[newPosition[0]][newPosition[1]] == 0 and newPosition not in visited
                ):
                    newH = getHeuristic(newPosition, choosenObject)
                    frontier.append((newPosition, newH))


# 0 = free, 1 = obstacle
grid = [
    [0,0,0,0],
    [0,0,1,0],
    [1,0,0,0],
    [0,0,1,0]
]
objects = [(0,1),(2,2),(3,1)]

start = (0,0)

print("Robot Object Collection using GBFS")
GBFS(grid, start, objects)