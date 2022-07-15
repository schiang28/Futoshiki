from copy import deepcopy
from random import choice, shuffle
import numpy as np


class Game:

    EMPTY = " "

    def __init__(self):
        self._board = None
        self._grid_size = None
        self.__answer = None
        self.__fixed = None
        self.__moves = []

    # displays board to terminal
    def __repr__(self):
        display = "   ".join(str(i + 1) for i in range(self._grid_size)) + "\n"
        display += "----" * (self._grid_size - 1) + "--" + "\n"
        for row in range(len(self._board)):
            if row % 2 == 0:
                display += " ".join(self._board[row]) + " | " + str(row // 2 + 1) + "\n"
            else:
                display += " ".join(self._board[row]) + " | " + "\n"
        return display

    @property
    def get_board(self):
        return self._board

    def get_board_num(self, row, col):
        return self._board[row][col]

    def set_board(self, row, col, value):
        self.__moves.append((row, col, self._board[row][col]))
        self._board[row][col] = value

    @property
    def get_grid_size(self):
        return self._grid_size

    def set_grid_size(self, value):
        self._grid_size = value

    def show_answer(self):
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                self._board[row][col] = self.__answer[row][col]

    def create_grid(self, size, difficulty):
        self.__difficulty = difficulty
        self.__board_empty = np.full((size * 2 - 1, size * 2 - 1), Game.EMPTY)
        self.__cells = list(range((self._grid_size * 2 - 1) ** 2))
        self.__fill(self.__board_empty)
        self.__fill_inequalities()
        self.__generate()
        print(self.__removed)

        # changing of inequalities for displaying to gui
        for i in range(1, len(self.file), 2):
            for j in range(0, len(self.file[i]), 2):
                if self.file[i][j] == "<":
                    self.file[i][j] = "^"
                if self.file[i][j] == ">":
                    self.file[i][j] = "v"

        # list of cells that are fixed and cannot be changed by the user
        fixed = []
        for row in range(0, len(self.file), 2):
            for col in range(0, len(self.file[row]), 2):
                if self.file[row][col] != " ":
                    fixed.append((row // 2 + 1, col // 2 + 1))

        # board has to deepcopy as lists are mutable and board is 2d, have to convert from numpy to list
        self._board = (deepcopy(self.file)).tolist()
        self.__fixed = fixed

    def check(self):
        # return True if answer = current board
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                if self._board[row][col] != self.__answer[row][col]:
                    return False
        return True

    def is_valid(self, row, col, choice):
        # notifies the user that there is same number in row or grid or doesn't satisfy inequality
        if (row, col) not in self.__fixed:
            if choice not in self._board[row * 2 - 2] and choice not in [
                i[col * 2 - 2] for i in self._board
            ]:
                return True
            print("same number in row or column, so invalid move")
            return False
        print("tile is fixed, so invalid move")
        return False

    def play(self, row, col, choice):
        # choice of number is played to respective row and column, this play is appended to a stack of moves
        original = self._board[(row - 1) * 2][(col - 1) * 2]
        if choice != "x":
            self._board[(row - 1) * 2][(col - 1) * 2] = choice
        else:
            self._board[(row - 1) * 2][(col - 1) * 2] = Game.EMPTY
        print(f"played {choice} at {row},{col}")
        # moves contains three tuple of row, col, original
        self.__moves.append(((row - 1) * 2, (col - 1) * 2, original))

    def restart(self):
        # restarts puzzle by recopying original file
        self._board = (deepcopy(self.file)).tolist()
        self.__moves = []

    def undo(self):
        # undo move by popping from moves stack, if stack empty returns -1
        if len(self.__moves) > 0:
            undomove = self.__moves[-1]
            self._board[undomove[0]][undomove[1]] = undomove[2]
            self.__moves.pop()
            return 1
        else:
            return -1

    def mistakefound(self):
        # returns true if a mistake is found in player's entered answers. Ignores pencil markings and empty cells
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                if (
                    self._board[row][col] != self.__answer[row][col]
                    and self._board[row][col] != Game.EMPTY
                    and len(self._board[row][col]) == 1
                ):
                    return True
        return False

    def get_hint(self):
        # fills in a random non-filled in cell and adds it to moves stack, returns -1 if all cells filled in
        empty_cells = []
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                if (
                    self._board[row][col] == Game.EMPTY
                    and (row, col) not in self.__fixed
                ):
                    empty_cells.append((row, col))

        try:
            rand_cell = choice(empty_cells)
            rand_ans = self.__answer[rand_cell[0]][rand_cell[1]]
            self._board[rand_cell[0]][rand_cell[1]] = rand_ans
            self.__moves.append((rand_cell[0], rand_cell[1], Game.EMPTY))
            return 1
        except:
            return -1

    def save_puzzle(self):
        # saves completed puzzle to file
        file = open("puzzle.txt", "w")
        file.write("\n".join([",".join(i) for i in self.__answer]))
        file.close()

    def __possible(self, board, row, col, val):
        # checks if a value can be played at row and column of board by checking for duplicates and whether it satisfies inequality constraints
        for i in range(self._grid_size):
            if board[row][i * 2] == str(val) or board[i * 2][col] == str(val):
                return False

        # checking for inequalities
        if row > 0 and board[row - 2][col] != Game.EMPTY:
            if board[row - 1][col] == "<" and val < int(board[row - 2][col]):
                return False
            if board[row - 1][col] == ">" and val > int(board[row - 2][col]):
                return False
        if row < self._grid_size * 2 - 2 and board[row + 2][col] != Game.EMPTY:
            if board[row + 1][col] == "<" and val > int(board[row + 2][col]):
                return False
            if board[row + 1][col] == ">" and val < int(board[row + 2][col]):
                return False
        if col > 0 and board[row][col - 2] != Game.EMPTY:
            if board[row][col - 1] == "<" and val < int(board[row][col - 2]):
                return False
            if board[row][col - 1] == ">" and val > int(board[row][col - 2]):
                return False
        if col < self._grid_size * 2 - 2 and board[row][col + 2] != Game.EMPTY:
            if board[row][col + 1] == "<" and val > int(board[row][col + 2]):
                return False
            if board[row][col + 1] == ">" and val < int(board[row][col + 2]):
                return False

        return True

    def __fill(self, board):
        # fills in an initial empty board, to satisfy conditions of latin square
        numbers = list(range(1, self._grid_size + 1))
        for row in range(0, self._grid_size * 2, 2):
            for col in range(0, self._grid_size * 2, 2):
                if board[row][col] == Game.EMPTY:
                    shuffle(numbers)
                    for n in numbers:
                        if self.__possible(board, row, col, n):
                            board[row][col] = n
                            if Game.EMPTY in board[::2, ::2]:
                                self.__fill(board)
                                board[row][col] = Game.EMPTY
                            else:
                                self.__answer = np.copy(board)
                    return

    def __fill_inequalities(self):
        # fills in all inequality spaces of a full grid
        for row in range(0, len(self.__answer), 2):
            for col in range(0, len(self.__answer[row]), 2):
                if col + 3 <= len(self.__answer):
                    self.__answer[col + 1, row] = (
                        "<"
                        if self.__answer[col, row] < self.__answer[col + 2, row]
                        else ">"
                    )
                if row + 3 <= len(self.__answer):
                    self.__answer[col, row + 1] = (
                        "<"
                        if self.__answer[col, row] < self.__answer[col, row + 2]
                        else ">"
                    )

    def __solve(self, temp):
        # checks whether temporary grid is solvable, backtracking
        for row in range(0, len(self.__answer), 2):
            for col in range(0, len(self.__answer[row]), 2):
                if temp[row][col] == Game.EMPTY:
                    for n in range(1, self._grid_size + 1):
                        if self.__possible(temp, row, col, n):
                            temp[row][col] = n
                            self.__solve(temp)
                            if not (self.__end_solver):
                                temp[row][col] = Game.EMPTY
                    return
        self.__n_solutions += 1
        if self.__n_solutions == 2:
            self.__removed -= 1
            self.__end_solver = True

    def __generate(self):
        # generates puzzle by removing random values and inequalities one by one
        self.file = deepcopy(self.__answer)
        shuffle(self.__cells)
        if self.__difficulty == 1:
            diff = -20
        elif self.__difficulty == 2:
            diff = -10
        else:
            diff = 0

        for i in range(len(self.__cells) + diff):
            row = self.__cells[i] // (self._grid_size * 2 - 1)
            col = self.__cells[i] % (self._grid_size * 2 - 1)
            backup = self.file[row][col]
            self.file[row][col] = Game.EMPTY

            board_copy = np.copy(self.file)
            self.__n_solutions = 0
            self.__end_solver = False
            self.__solve(board_copy)

            if self.__n_solutions != 1:
                self.file[row][col] = backup


if __name__ == "__main__":
    pass
