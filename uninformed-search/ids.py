# IDS performs repeated DLS increasing the depth limit until the goal is found or the max depth is reached

# 1. define a recursive depth-limited search (dls) function with:
#       node, goal, current depth, path
# 2. check if current node is the goal → if yes, add to path and return True
# 3. if depth limit reached → return False
# 4. if node has no children in the tree → return False
# 5. for each child of the node:
#       - recursively call dls with depth - 1
#       - if recursion returns True → add current node to path (backtracking) and return True
# 6. if no children lead to goal → return False

# 7. define iterative_deepening function with start, goal, max_depth
# 8. for depth = 0 to max_depth:
#       - initialize empty path
#       - call dls(start, goal, depth, path)
#       - if goal found → print path (reversed) and stop
# 9. if loop ends without finding goal → print "goal not found within depth limit"

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

def dls(node, goal, depth, path):
    # check goal first
    if node == goal:
        path.append(node)
        return True

    # stop if depth limit reached
    if depth == 0:
        return False

    if node not in tree:
        return False

    # explore children
    for child in tree[node]:
        if dls(child, goal, depth - 1, path):
            path.append(node)  # backtracking
            return True

    return False


def iterative_deepening(start, goal, max_depth):
    for depth in range(max_depth + 1):
        print(f"Depth: {depth}")
        path = []

        if dls(start, goal, depth, path):
            print("\nPath to goal:", " -> ".join(reversed(path)))
            return

    print("Goal not found within depth limit.")     

startNode = 'A'
goalNode = 'I'
maxSearchDepth = 5

iterative_deepening(startNode, goalNode, maxSearchDepth)