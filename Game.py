from telnetlib import GA
from Colors import color
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
        # different grid size and difficulties currently load from example files
        self.__numbers = list(range(1, size + 1))
        self.__board_empty = np.full((size * 2 - 1, size * 2 - 1), Game.EMPTY)
        self.__fill(self.__board_empty)
        self.__fill_inequalities()

        self.__temp = deepcopy(self.__answer)
        self.__cells = list(range((self._grid_size * 2 - 1) ** 2))
        self.__generate(self.__answer)
        file = deepcopy(self.__answer)

        for i in range(1, len(file), 2):
            for j in range(0, len(file[i]), 2):
                if file[i][j] == "<":
                    file[i][j] = "^"
                if file[i][j] == ">":
                    file[i][j] = "v"

        fixed = []
        for row in range(0, len(file), 2):
            for col in range(0, len(file[row]), 2):
                if file[row][col] != " ":
                    fixed.append((row // 2 + 1, col // 2 + 1))

        # board has to deepcopy as lists are mutable and board is 2d
        self.file = deepcopy(file)
        self._board = deepcopy(self.file)
        self.__answer = deepcopy(self.__temp)
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
        original = self._board[(row - 1) * 2][(col - 1) * 2]
        if choice != "x":
            self._board[(row - 1) * 2][(col - 1) * 2] = choice
        else:
            self._board[(row - 1) * 2][(col - 1) * 2] = Game.EMPTY
        print(f"played {choice} at {row},{col}")
        # moves contains three tuple of row, col, original
        self.__moves.append(((row - 1) * 2, (col - 1) * 2, original))

    def restart(self):
        self._board = deepcopy(self.file)
        self.__moves = []

    def undo(self):
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
        file = open("puzzle.txt", "w")
        file.write("\n".join([",".join(i) for i in self.__answer]))
        file.close()

    def __possible(self, board, row, col, val):
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
        for row in range(0, self._grid_size * 2, 2):
            for col in range(0, self._grid_size * 2, 2):
                if board[row][col] == Game.EMPTY:
                    shuffle(self.__numbers)
                    for n in self.__numbers:
                        if self.__possible(board, row, col, n):
                            board[row][col] = n
                            if Game.EMPTY in board[::2, ::2]:
                                self.__fill(board)
                                board[row][col] = Game.EMPTY
                            else:
                                self.__answer = np.copy(board)
                    return

    def __fill_inequalities(self):
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                try:
                    self.__answer[col * 2 + 1, row * 2] = (
                        "<"
                        if self.__answer[col * 2, row * 2]
                        < self.__answer[col * 2 + 2, row * 2]
                        else ">"
                    )
                except IndexError:
                    pass
                try:
                    self.__answer[col * 2, row * 2 + 1] = (
                        "<"
                        if self.__answer[col * 2, row * 2]
                        < self.__answer[col * 2, row * 2 + 2]
                        else ">"
                    )
                except IndexError:
                    pass

    def __solve(self, board):
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                if board[row * 2][col * 2] == Game.EMPTY:
                    for n in range(1, self._grid_size + 1):
                        if self.__possible(board, row * 2, col * 2, n):
                            board[row * 2][col * 2] = n
                            self.__solve(board)
                            if not (self.__end_solver):
                                board[row * 2][col * 2] = Game.EMPTY
                    return
        self.__n_solutions += 1
        if self.__n_solutions == 2:
            self.__end_solver = True

    def __generate(self, board):
        shuffle(self.__cells)
        for i in range((self._grid_size * 2 - 1) ** 2):
            row = self.__cells[i] // (self._grid_size * 2 - 1)
            col = self.__cells[i] % (self._grid_size * 2 - 1)
            backup = board[row][col]
            board[row][col] = Game.EMPTY
            board_copy = np.copy(board)
            self.__n_solutions = 0
            self.__end_solver = False
            self.__solve(board_copy)
            if self.__n_solutions != 1:
                board[row][col] = backup


if __name__ == "__main__":
    pass
