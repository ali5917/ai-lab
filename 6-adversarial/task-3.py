'''
Task 3: Minimax with Depth Limit & Heuristic

Design a grid-based game (1D or 2D) where:
    Agent (Max) tries to reach a goal (+10 reward)
    Opponent (Min) tries to block (-10 penalty)

Implement Minimax with:
    Depth limit = 3
    Custom heuristic function (e.g., distance to goal)

Simulate at least 3 game state and print:
    Chosen move at each step
    Heuristic values at leaf nodes 

''' 

import math

rows = cols = 4
goal = (3, 3)

def heuristic(pos):
    return -(abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))

def getMoves(pos):
    moves = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        newPos = (pos[0] + dx, pos[1] + dy)
        if 0 <= newPos[0] < rows and 0 <= newPos[1] < cols:
            moves.append(newPos)
    return moves

leafValues = []

def minimax(state, depth, maximizing):
    agent, opp = state

    # Terminal checks
    if agent == goal:               # agent wins
        leafValues.append(10)
        return 10
    
    if agent == opp:                # agent blocked
        leafValues.append(-10)
        return -10

    if depth == 0:                  # search limit reached
        h = heuristic(agent)
        leafValues.append(h)
        return h

    if maximizing:
        value = -math.inf
        for move in getMoves(agent):
            childValue = minimax((move, opp), depth - 1, False)
            value = max(value, childValue)
        return value
    else:
        value = math.inf
        for move in getMoves(opp):
            childValue = minimax((agent, move), depth - 1, True)
            value = min(value, childValue)
        return value

def bestMove(state, depth, maximizing):
    agent, opp = state
    moves = getMoves(agent if maximizing else opp)
    
    values = []
    for m in moves:
        if maximizing:
            newState = (m, opp)
            value = minimax(newState, depth - 1, False)
        else:
            newState = (agent, m)
            value = minimax(newState, depth - 1, True)
        
        values.append(value)

    if maximizing:
        maxIndex = values.index(max(values))
        return moves[maxIndex]
    else:
        minIndex = values.index(min(values))
        return moves[minIndex]


startAgent = (0,0) 
startOpp = (3, 0)
state = (startAgent, startOpp)

for step in range(3):
    leafValues.clear() 
    
    print(f"\nStep {step+1}")
    print(f"Agent: {state[0]}  Opponent: {state[1]}")

    move = bestMove(state, depth=3, maximizing=True)
    state = (move, state[1])
    print(f"Agent moves → {move}")

    oppMove = bestMove(state, depth=3, maximizing=False)
    state = (state[0], oppMove)
    print(f"Opponent moves → {oppMove}")

    print("Leaf values:", leafValues)