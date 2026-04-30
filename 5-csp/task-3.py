from ortools.sat.python import cp_model

"""
Sudoku: Fill a 9x9 grid so every row, column, and 3x3 box contains 1-9 with no repeats.
Variables: each cell (row, col) in the grid
Domain: 1-9 per cell (pre-filled cells are fixed to their given value)
Constraints: row uniqueness, column uniqueness, 3x3 box uniqueness
"""

# puzzle (0 = empty cell)
puzzle = [
    [5, 3, 0,  0, 7, 0,  0, 0, 0],
    [6, 0, 0,  1, 9, 5,  0, 0, 0],
    [0, 9, 8,  0, 0, 0,  0, 6, 0],

    [8, 0, 0,  0, 6, 0,  0, 0, 3],
    [4, 0, 0,  8, 0, 3,  0, 0, 1],
    [7, 0, 0,  0, 2, 0,  0, 0, 6],

    [0, 6, 0,  0, 0, 0,  2, 8, 0],
    [0, 0, 0,  4, 1, 9,  0, 0, 5],
    [0, 0, 0,  0, 8, 0,  0, 7, 9]
]

model = cp_model.CpModel()

# assigning domain to each cell (1-9)
cellVars = []
for r in range(9):
    row = []
    for c in range(9):
        row.append(model.new_int_var(1, 9, f'cell_{r}_{c}'))
    cellVars.append(row)

# fix pre-filled cells to their given value
for r in range(9):
    for c in range(9):
        if puzzle[r][c] != 0:
            model.add(cellVars[r][c] == puzzle[r][c])

# constraint: each row must contain unique values
for r in range(9):
    model.add_all_different(cellVars[r])

# constraint: each column must contain unique values
for c in range(9):
    col = []
    for r in range(9):
        col.append(cellVars[r][c])
    model.add_all_different(col)

# constraint: each 3x3 box must contain unique values
for boxRow in range(3):
    for boxCol in range(3):
        box = []
        for r in range(boxRow * 3, boxRow * 3 + 3):
            for c in range(boxCol * 3, boxCol * 3 + 3):
                box.append(cellVars[r][c])
        model.add_all_different(box)

solver = cp_model.CpSolver()
status = solver.solve(model)

# pretty print helper
def printSudoku(grid):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("  ---------------------")
        rowStr = "  "
        for c in range(9):
            if c % 3 == 0 and c != 0:
                rowStr += "| "
            rowStr += str(grid[r][c]) + " "
        print(rowStr)

# output
print("Original puzzle (0 = empty):")
printSudoku(puzzle)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("\nSolved puzzle:")
    solved = []
    for r in range(9):
        row = []
        for c in range(9):
            row.append(solver.value(cellVars[r][c]))
        solved.append(row)
    printSudoku(solved)
else:
    print("no solution found.")