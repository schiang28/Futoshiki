from abc import ABC, abstractmethod
from Game import Game
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
        self.__game.set_grid_size(5)
        # needs to be variables eventually
        self.__game.create_grid(5, 1)

        game_win = Toplevel(self.__root)
        game_win.title("Puzzle")

        # geometry has to be a variable for different grid sizes
        game_win.geometry("800x500")
        self.__width = self.__height = Gui.MARGIN * 2 + Gui.SIDE * (
            self.__game.get_grid_size * 2 - 1
        )

        console = Text(game_win, height=1, width=50)
        console.tag_configure("center", justify="center")
        console.pack(side=TOP)
        console.configure(state="disabled")
        self.__console = console

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
        for row in range(self.__game.get_grid_size):
            for l in range(self.__game.get_grid_size * 2):
                # vertical lines
                x0 = Gui.MARGIN + l * Gui.SIDE
                y0 = Gui.MARGIN + Gui.SIDE * 2 * row
                x1 = Gui.MARGIN + l * Gui.SIDE
                y1 = Gui.MARGIN + Gui.SIDE * 2 * row + Gui.SIDE
                self.__canvas.create_line(x0, y0, x1, y1)

            for l in range(self.__game.get_grid_size):
                # horizontal lines
                x0 = Gui.MARGIN + l * 2 * Gui.SIDE
                y0 = Gui.MARGIN + Gui.SIDE * 2 * row
                x1 = Gui.MARGIN + l * 2 * Gui.SIDE + Gui.SIDE
                y1 = Gui.MARGIN + Gui.SIDE * 2 * row
                self.__canvas.create_line(x0, y0, x1, y1)
                self.__canvas.create_line(x0, y0 + Gui.SIDE, x1, y1 + Gui.SIDE)

    def __draw_puzzle(self):
        self.__canvas.delete("numbers")
        numbers = self.__game.get_board
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

    def __key_pressed(self, event):
        if self.__game.check():
            return

        if (
            self.__row >= 0
            and self.__col >= 0
            and self.__row % 2 == 0
            and self.__col % 2 == 0
            and self.__game.file[self.__row][self.__col] == self.__game.EMPTY
            and (event.char in "123456789" or event.keysym == "BackSpace")
        ):
            if event.char in "123456789":
                self.__game.set_board(self.__row, self.__col, str(int(event.char)))
            else:
                self.__game.set_board(self.__row, self.__col, self.__game.EMPTY)

            if self.__game.check():
                self.__complete()
            self.__draw_puzzle()
            self.__draw_cursor()

    def __quit(self):
        self.__root.quit()

    def __dismiss_game_win(self):
        self.__game_win.destroy()
        self.__game_win = None

    def __complete(self):
        self.__console.configure(state="normal")
        self.__console.insert(END, "puzzle correct!")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

    def __check(self):
        pass

    def run(self):
        self.__root.mainloop()


class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def __get_grid_settings(self):
        while True:
            try:
                size = int(input("Enter prefered grid size: "))
                if 4 <= size <= 7:
                    break
                else:
                    print("not valid grid size")
            except:
                print("invalid input")

        while True:
            try:
                difficulty = int(input("Enter difficulty; 1 for easy, 2 for hard: "))
                if 1 <= difficulty <= 2:
                    break
                else:
                    print("not valid difficulty input")
            except:
                print("invalid input")

        return size, difficulty

    def __get_input(self):
        while True:
            try:
                row = int(input("Enter row: "))
                column = int(input("Enter column: "))
                if (
                    1 <= row <= self.__game.get_grid_size
                    and 1 <= column <= self.__game.get_grid_size
                ):
                    break
                else:
                    print("Invalid input. Please try again")
            except:
                print("invalid input")

        while True:
            choice = input("Enter number to play or x to clear: ")
            if choice == "x":
                break
            try:
                if 1 <= int(choice) <= self.__game.get_grid_size:
                    break
                else:
                    print("Invalid input. Please try again")
            except:
                print("invalid input")

        return row, column, choice

    def __get_option(self):
        while True:
            choice = input(
                "enter to continue, or r:restart, u:undo, c:check for mistakes"
            )
            if choice in ["", "r", "u", "c"]:
                break
            else:
                print("invalid input")
        return choice

    def run(self):
        size, difficulty = self.__get_grid_settings()
        self.__game.set_grid_size(size)
        self.__game.create_grid(size, difficulty)

        while not self.__game.check():
            print(self.__game)

            choice = self.__get_option()
            if choice == "r":
                self.__game.restart()
                continue
            elif choice == "u":
                self.__game.undo()
                continue
            elif choice == "c":
                if self.__game.mistakefound():
                    print("mistake is found")
                else:
                    print("no mistakes found")
                continue

            row, col, choice = self.__get_input()
            if self.__game.is_valid(row, col, choice):
                self.__game.play(row, col, choice)

        print(self.__game)
        print("puzzle correct!")
