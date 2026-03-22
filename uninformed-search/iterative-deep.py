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
    # check goal FIRST
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