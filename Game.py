from Colors import color


class Game:

    GRID_SIZE = 4
    EMPTY = " "

    with open("game1.txt") as f:
        file = [l.split(",") for l in f.read().splitlines()]
    for i in range(1, len(file), 2):
        for j in range(0, len(file[i]), 2):
            if file[i][j] == "<":
                file[i][j] = "^"
            if file[i][j] == ">":
                file[i][j] = "v"

    with open("game1ans.txt") as f:
        answer = [l.split(",") for l in f.read().splitlines()]

    fixed = []
    for row in range(0, len(file), 2):
        for col in range(0, len(file[row]), 2):
            if file[row][col] != " ":
                fixed.append((row // 2 + 1, col // 2 + 1))

    def __init__(self):
        self.__board = Game.file
        self.__answer = Game.answer
        self.__fixed = Game.fixed

    def __repr__(self):
        display = "   ".join(str(i + 1) for i in range(Game.GRID_SIZE)) + "\n"
        display += "----" * (Game.GRID_SIZE - 1) + "--" + "\n"
        for row in range(len(self.__board)):
            if row % 2 == 0:
                display += (
                    " ".join(self.__board[row]) + " | " + str(row // 2 + 1) + "\n"
                )
            else:
                display += " ".join(self.__board[row]) + " | " + "\n"
        return display

    @property
    def get_board(self):
        return self.__board

    def check(self):
        # return True if answer = current board
        for row in range(len(self.__board)):
            for col in range(len(self.__board[row])):
                if self.__board[row][col] != self.__answer[row][col] and (
                    self.__board[row][col] not in [">", "<", "^", "v"]
                    or self.__answer[row][col] not in [">", "<", "^", "v"]
                ):
                    return False
        return True

    def is_valid(self, row, col, choice):
        # notifies the user that there is same number in row or grid or doesn't satisfy inequality
        if (row, col) not in self.__fixed:
            if choice not in self.__board[row * 2 - 2] and choice not in [
                i[col * 2 - 2] for i in self.__board
            ]:
                return True
            print("same number in row or column, so invalid move")
            return False
        print("tile is fixed, so invalid move")
        return False

    def play(self, row, col, choice):
        if choice != "x":
            self.__board[(row - 1) * 2][(col - 1) * 2] = choice
        else:
            self.__board[(row - 1) * 2][(col - 1) * 2] = Game.EMPTY
        print(f"played {choice} at {row},{col}")


if __name__ == "__main__":
    pass
