import numpy as np
from random import randint, shuffle


def possible(board, row, col, val):
    for i in range(d):
        if board[row][i * 2] == str(val) or board[i * 2][col] == str(val):
            return False

    # checking for inequalities
    if row > 0 and board[row - 2][col] != " ":
        if board[row - 1][col] == "<" and val < board[row - 2][col]:
            return False
        if board[row - 1][col] == ">" and val > board[row - 2][col]:
            return False
    if row < d * 2 - 2 and board[row + 2][col] != " ":
        if board[row + 1][col] == "<" and val > board[row + 2][col]:
            return False
        if board[row + 1][col] == ">" and val < board[row + 2][col]:
            return False
    if col > 0 and board[row][col - 2] != " ":
        if board[row][col - 1] == "<" and val < board[row][col - 2]:
            return False
        if board[row][col - 1] == ">" and val > board[row][col - 2]:
            return False
    if col < d * 2 - 2 and board[row][col + 2] != " ":
        if board[row][col + 1] == "<" and val > board[row][col + 2]:
            return False
        if board[row][col + 1] == ">" and val < board[row][col + 2]:
            return False

    return True


def fill(board):
    global board_filled
    d = (len(board) + 1) // 2
    for row in range(0, d * 2, 2):
        for col in range(0, d * 2, 2):
            if board[row][col] == " ":
                shuffle(numbers)
                for n in numbers:
                    if possible(board, row, col, n):
                        board[row][col] = n
                        if " " in board[::2, ::2]:
                            fill(board)
                            board[row][col] = " "
                        else:
                            board_filled = np.copy(board)
                return


d = 4

# Utility variables
numbers = list(range(1, d + 1))
cells = list(range((d * 2 - 1) ** 2))
board_empty = np.full((d * 2 - 1, d * 2 - 1), " ")

# Fill randomly the empty board and complete it with the inequalities clues
fill(board_empty)
print("Filled board randomly generated:")
print(board_filled, "\n")

