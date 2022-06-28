from abc import ABC, abstractmethod
from Game import Game
from Colors import color


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
                if 1 <= row <= Game.GRID_SIZE and 1 <= column <= Game.GRID_SIZE:
                    break
                else:
                    print("Invalid input. Please try again")
            except ValueError():
                print("invalid input")

        while True:
            choice = input("Enter number to play or x to clear: ")
            if choice == "x":
                break
            try:
                if 1 <= int(choice) <= Game.GRID_SIZE:
                    break
                else:
                    print("Invalid input. Please try again")
            except:
                print("invalid input")

        return row, column, choice

    def run(self):
        while not self.__game.check():
            print(self.__game)
            row, col, choice = self.__get_input()
            self.__game.play(row, col, choice)
        print(self.__game)
        print("puzzle correct!")
