from abc import ABC, abstractmethod
from Game import Game
from tkinter import *
import sqlite3
import time as time
import hashlib

try:
    # try connecting to the database if it exists
    f = open("userdatabase.db")
    conn = sqlite3.connect("userdatabase.db")
    cursor = conn.cursor()
except IOError:

    ##########################
    # Group A                #
    # Complex Database Model #
    ##########################
    
    conn = sqlite3.connect("userdatabase.db")
    cursor = conn.cursor()

    # create table of users containing information such as username, password, number of games, completed games and times
    cursor.execute(
        """CREATE TABLE users (
                    username text,
                    password text,
                    games integer,
                    completed integer,
                    timer real
                    )"""
    )

    # create table of puzzles including gameid, time to complete the game, grid size and difficulty
    cursor.execute(
        """CREATE TABLE puzzles (
                    gameid integer,
                    time real,
                    grid_size integer,
                    difficulty text
                    )"""
    )

    # create tables with each gamid and its corresponding user
    cursor.execute(
        """CREATE TABLE savedgames (
                    username text,
                    gameid integer
                    )"""
    )
    ### joining table with gameid and userid as primary key / foreign key
    conn.commit()


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
        self.__register_win = None
        self.__logged_in = False
        self.__stats_win = None
        self.__set_win = None
        self.__timer = False
        self.__backgroundcol = "white"

        # main menu screen gui
        root = Tk()
        root.title("Futoshiki")
        root.geometry("500x500")
        frame = Frame(root)
        frame.pack()

        # Buttons that appear on the main page
        Button(
            frame, text="Play", command=self.__select_options, height=2, width=25
        ).pack()
        Button(frame, text="Login", command=self.__login, height=2).pack(fill=X)
        Button(frame, text="Logout", command=self.__logout, height=2).pack(fill=X)
        Button(frame, text="Help", command=self.__help, height=2).pack(fill=X)
        Button(frame, text="Stats", command=self.__stats, height=2).pack(fill=X)
        Button(frame, text="Settings", command=self.__settings, height=2).pack(fill=X)
        Button(frame, text="Quit", command=self.__quit, height=2).pack(fill=X)

        console = Text(frame, height=1, width=25)
        console.tag_configure("center", justify="center")
        console.pack(side=TOP)
        console.configure(state="disabled")
        self.__menu_console = console

        self.__root = root

    def __play_game(self):
        if self.__game_win:
            return

        
        ###################################
        # Group A                         #
        # Dynamic Generation of an Object #
        ###################################

        self.__game = Game()
        self.__game.set_grid_size(self.__size)
        self.__game.create_grid(self.__size, self.__difficulty)

        game_win = Toplevel(self.__root)
        game_win.title("Puzzle")
        game_win.configure(background=self.__backgroundcol)

        # calculates appropriate sized window
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

        # additional buttons and features when playing in the game window
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


        ############################
        # GROUP A                  #
        # Aggregate SQL Functions  #
        ############################

        # if user is logged in, stats are updates when a game is played
        if self.__logged_in:
            # if the user is logged in, an SQL query will be made to increment the number of games played by 1
            conn.execute(
                """UPDATE users SET games = games+1 WHERE username=?""", (self.__user,),
            )
            conn.commit()

        # starts timer
        if self.__timer and self.__logged_in:
            self.__start = time.time()

    # method that draws grid of puzzle
    def __draw_grid(self):
        for row in range(self.__game.get_grid_size):
            for l in range(self.__game.get_grid_size * 2):
                # draws vertical lines
                x0 = Gui.MARGIN + l * Gui.SIDE
                y0 = Gui.MARGIN + Gui.SIDE * 2 * row
                x1 = Gui.MARGIN + l * Gui.SIDE
                y1 = Gui.MARGIN + Gui.SIDE * 2 * row + Gui.SIDE
                self.__canvas.create_line(x0, y0, x1, y1)

            for l in range(self.__game.get_grid_size):
                # draws horizontal lines
                x0 = Gui.MARGIN + l * 2 * Gui.SIDE
                y0 = Gui.MARGIN + Gui.SIDE * 2 * row
                x1 = Gui.MARGIN + l * 2 * Gui.SIDE + Gui.SIDE
                y1 = Gui.MARGIN + Gui.SIDE * 2 * row
                self.__canvas.create_line(x0, y0, x1, y1)
                self.__canvas.create_line(x0, y0 + Gui.SIDE, x1, y1 + Gui.SIDE)

    def __draw_puzzle(self):
        self.__canvas.delete("numbers")
        numbers = self.__game.get_board
        
        # loop through every cell of the puzzle
        for row in range(len(numbers)):
            for col in range(len(numbers[row])):
                if len(numbers[row][col]) == 1:

                    # if there is only once number in a cell, write that number on the canvas
                    self.__canvas.create_text(
                        Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 2,
                        Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                        text=numbers[row][col],
                        tags="numbers",
                        font=("Arial", 15),
                    )
                else:
                    # calculations for pencil markings, splits one cell into 9 grids
                    for i in numbers[row][col]:
                        # place 1 as a pencil marking in the top left corner of the cell
                        if i == "1":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        
                        # place 2 as a pencil marking in the top middle of the cell
                        elif i == "2":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 2,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        
                        # place 3 as pencil marking in the top right of the cell
                        elif i == "3":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + 5 * Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        
                        # place 4 as a pencil marking in the left middle of the cell
                        elif i == "4":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        
                        # place 5 as a pencil marking in the middle of the cell
                        elif i == "5":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 2,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        
                        # place 6 as a pencil marking in the middle right of the cell
                        elif i == "6":
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + 5 * Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + Gui.SIDE / 2,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )
                        
                        # place 7 as a pencil marking in the bottom left of the cell
                        else:
                            self.__canvas.create_text(
                                Gui.MARGIN + col * Gui.SIDE + Gui.SIDE / 6,
                                Gui.MARGIN + row * Gui.SIDE + 5 * Gui.SIDE / 6,
                                text=i,
                                tags="numbers",
                                font=("Arial", 10),
                            )

    # method which calculates which cell has been clicked on the canvas
    def __cell_clicked(self, event):

        # if the game is already complete, the player cannot make changes to the grid anymore
        if self.__game.check():
            return

        # takes x and y coordinates of a mouse click
        x, y = event.x, event.y
        if (
            Gui.MARGIN < x < self.__width - Gui.MARGIN
            and Gui.MARGIN < y < self.__height - Gui.MARGIN
        ):
            self.__canvas.focus_set()

        # determines which row and column of cell has been clicked
        self.__row, self.__col = (
            (y - Gui.MARGIN) // Gui.SIDE,
            (x - Gui.MARGIN) // Gui.SIDE,
        )
        self.__draw_cursor()

    # method to draw box around a selected cell
    def __draw_cursor(self):
        # deletes any previous existing cursors
        self.__canvas.delete("cursor")
        # checks row and col in canvas and is a grid rather than in between grid, and if it is empty
        if (
            self.__row >= 0
            and self.__col >= 0
            and self.__row % 2 == 0
            and self.__col % 2 == 0
            and self.__game.file[self.__row][self.__col] == self.__game.EMPTY
        ):
            # draws box around appropriate cell
            x0 = Gui.MARGIN + self.__col * Gui.SIDE + 1
            y0 = Gui.MARGIN + self.__row * Gui.SIDE + 1
            x1 = Gui.MARGIN + (self.__col + 1) * Gui.SIDE - 1
            y1 = Gui.MARGIN + (self.__row + 1) * Gui.SIDE - 1
            
            # draws a red box around the selected cell
            self.__canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    # method which detects if key is pressed
    def __key_pressed(self, event):

        # if the game is already complete, player cannot make changes to the grid
        if self.__game.check():
            return

        # checks if key pressed is in a non fixed cell
        # checks if the key pressed is either a digit from 1-7 or a backspace
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
                # if a backspace is pressed, clear the cell
                self.__game.set_board(self.__row, self.__col, self.__game.EMPTY)

            if self.__game.check():
                self.__complete()
            
            # redraws puzzle and cell with updates values
            self.__draw_puzzle()
            self.__draw_cursor()

    def __login(self):

        # don't open if game, option of login window is already open
        if self.__login_win or self.__game_win or self.__opt_win:
            return

        # if the user is already logged in, a message is displayed to say that
        if self.__logged_in:
            self.__menu_console.configure(state="normal")
            self.__menu_console.delete("1.0", END)
            self.__menu_console.insert(END, "already logged in")
            self.__menu_console.tag_add("center", "1.0", "end")
            self.__menu_console.configure(state="disabled")
            return

        # otherwise, open the login window
        login_win = Toplevel(self.__root)
        login_win.title("Login")
        login_win.geometry("400x400")
        self.__login_win = login_win

        console = Text(login_win, height=1, width=50)
        console.tag_configure("center", justify="center")
        console.pack(side=TOP)
        console.configure(state="disabled")
        self.__login_console = console

        # allows user to enter username and password in text boxes
        Label(login_win, text="Username:").pack(side=TOP, pady=(50, 0))
        self.__username = StringVar()
        Entry(login_win, textvariable=self.__username).pack(side=TOP)
        Label(login_win, text="Password:").pack(side=TOP)
        self.__password = StringVar()
        Entry(login_win, textvariable=self.__password).pack(side=TOP)

        # displays the Dismiss button at the bottom of the window
        dismiss_button = Button(
            login_win,
            text="Dismiss",
            command=self.__dismiss_login_win,
            width=20,
            height=2,
        )
        dismiss_button.pack(side=BOTTOM)

        # a New Account button is also displayed at the bottom of the window
        newacc_button = Button(
            login_win,
            text="Create New Account",
            command=self.__register,
            width=20,
            height=2,
        )
        newacc_button.pack(side=BOTTOM)

        # enter button
        enter_button = Button(
            login_win, text="Enter", command=self.__get_logins, width=20, height=2
        )
        enter_button.pack(side=BOTTOM)

    # method that gets login details from the user
    def __get_logins(self):
        
        # retrieves the username and password that was entered in the text boxes
        self.__user = self.__username.get()
        self.__pswd = self.__password.get()

        # hashes password for searching in database
        self.__pswd = hash_password(self.__pswd)

        # queries a user with the same username and password in database
        stmt = cursor.execute(
            """SELECT * FROM users WHERE username=? AND password=?""",
            (self.__user, self.__pswd,),
        )
        
        # if there is no matching user, a message is displayed stating an incorrect username of password
        if len(stmt.fetchall()) == 0:
            self.__login_console.configure(state="normal")
            self.__login_console.delete("1.0", END)
            self.__login_console.insert(END, "incorrect username or password")
            self.__login_console.tag_add("center", "1.0", "end")
            self.__login_console.configure(state="disabled")
        else:
            # otherwise, the user has successfully logged in
            self.__logged_in = True
            self.__current_username = self.__user
            self.__menu_console.configure(state="normal")
            self.__menu_console.delete("1.0", END)
            self.__menu_console.insert(END, "successfully logged in")
            self.__menu_console.tag_add("center", "1.0", "end")
            self.__menu_console.configure(state="disabled")

            # the login window is dismissed
            self.__dismiss_login_win()

    # method which allows the user to register a new account
    def __register(self):
        
        # if the game or option window is already opened, this window cannot be opened
        if self.__game_win or self.__opt_win:
            return

        # otherwise, a new window is displayed, and the login window is dismissed
        register_win = Toplevel(self.__root)
        register_win.title("Create New Account")
        register_win.geometry("400x400")
        self.__register_win = register_win
        self.__dismiss_login_win()

        console = Text(register_win, height=1, width=50)
        console.tag_configure("center", justify="center")
        console.pack(side=TOP)
        console.configure(state="disabled")
        self.__register_console = console

        # user can enter new username and password
        Label(register_win, text="Enter a new username and password").pack(
            side=TOP, pady=(50, 0)
        )
        Label(register_win, text="Username:").pack(side=TOP, pady=(50, 0))
        self.__newusername = StringVar()
        Entry(register_win, textvariable=self.__newusername).pack(side=TOP)
        Label(register_win, text="Password:").pack(side=TOP)
        self.__newpassword = StringVar()
        Entry(register_win, textvariable=self.__newpassword).pack(side=TOP)

        # dismiss button packed at the bottom of window
        dismiss_button = Button(
            register_win,
            text="Dismiss",
            command=self.__dismiss_register_win,
            width=20,
            height=2,
        )
        dismiss_button.pack(side=BOTTOM)

        # create account button packed at the bottom of window
        create_button = Button(
            register_win,
            text="Create Account",
            command=self.__register_login,
            width=20,
            height=2,
        )
        create_button.pack(side=BOTTOM)

    # method adds login details to database if username doesn't already exist
    def __register_login(self):

        # retrieves the username and password entered in the text boxes
        self.__new_user = self.__newusername.get()
        self.__new_pswd = self.__newpassword.get()

        # hashes password to store in database
        self.__new_pswd = hash_password(self.__new_pswd)

        self.__register_console.configure(state="normal")
        self.__register_console.delete("1.0", END)

        # retrieves all existing users with the same username
        currentuser = cursor.execute(
            """SELECT * FROM users WHERE username=?""", (self.__new_user,),
        )

        ###########
        # Group B #
        # Records #
        ###########

        if len(currentuser.fetchall()) == 0:
            # if there is no existing user with the same username
            # a new user record is inserted into the database
            cursor.execute(
                """INSERT INTO users (username,password,games,completed,timer)
        VALUES (?, ?, ?, ?, ?)""",
                (self.__new_user, self.__new_pswd, 0, 0, 0),
            )
            conn.commit()
            self.__register_console.insert(END, "created new account")
        else:
            # otherwise a message is displayed to ask the user to enter a unique username
            self.__register_console.insert(END, "please enter a unique username.")

        self.__register_console.tag_add("center", "1.0", "end")
        self.__register_console.configure(state="disabled")

    # method that lets the user log out
    def __logout(self):
        self.__menu_console.configure(state="normal")
        self.__menu_console.delete("1.0", END)
        
        # if the user is logged in, log out
        if self.__logged_in:
            self.__logged_in = False
            self.__menu_console.insert(END, "successfully logged out")
        else:
            # if the user isn't logged in, they naturally cannot log out
            self.__menu_console.insert(END, "you are not logged in")

        self.__menu_console.tag_add("center", "1.0", "end")
        self.__menu_console.configure(state="disabled")

    # method that opens help window
    def __help(self):
        
        # the window will not open if it is already opened
        if self.__help_win:
            return

        # creates new help window
        help_win = Toplevel(self.__root)
        help_win.title("Help")
        help_win.geometry("400x400")
        self.__help_win = help_win

        ##############
        # Group B    #
        # Text Files #
        ##############

        # opens a text file containing the game rules and displays this to the window
        with open("rules.txt") as f:
            rules = f.read()

        text = Text(help_win)
        text.pack(expand=True, fill="both")
        text.insert(END, rules)
        text.configure(state="disabled")

        # dismiss button is packed at the bottom of the window
        dismiss_button = Button(
            help_win,
            text="Dismiss",
            command=self.__dismiss_help_win,
            width=10,
            height=2,
        )
        dismiss_button.pack(side=BOTTOM)

    # method that allows the user to configure their puzzle settings
    def __select_options(self):

        # doesn't open if an option, game or login window already open
        if self.__opt_win or self.__game_win or self.__login_win:
            return

        # new window is created
        opt_win = Tk()
        opt_win.title("Configure Grid Settings")
        opt_win.geometry("400x400")
        self.__opt_win = opt_win

        # drop down menus for grid size and difficulty
        # the user has 4 different options to choose for grid sizes
        Label(opt_win, text="Please select grid size:").pack(side=TOP, pady=(50, 0))
        self.__size = StringVar(opt_win)
        self.__size.set("4x4")
        OptionMenu(opt_win, self.__size, "4x4", "5x5", "6x6", "7x7").pack(side=TOP)

        # the user has 3 difficulty levels to choose from
        Label(opt_win, text="Please select difficulty:").pack(side=TOP)
        self.__difficulty = StringVar(opt_win)
        self.__difficulty.set("1. easy")
        OptionMenu(opt_win, self.__difficulty, "1. easy", "2. medium", "3. hard").pack(
            side=TOP
        )

        # dismiss button is packed at the bottom of the window
        dismiss_button = Button(
            opt_win, text="Dismiss", command=self.__dismiss_opt_win, width=10, height=2,
        )
        dismiss_button.pack(side=BOTTOM)

        # 'done' button is packed at the bottom of the window
        done_button = Button(
            opt_win, text="Done", command=self.__configured, width=10, height=2,
        )
        done_button.pack(side=BOTTOM)

    def __configured(self):
        # retrieves the size and difficuly level that the user has selected
        self.__size = int(self.__size.get()[0])
        self.__difficulty = int(self.__difficulty.get()[0])

        # destroys the configuration window
        self.__opt_win.destroy()
        self.__opt_win = None

        # calls the play game method
        self.__play_game()

    # method that displayes the statistics window
    def __stats(self):
        
        # the window will not open if it is already opened
        if self.__stats_win:
            return

        # user can view their stats if they are logged, as well as a leaderboard of all users sorted by completed games
        if self.__logged_in:
            stats_win = Toplevel(self.__root)
            stats_win.title("Statistics")
            stats_win.geometry("400x400")
            self.__stats_win = stats_win

            # the number of completed games is displayed
            Label(stats_win, text="number of completed games: ", font=('Courier', 12, 'bold')).pack(
                side=TOP, pady=(30, 0)
            )
            # the number of completed games is queried from the database
            result = conn.execute(
                """SELECT completed FROM users WHERE username=?""", (self.__user,)
            )
            Label(stats_win, text=result.fetchone()).pack(side=TOP)

            # the number of total games is displayed
            Label(stats_win, text="number of total games:", font=('Courier', 12, 'bold')).pack(side=TOP, pady=(20, 0))
            result = conn.execute(
                """SELECT games FROM users WHERE username=?""", (self.__user,)
            )
            Label(stats_win, text=result.fetchone()).pack(side=TOP)

            # the average time for a player to complete a certain puzzle is displayed
            Label(stats_win, text="average time taken to complete puzzle:", font=('Courier', 12, 'bold')).pack(
                side=TOP, pady=(20, 0)
            )
            result = conn.execute(
                """SELECT timer FROM users WHERE username=?""", (self.__user,)
            )
            Label(stats_win, text=result.fetchone()).pack(side=TOP)

            # a leaderboard containing all users sorted by number of completed puzzles is displayed
            Label(stats_win, text="Leaderboard (sorted by completed)", font=('Courier', 12, 'bold')).pack(
                side=TOP, pady=(20, 0)
            )
            result = conn.execute(
                """SELECT username, completed FROM users ORDER BY completed DESC"""
            ).fetchall()

            for row in result:
                Label(stats_win, text=row).pack(side=TOP, pady=0)


            # the games that a user has saved is displayed
            Label(stats_win, text="Saved Games (GameID, Time, Grid Size, Difficulty):", font=('Courier', 12, 'bold')).pack(
                side=TOP, pady=(20, 0)
            )

            ##########################
            # Group A                #
            # Complex Database Model #
            ##########################

            # queries all saved games by joining the users, puzzles and savedgames tables
            result = conn.execute(
                """SELECT puzzles.gameid, time, grid_size, difficulty FROM puzzles
                    INNER JOIN savedgames ON puzzles.gameid = savedgames.gameid
                    INNER JOIN users ON savedgames.username = users.username
                    WHERE users.username=?""", (self.__current_username,)
            ).fetchall()

            for row in result:
                Label(stats_win, text=row).pack(side=TOP, pady=0)

            # dismiss button is packed at the bottom of the window
            dismiss_button = Button(
                stats_win,
                text="Dismiss",
                command=self.__dismiss_stats_win,
                width=10,
                height=2,
            )
            dismiss_button.pack(side=BOTTOM)

        else:
            # if the user is not logged in, a message is displayed to prompt the user to login
            self.__menu_console.configure(state="normal")
            self.__menu_console.delete("1.0", END)
            self.__menu_console.insert(END, "need to login first")
            self.__menu_console.tag_add("center", "1.0", "end")
            self.__menu_console.configure(state="disabled")

    # method which displays the settings window
    def __settings(self):
        # if the game, option, login or stats window is already open, this page will not open
        if self.__game_win or self.__opt_win or self.__login_win or self.__stats_win:
            return

        set_win = Toplevel(self.__root)
        set_win.title("Settings")
        set_win.geometry("400x400")
        self.__set_win = set_win

        # a toggle is displayed allowing the user to allow timings for puzzles
        self.__toggle = IntVar()
        Checkbutton(
            set_win,
            text="timings for games",
            var=self.__toggle,
            onvalue=1,
            offvalue=0,
            command=self.__toggle_timer,
        ).pack(side=TOP, pady=(50, 0))

        # the option to change the colour background is given to the user
        Label(set_win, text="colour background: ").pack(side=TOP, pady=(50, 0))
        self.__backgroundcol = StringVar(set_win)
        self.__backgroundcol.set("white")
        
        # 6 different colours are given as a background colour option
        OptionMenu(
            set_win,
            self.__backgroundcol,
            "white",
            "black",
            "red",
            "blue",
            "green",
            "yellow",
        ).pack(side=TOP)

        # dismiss button is packed at the bottom of the window
        dismiss_button = Button(
            set_win, text="Dismiss", command=self.__dismiss_set_win, width=10, height=2,
        )
        dismiss_button.pack(side=BOTTOM)

    # method that checks whether timing checkbox is ticked or not
    def __toggle_timer(self):
        if self.__toggle.get() == 1:
            self.__timer = True
        else:
            self.__timer = False

    # method that quits the root window and thus the game
    def __quit(self):
        self.__root.quit()

    # method that dismisses the settings window
    def __dismiss_set_win(self):
        # retreives the background colour that the user has selected
        self.__backgroundcol = self.__backgroundcol.get()
        self.__set_win.destroy()
        self.__set_win = None

    # method that dismisses the statistics window
    def __dismiss_stats_win(self):
        self.__stats_win.destroy()
        self.__stats_win = None

    # method that dismisses the game window
    def __dismiss_game_win(self):
        self.__game_win.destroy()
        self.__game_win = None

    # method that dismisses the help window
    def __dismiss_help_win(self):
        self.__help_win.destroy()
        self.__help_win = None

    # method that dismisses the login window
    def __dismiss_login_win(self):
        self.__login_win.destroy()
        self.__login_win = None

    # method that dismisses the option window
    def __dismiss_opt_win(self):
        self.__opt_win.destroy()
        self.__opt_win = None

    # method that dismisses the register window
    def __dismiss_register_win(self):
        self.__register_win.destroy()
        self.__register_win = None

    # method to call if the came is complete
    def __complete(self):
        # displays message in console to user if puzzle correct
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.insert(END, "puzzle correct!")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

        if self.__logged_in:
            # if the user is logged in, incremented the number of completed games for the current user
            conn.execute(
                """UPDATE users SET completed = completed+1 WHERE username=?""",
                (self.__user,),
            )
            conn.commit()

            if self.__timer:
                # if the timings are enabled, calculate the time taken to complete the puzzle
                self.__time = time.time() - self.__start

                ####################################
                # Group C                          #
                # Simple Mathematical Calculations #
                ####################################

                # calculates and stores the new timed average for a completed game in the user's record
                conn.execute(
                    """UPDATE users SET timer = (timer*(completed-1)+?)/completed WHERE username=?""",
                    (self.__time, self.__user,),
                )
                conn.commit()

    # method to check if there are any mistakes in the users answer
    def __check(self):
        if self.__game.check():
            return

        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)

        mistake = self.__game.mistakefound()
        
        # if a mistake if found, a message is displayed on the screen
        if mistake:
            self.__console.insert(END, "mistakes found")
        else:
            self.__console.insert(END, "no mistakes found")

        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

    # method which restarts the puzzle
    def __restart(self):
        self.__game.restart()
        self.__draw_puzzle()
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.configure(state="disabled")

    # method which undos the users last move
    def __undo(self):
        # if the game is already completed, then nothing occurs
        if self.__game.check():
            return

        if self.__game.undo() > 0:
            # puzzle is redrawn after a move is undone
            self.__draw_puzzle()
        else:
            # if the moves stack is empty, there are no moves left for the user to undo
            self.__console.configure(state="normal")
            self.__console.delete("1.0", END)
            self.__console.insert(END, "no moves to undo")
            self.__console.tag_add("center", "1.0", "end")
            self.__console.configure(state="disabled")

    # method which displays the answer
    def __answer(self):
        # return if the game is already completed
        if self.__game.check():
            return

        # shows the answer and redraws puzzle
        self.__game.show_answer()
        self.__draw_puzzle()
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.insert(END, "solution to puzzle:")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

    # method which displays a hint to the user
    def __hint(self):
        # return if the puzzle is already completed
        if self.__game.check():
            return

        # a random non-filled cell will be filled in for the user when pressed
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

    # method for when the user presses save
    def __save(self):

        # saves the solution of a puzzle to a file
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)

        if not self.__game.check():
            # the user can only save a puzzle if it is comleted
            self.__console.insert(END, "can only save is puzzle is completed")
            self.__console.tag_add("center", "1.0", "end")
            self.__console.configure(state="disabled")
            return

        self.__game.save_puzzle()
        self.__console.insert(END, "saved puzzle")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

        # if timings are enabled, add the timings to the record
        # otherwise insert "n/a" to indicate the user did not have timings enabled for that puzzle
        
        if self.__logged_in:
            # if the user is logged in, add the puzzle details to their saved games
            if self.__timer:
                temptime = self.__time
            else:
                temptime = "n/a"
            
            ###########################
            # Group A                 #
            # Aggregate SQL Functions #
            ###########################

            # gets number of rows from puzzle table and assinged to variable gamelength
            gamelength = len(cursor.execute("""SELECT * FROM puzzles""").fetchall()) + 1

            # inserts puzzle details such as difficulty, grid size, time and gameid into the database
            cursor.execute(
                """INSERT INTO puzzles (gameid, time, grid_size, difficulty)
                        VALUES (?, ?, ?, ?)""",
                                (gamelength, temptime, self.__game.get_grid_size, self.__difficulty),
                            )
            cursor.execute(
                """INSERT INTO savedgames (username, gameid)
                        VALUES (?, ?)""",
                                (self.__current_username, gamelength),
                            )
            conn.commit()


    def run(self):
        self.__root.mainloop()


