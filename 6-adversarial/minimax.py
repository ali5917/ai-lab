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
        # checks if we already computed the answer
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
                childValue = self.computeMinimax(child, depth - 1, False)   # flip to minimiser
                value = max(value, childValue)
            node.minmaxValue = value
            self.computedNodes.append(node.value)
            return value

        else:  # minimising player
            value = math.inf                          
            for child in node.children:
                childValue = self.computeMinimax(child, depth - 1, True)    # flip to maximiser
                value = min(value, childValue)
            node.minmaxValue = value
            self.computedNodes.append(node.value)
            return value

def runAgent(agent, environment, startNode):
    percept = environment.getPercept(startNode)
    result = agent.act(percept, environment)
    print("Minimax value:", result)


# constructing a tree
root = Node('A')
n1 = Node('B')
n2 = Node('C')
root.children = [n1, n2]
n3 = Node('D')
n4 = Node('E')
n5 = Node('F')
n6 = Node('G')
n1.children = [n3, n4]
n2.children = [n5, n6]
n7 = Node(2)
n8 = Node(3)
n9 = Node(5)
n10 = Node(9)
n11 = Node(0)
n12 = Node(1)
n13 = Node(7)
n14 = Node(5)
n3.children = [n7, n8]
n4.children = [n9, n10]
n5.children = [n11, n12]
n6.children = [n13, n14]

depth = 3   # depth = number of edges from root to leaves
agent = MinimaxAgent(depth)
environment = Environment(root)
runAgent(agent, environment, root)
print("Order visited:", environment.computedNodes)
print("Minimax values:")
print("A:", root.minmaxValue)
print("B:", n1.minmaxValue)
print("C:", n2.minmaxValue)
print("D:", n3.minmaxValue)
print("E:", n4.minmaxValue)
print("F:", n5.minmaxValue)
print("G:", n6.minmaxValue)