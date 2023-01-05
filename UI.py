from abc import ABC, abstractmethod
from Game import Game
from tkinter import *
import sqlite3
import time as time
import hashlib

try:
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
    cursor.execute(
        """CREATE TABLE users (
                    username text,
                    password text,
                    games integer,
                    completed integer,
                    timer real
                    )"""
    )
    cursor.execute(
        """CREATE TABLE puzzles (
                    gameid integer,
                    time real,
                    grid_size integer,
                    difficulty text
                    )"""
    )

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

        # additional buttons and features when playing
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
        for row in range(len(numbers)):
            for col in range(len(numbers[row])):
                if len(numbers[row][col]) == 1:
                    # pen marking
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
        # calculated where cell is clicked on canvas
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
            # draws box around appropriate cell
            x0 = Gui.MARGIN + self.__col * Gui.SIDE + 1
            y0 = Gui.MARGIN + self.__row * Gui.SIDE + 1
            x1 = Gui.MARGIN + (self.__col + 1) * Gui.SIDE - 1
            y1 = Gui.MARGIN + (self.__row + 1) * Gui.SIDE - 1
            self.__canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    def __key_pressed(self, event):
        if self.__game.check():
            return

        # checks if key pressed is in a non fixed cell
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
        if self.__logged_in:
            self.__menu_console.configure(state="normal")
            self.__menu_console.delete("1.0", END)
            self.__menu_console.insert(END, "already logged in")
            self.__menu_console.tag_add("center", "1.0", "end")
            self.__menu_console.configure(state="disabled")
            return

        login_win = Toplevel(self.__root)
        login_win.title("Login")
        login_win.geometry("400x400")
        self.__login_win = login_win

        console = Text(login_win, height=1, width=50)
        console.tag_configure("center", justify="center")
        console.pack(side=TOP)
        console.configure(state="disabled")
        self.__login_console = console

        # allows user to enter uername and password text boxes
        Label(login_win, text="Username:").pack(side=TOP, pady=(50, 0))
        self.__username = StringVar()
        Entry(login_win, textvariable=self.__username).pack(side=TOP)
        Label(login_win, text="Password:").pack(side=TOP)
        self.__password = StringVar()
        Entry(login_win, textvariable=self.__password).pack(side=TOP)

        dismiss_button = Button(
            login_win,
            text="Dismiss",
            command=self.__dismiss_login_win,
            width=20,
            height=2,
        )
        dismiss_button.pack(side=BOTTOM)

        newacc_button = Button(
            login_win,
            text="Create New Account",
            command=self.__register,
            width=20,
            height=2,
        )
        newacc_button.pack(side=BOTTOM)

        enter_button = Button(
            login_win, text="Enter", command=self.__get_logins, width=20, height=2
        )
        enter_button.pack(side=BOTTOM)

    def __get_logins(self):
        # get login details from user
        self.__user = self.__username.get()
        self.__pswd = self.__password.get()

        # hashes password for searching in database
        self.__pswd = hash_password(self.__pswd)

        stmt = cursor.execute(
            """SELECT * FROM users WHERE username=? AND password=?""",
            (self.__user, self.__pswd,),
        )
        if len(stmt.fetchall()) == 0:
            self.__login_console.configure(state="normal")
            self.__login_console.delete("1.0", END)
            self.__login_console.insert(END, "incorrect username or password")
            self.__login_console.tag_add("center", "1.0", "end")
            self.__login_console.configure(state="disabled")
        else:
            self.__logged_in = True
            self.__current_username = self.__user
            self.__menu_console.configure(state="normal")
            self.__menu_console.delete("1.0", END)
            self.__menu_console.insert(END, "successfully logged in")
            self.__menu_console.tag_add("center", "1.0", "end")
            self.__menu_console.configure(state="disabled")
            self.__dismiss_login_win()

    def __register(self):
        # register a new account window, user enters new useranme and password
        if self.__game_win or self.__opt_win:
            return

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

        Label(register_win, text="Enter a new username and password").pack(
            side=TOP, pady=(50, 0)
        )
        Label(register_win, text="Username:").pack(side=TOP, pady=(50, 0))
        self.__newusername = StringVar()
        Entry(register_win, textvariable=self.__newusername).pack(side=TOP)
        Label(register_win, text="Password:").pack(side=TOP)
        self.__newpassword = StringVar()
        Entry(register_win, textvariable=self.__newpassword).pack(side=TOP)

        dismiss_button = Button(
            register_win,
            text="Dismiss",
            command=self.__dismiss_register_win,
            width=20,
            height=2,
        )
        dismiss_button.pack(side=BOTTOM)

        create_button = Button(
            register_win,
            text="Create Account",
            command=self.__register_login,
            width=20,
            height=2,
        )
        create_button.pack(side=BOTTOM)

    def __register_login(self):
        # adds login details to database if username doesn't already exist
        self.__new_user = self.__newusername.get()
        self.__new_pswd = self.__newpassword.get()

        # hashes password to store in database
        self.__new_pswd = hash_password(self.__new_pswd)

        self.__register_console.configure(state="normal")
        self.__register_console.delete("1.0", END)

        currentuser = cursor.execute(
            """SELECT * FROM users WHERE username=?""", (self.__new_user,),
        )


        ###########
        # Group B #
        # Records #
        ###########

        if len(currentuser.fetchall()) == 0:
            # creates a new user record into the database
            cursor.execute(
                """INSERT INTO users (username,password,games,completed,timer)
        VALUES (?, ?, ?, ?, ?)""",
                (self.__new_user, self.__new_pswd, 0, 0, 0),
            )
            conn.commit()
            self.__register_console.insert(END, "created new account")
        else:
            self.__register_console.insert(END, "please enter a unique username.")
        self.__register_console.tag_add("center", "1.0", "end")
        self.__register_console.configure(state="disabled")

    def __logout(self):
        # user can logout of they are logged in
        self.__menu_console.configure(state="normal")
        self.__menu_console.delete("1.0", END)
        if self.__logged_in:
            self.__logged_in = False
            self.__menu_console.insert(END, "successfully logged out")
        else:
            self.__menu_console.insert(END, "you are not logged in")
        self.__menu_console.tag_add("center", "1.0", "end")
        self.__menu_console.configure(state="disabled")

    def __help(self):
        # opens help window (unless already opened) and displayed information on game
        if self.__help_win:
            return

        help_win = Toplevel(self.__root)
        help_win.title("Help")
        help_win.geometry("400x400")
        self.__help_win = help_win

        ##############
        # Group B    #
        # Text Files #
        ##############

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
        # doesn't open if an option, game or login window already open
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
        OptionMenu(opt_win, self.__difficulty, "1. easy", "2. medium", "3. hard").pack(
            side=TOP
        )

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

    def __stats(self):
        if self.__stats_win:
            return

        # user can view their stats if they are logged, as well as a leaderboard of all users sorted by completed games
        if self.__logged_in:
            stats_win = Toplevel(self.__root)
            stats_win.title("Statistics")
            stats_win.geometry("400x400")
            self.__stats_win = stats_win

            Label(stats_win, text="number of completed games: ").pack(
                side=TOP, pady=(30, 0)
            )
            result = conn.execute(
                """SELECT completed FROM users WHERE username=?""", (self.__user,)
            )
            Label(stats_win, text=result.fetchone()).pack(side=TOP)

            Label(stats_win, text="number of total games:").pack(side=TOP, pady=(20, 0))
            result = conn.execute(
                """SELECT games FROM users WHERE username=?""", (self.__user,)
            )
            Label(stats_win, text=result.fetchone()).pack(side=TOP)

            Label(stats_win, text="average time taken to complete puzzle:").pack(
                side=TOP, pady=(20, 0)
            )
            result = conn.execute(
                """SELECT timer FROM users WHERE username=?""", (self.__user,)
            )
            Label(stats_win, text=result.fetchone()).pack(side=TOP)

            Label(stats_win, text="Leaderboard (sorted by completed)").pack(
                side=TOP, pady=(20, 0)
            )
            result = conn.execute(
                """SELECT username, completed FROM users ORDER BY completed DESC"""
            ).fetchall()

            for row in result:
                Label(stats_win, text=row).pack(side=TOP, pady=0)


            Label(stats_win, text="Saved Games (GameID, Time, Grid Size, Difficulty):").pack(
                side=TOP, pady=(20, 0)
            )

            ##########################
            # Group A                #
            # Complex Database Model #
            ##########################

            result = conn.execute(
                """SELECT puzzles.gameid, time, grid_size, difficulty FROM puzzles
                    INNER JOIN savedgames ON puzzles.gameid = savedgames.gameid
                    INNER JOIN users ON savedgames.username = users.username
                    WHERE users.username=?""", (self.__current_username,)
            ).fetchall()

            for row in result:
                Label(stats_win, text=row).pack(side=TOP, pady=0)

            dismiss_button = Button(
                stats_win,
                text="Dismiss",
                command=self.__dismiss_stats_win,
                width=10,
                height=2,
            )
            dismiss_button.pack(side=BOTTOM)

        else:
            self.__menu_console.configure(state="normal")
            self.__menu_console.delete("1.0", END)
            self.__menu_console.insert(END, "need to login first")
            self.__menu_console.tag_add("center", "1.0", "end")
            self.__menu_console.configure(state="disabled")

    def __settings(self):
        # separte window allows user to toggle timings and choose background colour
        if self.__game_win or self.__opt_win or self.__login_win or self.__stats_win:
            return

        set_win = Toplevel(self.__root)
        set_win.title("Settings")
        set_win.geometry("400x400")
        self.__set_win = set_win

        self.__toggle = IntVar()
        Checkbutton(
            set_win,
            text="timings for games",
            var=self.__toggle,
            onvalue=1,
            offvalue=0,
            command=self.__toggle_timer,
        ).pack(side=TOP, pady=(50, 0))

        Label(set_win, text="colour background: ").pack(side=TOP, pady=(50, 0))
        self.__backgroundcol = StringVar(set_win)
        self.__backgroundcol.set("white")
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

        dismiss_button = Button(
            set_win, text="Dismiss", command=self.__dismiss_set_win, width=10, height=2,
        )
        dismiss_button.pack(side=BOTTOM)

    def __toggle_timer(self):
        # checks whether the timing checkbox is ticked or not
        if self.__toggle.get() == 1:
            self.__timer = True
        else:
            self.__timer = False

    def __quit(self):
        self.__root.quit()

    def __dismiss_set_win(self):
        # gets color option from drop down menu and dismisses
        self.__backgroundcol = self.__backgroundcol.get()
        self.__set_win.destroy()
        self.__set_win = None

    def __dismiss_stats_win(self):
        self.__stats_win.destroy()
        self.__stats_win = None

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

    def __dismiss_register_win(self):
        self.__register_win.destroy()
        self.__register_win = None

    def __complete(self):
        # displays message in console to user if puzzle correct
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.insert(END, "puzzle correct!")
        self.__console.tag_add("center", "1.0", "end")
        self.__console.configure(state="disabled")

        if self.__logged_in:
            conn.execute(
                """UPDATE users SET completed = completed+1 WHERE username=?""",
                (self.__user,),
            )
            conn.commit()

            if self.__timer:
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

    def __check(self):
        # checks for mistakes in user's answer and displays message in gui
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
        # restarts puzzle for user in gui
        self.__game.restart()
        self.__draw_puzzle()
        self.__console.configure(state="normal")
        self.__console.delete("1.0", END)
        self.__console.configure(state="disabled")

    def __undo(self):
        # undos the user's last move
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
        # displays the answer of puzzle to user
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
        # a random non-filled cell will be filled in for the user when pressed
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
        # saves the solution of a puzzle to a file
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

        # if timings are enabled, add the timings to the record
        # otherwise insert "n/a" to indicate the user did not have timings enabled for that puzzle
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
        print(gamelength)

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
    pswd = hashlib.sha256(pswd.encode('utf-8')).hexdigest()
    return pswd


class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def __get_grid_settings(self):
        # askes user to enter grid size, and difficulty level
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
        # gets row and column and number from user
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
                # quits if user want to view answer
                print("solution to puzzle: ")
                self.__game.show_answer()
                print(self.__game)
                quit()

            row, col, choice = self.__get_input()
            if self.__game.is_valid(row, col, choice):
                self.__game.play(row, col, choice)

        print(self.__game)
        print("puzzle correct!")
