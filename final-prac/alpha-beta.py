# Game Tree Evaluation using Minimax with Alpha-Beta Pruning

# A two-player zero-sum game is represented as a game tree where the MAX player
# tries to maximize the score and the MIN player tries to minimize it.

# Tree Structure:
# - Depth 3: MAX -> MIN -> MAX -> Leaf nodes
# - Root is a MAX node
# - Each internal node has exactly 3 children
# - Leaf node values (left to right):
#   [5, 3, 8, 2, 7, 1, 9, 4, 6, 3, 8, 5, 2, 7, 4, 9, 1, 6, 5, 3, 8, 2, 7, 4, 9, 1, 6]

# Tasks:
#   - Implement Alpha-Beta Pruning on the same tree
#   - Return and print the optimal value at the root
#   - Keep a counter of how many nodes were pruned and print it
#   - Print total nodes evaluated by Alpha-Beta


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.minmaxValue = None

import math
totalNodes = 0
prunedNodes = 0

def alphaBeta (node, alpha, beta, depth, maximizing):
    global totalNodes, prunedNodes
    
    totalNodes += 1

    if depth == 0 or not node.children:
        return node.value

    if maximizing:
        value = -math.inf
        for i, child in enumerate(node.children):
            childValue = alphaBeta(child, alpha, beta, depth - 1, False)
            value = max(value, childValue)
            alpha = max(alpha, value)

            if alpha >= beta:
                prunedNodes += len(node.children) - (i + 1)
                print(f"Pruned nodes - Depth {depth} : {prunedNodes}")
                break                

        node.minmaxValue = value
        return value

    else:
        value = math.inf
        for i, child in enumerate(node.children):
            childValue = alphaBeta(child, alpha, beta, depth - 1, True)
            value = min(value, childValue)
            beta = min(beta, value)

            if alpha >= beta:
                prunedNodes += len(node.children) - (i + 1)
                print(f"Pruned nodes - Depth {depth} : {prunedNodes}")
                break                

        node.minmaxValue = value
        return value

# constructing a tree
# Depth 1 - MAX (root)
root = Node('Root')

# Depth 2 - MIN nodes
n1 = Node('B')
n2 = Node('C')
n3 = Node('D')
root.children = [n1, n2, n3]

# Depth 3 - MAX nodes
n4  = Node('E')
n5  = Node('F')
n6  = Node('G')
n7  = Node('H')
n8  = Node('I')
n9  = Node('J')
n10 = Node('K')
n11 = Node('L')
n12 = Node('M')
n1.children = [n4, n5, n6]
n2.children = [n7, n8, n9]
n3.children = [n10, n11, n12]

# Leaf nodes
n4.children  = [Node(5),  Node(3),  Node(8)]
n5.children  = [Node(2),  Node(7),  Node(1)]
n6.children  = [Node(9),  Node(4),  Node(6)]
n7.children  = [Node(3),  Node(8),  Node(5)]
n8.children  = [Node(2),  Node(7),  Node(4)]
n9.children  = [Node(9),  Node(1),  Node(6)]
n10.children = [Node(5),  Node(3),  Node(8)]
n11.children = [Node(2),  Node(7),  Node(4)]
n12.children = [Node(9),  Node(1),  Node(6)]

value = alphaBeta(root, -math.inf, math.inf, 3, True)
print("\nValue at root: ", value)
print("Total nodes: ", totalNodes)