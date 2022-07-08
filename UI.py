from abc import ABC, abstractmethod
from calendar import c
from turtle import width
from types import CellType
from Game import Game
from Colors import color
from tkinter import *


class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class Gui(Ui):
    # TODO: create futoshiki grid
    MARGIN = 20
    SIDE = 50

    with open("game1.txt") as f:
        file = [l.split(",") for l in f.read().splitlines()]

    def __init__(self):
        self.__game_win = None
        root = Tk()
        root.title("Futoshiki")
        root.geometry("500x500")
        frame = Frame(root)
        frame.pack()

        Button(frame, text="Play", command=self.__play_game, height=2, width=30).pack(
            fill=X
        )
        Button(frame, text="Quit", command=self.__quit, height=2).pack(fill=X)

        self.__root = root

    def __play_game(self):
        if self.__game_win:
            return

        self.__game = Game()
        game_win = Toplevel(self.__root)
        game_win.title("Puzzle")

        # geometry has to be a variable for different grid sizes
        game_win.geometry("600x400")
        self.__width = self.__height = Gui.MARGIN * 2 + Gui.SIDE * (
            self.__game.GRID_SIZE * 2 - 1
        )

        self.__canvas = Canvas(game_win, width=self.__width, height=self.__height)
        self.__canvas.pack(side=LEFT)

        self.__draw_grid()
        self.__draw_puzzle()

        self.__canvas.bind("<Button-1>", self.__cell_clicked)
        self.__canvas.bind("<Key>", self.__key_pressed)

        # stage 2.2 dismiss and check buttons on game window
        self.__game_win = game_win
        dismiss_button = Button(
            game_win, text="Dismiss", command=self.__dismiss_game_win
        )
        dismiss_button.pack(ipadx=10, ipady=10, expand=True)
        check_button = Button(game_win, text="Check", command=self.__check)
        check_button.pack(ipadx=10, ipady=10, expand=True)

    def __draw_grid(self):
        for row in range(self.__game.GRID_SIZE):
            for l in range(self.__game.GRID_SIZE * 2):
                # vertical lines
                x0 = Gui.MARGIN + l * Gui.SIDE
                y0 = Gui.MARGIN + Gui.SIDE * 2 * row
                x1 = Gui.MARGIN + l * Gui.SIDE
                y1 = Gui.MARGIN + Gui.SIDE * 2 * row + Gui.SIDE
                self.__canvas.create_line(x0, y0, x1, y1)

            for l in range(self.__game.GRID_SIZE):
                # horizontal lines
                x0 = Gui.MARGIN + l * 2 * Gui.SIDE
                y0 = Gui.MARGIN + Gui.SIDE * 2 * row
                x1 = Gui.MARGIN + l * 2 * Gui.SIDE + Gui.SIDE
                y1 = Gui.MARGIN + Gui.SIDE * 2 * row
                self.__canvas.create_line(x0, y0, x1, y1)
                self.__canvas.create_line(x0, y0 + Gui.SIDE, x1, y1 + Gui.SIDE)

    def __draw_puzzle(self):
        numbers = self.__game.file
        for row in range(len(numbers)):
            for col in range(len(numbers[row])):
                self.__canvas.create_text(
                    Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 2,
                    Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                    text=numbers[row][col],
                    tags="numbers",
                )

    def __cell_clicked(self, event):
        if self.__game.check():
            return

        x, y = event.x, event.y
        if (
            Gui.MARGIN < x < self.__width - Gui.MARGIN
            and Gui.MARGIN < y < self.__height - Gui.MARGIN
        ):
            self.__canvas.focus_set()

        self.__row, self.__col = (
            (y - Gui.MARGIN) // Gui.SIDE,
            (x - Gui.MARGIN) // Gui.SIDE,
        )
        self.__draw_cursor()

    def __draw_cursor(self):
        self.__canvas.delete("cursor")  # clears previous cursors
        # checks row and col in canvas and is a grid rather than in between grid, and if it is empty
        if (
            self.__row >= 0
            and self.__col >= 0
            and self.__row % 2 == 0
            and self.__col % 2 == 0
            and self.__game.file[self.__row][self.__col] == self.__game.EMPTY
        ):
            x0 = Gui.MARGIN + self.__col * Gui.SIDE + 1
            y0 = Gui.MARGIN + self.__row * Gui.SIDE + 1
            x1 = Gui.MARGIN + (self.__col + 1) * Gui.SIDE - 1
            y1 = Gui.MARGIN + (self.__row + 1) * Gui.SIDE - 1
            self.__canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    def __key_pressed(self):
        pass

    def __quit(self):
        self.__root.quit()

    def __dismiss_game_win(self):
        self.__game_win.destroy()
        self.__game_win = None

    def __check(self):
        pass

    def run(self):
        self.__root.mainloop()


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
            if self.__game.is_valid(row, col, choice):
                self.__game.play(row, col, choice)
        print(self.__game)
        print("puzzle correct!")
