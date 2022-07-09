from Colors import color
from copy import deepcopy


class Game:

    EMPTY = " "

    def __init__(self):
        self._board = None
        self._grid_size = None
        self.__answer = None
        self.__fixed = None

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

    def set_board(self, row, col, value):
        self._board[row][col] = value

    @property
    def get_grid_size(self):
        return self._grid_size

    def set_grid_size(self, value):
        self._grid_size = value

    def create_grid(self, size, difficulty):
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

        with open(filename) as f:
            file = [l.split(",") for l in f.read().splitlines()]
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

        self.file = file
        self._board = deepcopy(self.file)
        self.__answer = answer
        self.__fixed = fixed

    def check(self):
        # return True if answer = current board
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] != self.__answer[row][col] and (
                    self._board[row][col] not in [">", "<", "^", "v"]
                    or self.__answer[row][col] not in [">", "<", "^", "v"]
                ):
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
        if choice != "x":
            self._board[(row - 1) * 2][(col - 1) * 2] = choice
        else:
            self._board[(row - 1) * 2][(col - 1) * 2] = Game.EMPTY
        print(f"played {choice} at {row},{col}")


if __name__ == "__main__":
    pass