###########
# Group A #
# Hashing #
###########

def hash_password(pswd):
    # uses sha256 to hash password
    pswd = hashlib.sha256(pswd.encode('utf-8')).hexdigest()
    return pswd


class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def __get_grid_settings(self):
        # askes user to enter grid size and difficulty level
        # the user is asked to re-enter if it's not a valid input
        while True:
            try:
                size = int(input("Enter prefered grid size: "))
                if 4 <= size <= 7:
                    break
                else:
                    print("not valid grid size")
            except:
                print("invalid input")

        # the user is asked to enter a difficulty level until it is a valid input
        while True:
            try:
                difficulty = int(input("Enter difficulty; 1 for easy, 2 for hard: "))
                if 1 <= difficulty <= 2:
                    break
                else:
                    print("not valid difficulty input")
            except:
                print("invalid input")

        # returns the users size and difficulty preference
        return size, difficulty

    def __get_input(self):
        # repeaetings geting row and column and number from user until valid input
        while True:
            try:

                #####################
                # Group C           #
                # Simple Data Types #
                #####################

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

        # returns the row number, column number and value that the user wants to play
        return row, column, choice

    def __get_option(self):
        # extra functionality options e.g. restarting game
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
        # creates a puzzle based on user selecting size and difficulty
        size, difficulty = self.__get_grid_settings()
        self.__game.set_grid_size(size)
        self.__game.create_grid(size, difficulty)

        # loop unless answer of the puzzle is correct, or user selects answer
        while not self.__game.check():
            print(self.__game)

            choice = self.__get_option()

            # if r, the game is restarted
            if choice == "r":
                self.__game.restart()
                continue

            # if u, the user's last move is undone, unless the moves stack is empty
            elif choice == "u":
                if self.__game.undo() < 0:
                    print("no moves to undo")
                continue

            # if c, the game checks if there are any mistakes
            elif choice == "c":
                if self.__game.mistakefound():
                    print("mistake is found")
                else:
                    print("no mistakes found")
                continue
            
            # if a, the answer is displayed and the program ends
            elif choice == "a":
                print("solution to puzzle: ")
                self.__game.show_answer()
                print(self.__game)
                quit()

            # otherwise, a user plays a value into a cell if it is valid
            row, col, choice = self.__get_input()
            if self.__game.is_valid(row, col, choice):
                self.__game.play(row, col, choice)

        # if the user's puzzle is the same as the answer, the puzzle is correct!
        print(self.__game)
        print("puzzle correct!")
