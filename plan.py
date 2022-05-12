class Game:
    def play(self, pos, choice):
        # stores the user's choice in the position of the game grid
        # pos can be a1 or b4 representing the position of the grid
        # choice can be e.g. 1 to 4, and X being to clear the grid
        pass

    def login(self, username, password):
        # queries external database with all users, would return success of fail
        pass

    def get_stats(self, username):
        # return a dictionary or string with information on user outside program
        # also can return a leaderboard
        pass

    def undo(self):
        # returns the game state without the last made move
        pass

    def redo(self):
        # returns the game state redoing the last move
        pass

    def difficulty(self, size, mode):
        # size e.g. 3x3 GAME.SIZE = 3
        # mode easy, medium, hard: 0,1,2 e.g. GAME.MODE = 1
        pass

    def answer(self):
        # returns the answer to the grid
        pass

    def check(self):
        # returns True of False as to whether the answer is correct/incorrect
        # can also return a list of positions where the answer is incorrect, e.g. is list was lenght 0 then answer it right
        pass

    def hint(self):
        # could return a position and number of the game
        pass

    def pencil_markings(self, pos):
        # returns a list of pencil markings for a respective position
        pass

    def create_account(self, username, password):
        # creates a new account in users database
        pass

    def save(self):
        # saves the current state of the grid into a file
        pass

    def load(self, grid):
        # laods a game file grid and stores into game.__board
        pass

    def generation(self):
        # generates a new grd and stores into game.__board
        pass

