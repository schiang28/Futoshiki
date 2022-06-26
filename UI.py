from abc import ABC, abstractmethod
from Game import Game


class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class Gui(Ui):
    def __init__(self):
        pass

    def run(self):
        pass


class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def __get_input(self):
        while True:
            try:
                row = int(input("Enter row: "))
                column = int(input("Enter column: "))
                if 1 <= row <= 4 and 1 <= column <= 4:
                    break
                else:
                    print("Invalid input. Please try again")
            except ValueError():
                print("invalid input")

        return row, column

    def run(self):
        print(self.__game)
        row, col = self.__get_input()
        print(row, col)
