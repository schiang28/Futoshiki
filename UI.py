from abc import ABC, abstractmethod
from Game import Game
from tkinter import *


class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class Gui(Ui):
    MARGIN = 20
    SIDE = 50

    with open("game1.txt") as f:
        file = [l.split(",") for l in f.read().splitlines()]

    def __init__(self):
        self.__game_win = None
        self.__help_win = None
        self.__login_win = None
        self.__opt_win = None

        root = Tk()
        root.title("Futoshiki")
        root.geometry("500x500")
        frame = Frame(root)
        frame.pack()

        Button(
            frame, text="Play", command=self.__select_options, height=2, width=25
        ).pack()
        Button(frame, text="Login", command=self.__login, height=2).pack(fill=X)
        Button(frame, text="Help", command=self.__help, height=2).pack(fill=X)
        Button(frame, text="Quit", command=self.__quit, height=2).pack(fill=X)

        self.__root = root

    def __play_game(self):
        if self.__game_win:
            return

        self.__game = Game()
        self.__game.set_grid_size(self.__size)
        self.__game.create_grid(self.__size, self.__difficulty)

        game_win = Toplevel(self.__root)
        game_win.title("Puzzle")

        x, y = str(200 * self.__size), str(self.__size * 100 + 100)
        game_win.geometry(x + "x" + y)
        self.__width = self.__height = Gui.MARGIN * 2 + Gui.SIDE * (
            self.__game.get_grid_size * 2 - 1
        )

        console = Text(game_win, height=1, width=50)
        console.tag_configure("center", justify="center")
        console.pack(side=TOP)
        console.configure(state="disabled")
        self.__console = console

        self.__canvas = Canvas(game_win, width=self.__width, height=self.__height)
        self.__canvas.pack(side=LEFT, padx=(20, 0))

        self.__draw_grid()
        self.__draw_puzzle()

        self.__canvas.bind("<Button-1>", self.__cell_clicked)
        self.__canvas.bind("<Key>", self.__key_pressed)

        # stage 2.2 dismiss and check buttons on game window
        self.__game_win = game_win
        dismiss_button = Button(
            game_win, text="Dismiss", command=self.__dismiss_game_win, width=10
        )
        dismiss_button.pack(ipadx=10, ipady=10, expand=True)
        check_button = Button(game_win, text="Check", command=self.__check, width=10)
        check_button.pack(ipadx=10, ipady=10, expand=True)
        restart_button = Button(
            game_win, text="Restart", command=self.__restart, width=10
        )
        restart_button.pack(ipadx=10, ipady=10, expand=True)
        undo_button = Button(game_win, text="Undo", command=self.__undo, width=10)
        undo_button.pack(ipadx=10, ipady=10, expand=True)
        answer_button = Button(game_win, text="Answer", command=self.__answer, width=10)
        answer_button.pack(ipadx=10, ipady=10, expand=True)
        hint_button = Button(game_win, text="Hint", command=self.__hint, width=10)
        hint_button.pack(ipadx=10, ipady=10, expand=True)
        save_button = Button(game_win, text="Save", command=self.__save, width=10)
        save_button.pack(ipadx=10, ipady=10, expand=True)

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
                if len(numbers[row][col]) == 1:
                    self.__canvas.create_text(
                        Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 2,
                        Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                        text=numbers[row][col],
                        tags="numbers",
                        font=("Arial", 15),
                    )
                else:
                    # CALCULATIONS FOR PENCIL MARKINGS
                    for i in numbers[row][col]:
                        if i == "1":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        elif i == "2":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 2,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        elif i == "3":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + 5 * Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        elif i == "4":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        elif i == "5":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 2,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        elif i == "6":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + 5 * Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        else:
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + 5 * Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
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
            and (event.char in "1234567" or event.keysym == "BackSpace")
        ):
            if event.char in "1234567":
                # allows user to type in multiple numbers
                num = self.__game.get_board_num(self.__row, self.__col)
                if event.char not in num:
                    self.__game.set_board(
                        self.__row, self.__col, (num + str(event.char)).strip()
                    )
            else:
                self.__game.set_board(self.__row, self.__col, self.__game.EMPTY)

            if self.__game.check():
                self.__complete()
            self.__draw_puzzle()
            self.__draw_cursor()

    def __login(self):
        # don't open if game, option of login window already open
        if self.__login_win or self.__game_win or self.__opt_win:
            return

        login_win = Toplevel(self.__root)
        login_win.title("Login")
        login_win.geometry("400x400")
        self.__login_win = login_win

        # allows user to enter uername and password text boxes
        Label(login_win, text="Username:").pack(side=TOP, pady=(50, 0))
        username = StringVar()
        Entry(login_win, textvariable=username).pack(side=TOP)
        Label(login_win, text="Password:").pack(side=TOP)
        password = StringVar()
        Entry(login_win, textvariable=password).pack(side=TOP)

        dismiss_button = Button(
            login_win,
            text="Dismiss",
            command=self.__dismiss_login_win,
            width=20,
            height=2,
        )
        dismiss_button.pack(side=BOTTOM)

        newacc_button = Button(
            login_win, text="Create New Account", command=None, width=20, height=2
        )
        newacc_button.pack(side=BOTTOM)

        enter_button = Button(login_win, text="Enter", command=None, width=20, height=2)
        enter_button.pack(side=BOTTOM)

    def __help(self):
        if self.__help_win:
            return

        help_win = Toplevel(self.__root)
        help_win.title("Help")
        help_win.geometry("400x400")
        self.__help_win = help_win

        with open("rules.txt") as f:
            rules = f.read()

        text = Text(help_win)
        text.pack(expand=True, fill="both")
        text.insert(END, rules)
        text.configure(state="disabled")

        dismiss_button = Button(
            help_win,
            text="Dismiss",
            command=self.__dismiss_help_win,
            width=10,
            height=2,
        )
        dismiss_button.pack(side=BOTTOM)

    def __select_options(self):
        if self.__opt_win or self.__game_win or self.__login_win:
            return

        opt_win = Tk()
        opt_win.title("Configure Grid Settings")
        opt_win.geometry("400x400")
        self.__opt_win = opt_win

        # drop down menus for grid size and difficulty
        Label(opt_win, text="Please select grid size:").pack(side=TOP, pady=(50, 0))
        self.__size = StringVar(opt_win)
        self.__size.set("4x4")
        OptionMenu(opt_win, self.__size, "4x4", "5x5", "6x6", "7x7").pack(side=TOP)

        Label(opt_win, text="Please select difficulty:").pack(side=TOP)
        self.__difficulty = StringVar(opt_win)
        self.__difficulty.set("1. easy")
        OptionMenu(opt_win, self.__difficulty, "1. easy", "2. hard").pack(side=TOP)

        dismiss_button = Button(
            opt_win, text="Dismiss", command=self.__dismiss_opt_win, width=10, height=2,
        )
        dismiss_button.pack(side=BOTTOM)

        done_button = Button(
            opt_win, text="Done", command=self.__configured, width=10, height=2,
        )
        done_button.pack(side=BOTTOM)

    def __configured(self):
        # gets what is in the drop down menus, parsing
        self.__size = int(self.__size.get()[0])
        self.__difficulty = int(self.__difficulty.get()[0])
        self.__opt_win.destroy()
        self.__opt_win = None
        self.__play_game()

    def __quit(self):
        self.__root.quit()

    def __dismiss_game_win(self):
        self.__game_win.destroy()
        self.__game_win = None

    def __dismiss_help_win(self):
        self.__help_win.destroy()
        self.__help_win = None

    def __dismiss_login_win(self):
        self.__login_win.destroy()
        self.__login_win = None

    def __dismiss_opt_win(self):
        self.__opt_win.destroy()
        self.__opt_win = None

    def __complete(self):
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.insert(END, "puzzle correct!")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

    def __check(self):
        if self.__game.check():
            return

        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)

        mistake = self.__game.mistakefound()
        if mistake:
            self.__console.insert(END, "mistakes found")
        else:
            self.__console.insert(END, "no mistakes found")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

    def __restart(self):
        self.__game.restart()
        self.__draw_puzzle()
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.configure(state="disabled")

    def __undo(self):
        if self.__game.check():
            return

        if self.__game.undo() > 0:
            self.__draw_puzzle()
        else:
            self.__console.configure(state="normal")
            self.__console.delete("1.0", END)
            self.__console.insert(END, "no moves to undo")
            self.__console.tag_add("center", "1.0", "end")
            self.__console.configure(state="disabled")

    def __answer(self):
        if self.__game.check():
            return

        self.__game.show_answer()
        self.__draw_puzzle()
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.insert(END, "solution to puzzle:")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

    def __hint(self):
        if self.__game.check():
            return

        if self.__game.get_hint() > 0:
            self.__draw_puzzle()
        else:
            self.__console.configure(state="normal")
            self.__console.delete("1.0", END)
            self.__console.insert(END, "hints can only be used on empty cells")
            self.__console.tag_add("center", "1.0", "end")
            self.__console.configure(state="disabled")

        if self.__game.check():
            self.__complete()

    def __save(self):
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        if not self.__game.check():
            self.__console.insert(END, "can only save is puzzle is completed")
            self.__console.tag_add("center", "1.0", "end")
            self.__console.configure(state="disabled")
            return
        self.__game.save_puzzle()
        self.__console.insert(END, "saved puzzle")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

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
                "enter to continue, or r:restart, u:undo, c:check for mistakes, a:see answer and quit"
            )
            if choice in ["", "r", "u", "c", "a"]:
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
                if self.__game.undo() < 0:
                    print("no moves to undo")
                continue
            elif choice == "c":
                if self.__game.mistakefound():
                    print("mistake is found")
                else:
                    print("no mistakes found")
                continue
            elif choice == "a":
                print("solution to puzzle: ")
                self.__game.show_answer()
                print(self.__game)
                quit()

            row, col, choice = self.__get_input()
            if self.__game.is_valid(row, col, choice):
                self.__game.play(row, col, choice)

        print(self.__game)
        print("puzzle correct!")
