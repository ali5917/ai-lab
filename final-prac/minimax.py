# An AI agent is developed to play a strategic turn-based combat game against an opponent. 
# In this environment, every decision leads to a possible battle outcome. 
# The opponent is assumed to always play optimally to minimize the AI's advantage.

# The AI agent uses the Minimax algorithm to determine the best possible strategy. 
# Instead of a traditional game tree, the game designer provides strategy cards, where each card represents a possible decision by the AI. 
# Each strategy card has two possible opponent responses, each leading to different outcomes.
# The AI acts as the MAX player, aiming to maximize its score.
# The opponent acts as the MIN player, aiming to minimize the AI's score.

# Strategy Cards (Game Outcomes):
# Card A: Opponent responses 7 or 3 
# Card B: Opponent responses 6 or 5 
# Card C: Opponent responses 9 or 1
# Card D: Opponent responses 5 or 11

# Tasks:
# (a) Explain how the given "strategy card" representation models a Minimax decision problem 
#     without using a tree structure. 
# (b) For each card, determine the optimal move of the opponent and justify your answer. 
# (c) Based on the results obtained in part(b) determine which strategy the AI (MAX player) should select.
# (d) Identify the final guaranteed payoff (utility value) for the AI agent. 
# (e) Explain why the Minimax algorithm assumes an optimal opponent 
#     and discuss one limitation of this assumption in real-world AI applications. 

import math

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []
        self.minmaxValue = None

class MinimaxAgent:
    def __init__(self, depth):
        self.depth = depth

    def formulateGoal(self, node):
        return "Goal reached" if node.minmaxValue is not None else "Searching"

    def act(self, node, environment):
        goalStatus = self.formulateGoal(node)
        if goalStatus == "Goal reached":
            return f"Minimax value for root node: {node.minmaxValue}"
        else:
            return environment.computeMinimax(node, self.depth)

class Environment:
    def __init__(self, tree):
        self.tree = tree
        self.computedNodes = []

    def getPercept(self, node):
        return node

    def computeMinimax(self, node, depth, maximizingPlayer=True):
        # base case: leaf node or max depth reached
        if depth == 0 or not node.children:
            self.computedNodes.append(node.value)
            return node.value

        if maximizingPlayer:
            value = -math.inf
            for child in node.children:
                childValue = self.computeMinimax(child, depth - 1, False)
                value = max(value, childValue)
            node.minmaxValue = value
            self.computedNodes.append(node.value)
            return value

        else:  # minimising player
            value = math.inf
            for child in node.children:
                childValue = self.computeMinimax(child, depth - 1, True)
                value = min(value, childValue)
            node.minmaxValue = value
            self.computedNodes.append(node.value)
            return value

def runAgent(agent, environment, startNode):
    percept = environment.getPercept(startNode)
    result = agent.act(percept, environment)
    print("Minimax value:", result)


# constructing the tree
# root = AI (MAX player)
# Card nodes = Opponent (MIN player)
# Leaf nodes = battle outcomes

root = Node('AI')

cardA = Node('Card A')
cardB = Node('Card B')
cardC = Node('Card C')
cardD = Node('Card D')
root.children = [cardA, cardB, cardC, cardD]

# Card A: responses 7 or 3
cardA.children = [Node(7), Node(3)]

# Card B: responses 6 or 5
cardB.children = [Node(6), Node(5)]

# Card C: responses 9 or 1
cardC.children = [Node(9), Node(1)]

# Card D: responses 5 or 11
cardD.children = [Node(5), Node(11)]

depth = 2   # root (MAX) -> card (MIN) -> outcome (leaf)
agent = MinimaxAgent(depth)
environment = Environment(root)
runAgent(agent, environment, root)

print("\nCard-level minimax values (opponent's best response per card):")
print("Card A:", cardA.minmaxValue)   # min(7,3)  = 3
print("Card B:", cardB.minmaxValue)   # min(6,5)  = 5
print("Card C:", cardC.minmaxValue)   # min(9,1)  = 1
print("Card D:", cardD.minmaxValue)   # min(5,11) = 5

print("\nAI's best strategy: Card B (or D) with guaranteed payoff:", root.minmaxValue)