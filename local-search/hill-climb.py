"""
Hill Climbing starts with a random solution and keeps improving it by moving to a better neighbor.

N-Queens Representation:

- State = list of size N
  Example (N=4): [1, 3, 0, 2]
  Index = row
  Value = column of queen

Heuristic Function:
- h(n) = number of attacking queen pairs
- Goal: h(n) = 0 (no conflicts)

Simple Hill Climbing:

1. Generate a random initial state.
2. Compute its heuristic (conflicts).
3. Repeat:
    a. Generate all neighbors.
    b. Find the first neighbor with fewer conflicts.
    c. If found → move to that neighbor.
    d. If no better neighbor → STOP (local optimum).
4. Return the current state.
"""

# 1. Heuristic Function (Counts number of attacking queen pairs)
import random

def calculate_conflicts(state): 
    conflicts = 0
    n = len(state)
    
    for i in range(n):
        for j in range(i + 1, n):
            # same column or diagonal
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
                
    return conflicts

# 2. Generate all possible neighbors by moving one queen
def get_neighbors(state):
    neighbors = []
    n = len(state)
    
    for row in range(n):
        for col in range(n):
            if col != state[row]:  # skip current position
                new_state = list(state)
                new_state[row] = col
                neighbors.append(new_state)
                
    return neighbors

# 3. Simple Hill Climbing
def simple_hill_climbing(n): 
    # random initial state  
    current_state = [random.randint(0, n - 1) for _ in range(n)] 
    current_conflicts = calculate_conflicts(current_state) 
    
    while True:
        neighbors = get_neighbors(current_state)
        next_state = None
        next_conflicts = current_conflicts
        
        # find first better neighbor
        for neighbor in neighbors:
            neighbor_conflicts = calculate_conflicts(neighbor)
            
            if neighbor_conflicts < next_conflicts:
                next_state = neighbor
                next_conflicts = neighbor_conflicts
                break 
        
        # stop if no improvement
        if next_conflicts >= current_conflicts:
            break
        
        current_state = next_state
        current_conflicts = next_conflicts
    
    return current_state, current_conflicts

n = 8 
solution, conflicts = simple_hill_climbing(n)

if conflicts == 0:
    print(f"Solution found for {n}-Queens:")
    print(solution)
else:
    print(f"Stuck at local optimum with {conflicts} conflicts:")
    print(solution)