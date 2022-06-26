class Game:
    # reads pre loaded puzzle from text file
    with open("game1.txt") as f:
        file = [l.split(",") for l in f.read().splitlines()]
    for i in range(1, len(file), 2):
        for j in range(0, len(file[i]), 2):
            if file[i][j] == "<":
                file[i][j] = "^"
            if file[i][j] == ">":
                file[i][j] = "v"

    def __init__(self):
        self.__board = Game.file

    def __repr__(self):
        display = ""
        for row in range(len(self.__board)):
            display += f"{self.__board[row]} \n"
        return display

    def play(self, row, col):
        pass

    @property
    def winner(self):
        pass


if __name__ == "__main__":
    pass
