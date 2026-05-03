'''
Implement a Tic-Tac-Toe AI Agent where AI = Max player (X), Human = Min player (O)

Implement:
    Alpha-Beta pruning algorithm
    Game board (3x3)

AI should:
    Always play optimally
    Never lose (win or draw guaranteed)

Display:
    Game tree depth explored
    Moves pruned during execution

'''

import math

board = [' '] * 9

nodesExplored = 0
prunedCount = 0

# winning combinations
wins = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def printBoard():
    print()
    for i in range(0, 9, 3):
        print(board[i], "|", board[i+1], "|", board[i+2])
    print() 

def checkWinner():
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]

    if " " not in board:
        return "Draw"
    return None

def getMoves():
    moves = []
    for i in range(9):
        if board[i] == " ":
            moves.append(i)
            
    return moves

def alphaBeta(depth, alpha, beta, maximizing):
    global nodesExplored, prunedCount
    nodesExplored += 1

    result = checkWinner()
    if result == "X":
        return 10
    elif result == "O":
        return -10
    elif result == "Draw":
        return 0

    if maximizing:
        value = -math.inf
        moves = getMoves()

        for i, move in enumerate(moves):
            board[move] = "X"
            childValue = alphaBeta(depth + 1, alpha, beta, False)
            value = max(value, childValue)

            board[move] = " "

            alpha = max(alpha, value)
            if alpha >= beta:
                prunedCount += len(moves) - i - 1
                break

        return value

    else:
        value = math.inf
        moves = getMoves()

        for i, move in enumerate(moves):
            board[move] = "O"
            childValue = alphaBeta(depth + 1, alpha, beta, True)
            value = min(value, childValue)

            board[move] = " "

            beta = min(beta, value)
            if alpha >= beta:
                prunedCount += len(moves) - i - 1
                break

        return value

def bestMove():
    moves = getMoves()
    values = []
    for move in moves:
        board[move] = "X"
        value = alphaBeta(0, -math.inf, math.inf, False)
        values.append(value)
        board[move] = " "

    maxIndex = values.index(max(values))
    return moves[maxIndex] 

print("Tic-Tac-Toe: Human (O) vs AI (X)")
while True:
    printBoard()

    # Human move
    user = int(input("Enter position (0-8): "))
    if board[user] != " ":
        print("Invalid move!")
        continue
    board[user] = "O"

    if checkWinner():
        break

    # AI move
    move = bestMove()
    board[move] = "X"
    print(f"AI plays at {move}")

    if checkWinner():
        break

printBoard()

result = checkWinner()
if result == "X":
    print("AI Wins!")
elif result == "Draw":
    print("Match Drawn!")
else:
    print("Human Wins!")

print("Nodes explored:", nodesExplored)
print("Moves pruned:", prunedCount)