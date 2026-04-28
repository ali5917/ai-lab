"""
Random Restart Hill Climbing for N-Queens:

- Solve N-Queens (N = 8 or 10) using state = list of column positions for each row

Implement:
1. Conflict calculation function:
2. Neighbor generation:
3. Hill Climbing search:
4. Random Restart:
   → If stuck in local optimum, generate a new random state
   → Repeat up to 20 restarts

- Print solution state if found
- Number of restarts used
"""

import random

def getConflicts(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j)):
                conflicts += 1

    return conflicts

def getNeighbours(state):
    n = len(state)
    neighbours = []
    for queen in range(n):
        for col in range(n):
            if (col != state[queen]):
                newState = list(state)
                newState[queen] = col
                neighbours.append(newState)
    return neighbours

def getRandomState(n):
    state = []
    for i in range(n):
        value = random.randint(0, n - 1)
        state.append(value)

    return state

def hillClimb (n):
    # random initial state
    currentState = getRandomState(n)

    currentConflicts = getConflicts(currentState)
    restarts = 0

    while True:
        neighbours = getNeighbours(currentState)
        nextState = None
        nextConflicts = currentConflicts
    
        # first better neighbour
        for i in neighbours:
            nConflicts = getConflicts(i)

            if nConflicts < currentConflicts:
                nextState = i
                nextConflicts = nConflicts
                break

        if currentConflicts == 0: break

        if nextConflicts >= currentConflicts:
            if restarts < 20:
                currentState = getRandomState(n)
                currentConflicts = getConflicts(currentState)
                restarts += 1
            else:
                break
        else:
            currentState = nextState
            currentConflicts = nextConflicts

    return currentState, currentConflicts, restarts

n = 10
solution, conflicts, restarts = hillClimb(n)

if conflicts == 0:
    print(f"Solution: {solution}")
    print(f"Conflicts: {conflicts} - Restarts: {restarts}")
else:
    print(f"Stuck at local optimum with {conflicts} conflicts - Restarts limit (20) reached.")