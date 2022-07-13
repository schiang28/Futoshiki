from Colors import color
from copy import deepcopy
from random import choice


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
        self._board = deepcopy(self.__answer)

    def create_grid(self, size, difficulty):
        # different grid size and difficulties currently load from example files
        if size == 4:
            fileans = "game1ans.txt"
            if difficulty == 1:
                filename = "game1.txt"
            else:
                filename = "game1hard.txt"
        elif size == 5:
            fileans = "game2ans.txt"
            if difficulty == 1:
                filename = "game2easy.txt"
            else:
                filename = "game2hard.txt"
        elif size == 6:
            fileans = "game3ans.txt"
            if difficulty == 1:
                filename = "game3easy.txt"
            else:
                filename = "game3hard.txt"
        else:
            fileans = "game4ans.txt"
            if difficulty == 1:
                filename = "game4easy.txt"
            else:
                filename = "game4hard.txt"

        with open(filename) as f:
            file = [l.split(",") for l in f.read().splitlines()]
        # replacing inequalities orientation for displaying
        for i in range(1, len(file), 2):
            for j in range(0, len(file[i]), 2):
                if file[i][j] == "<":
                    file[i][j] = "^"
                if file[i][j] == ">":
                    file[i][j] = "v"

        with open(fileans) as f:
            answer = [l.split(",") for l in f.read().splitlines()]

        fixed = []
        for row in range(0, len(file), 2):
            for col in range(0, len(file[row]), 2):
                if file[row][col] != " ":
                    fixed.append((row // 2 + 1, col // 2 + 1))

        # board has to deepcopy as lists are mutable and board is 2d
        self.file = file
        self._board = deepcopy(self.file)
        self.__answer = answer
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


if __name__ == "__main__":
    pass
