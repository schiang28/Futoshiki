from copy import deepcopy
from random import choice, shuffle
import numpy as np


class Game:

    # EMPTY represent an empty cell
    EMPTY = " "

    # defining attributes of the Game class
    def __init__(self):
        self._board = None
        self._grid_size = None
        self.__answer = None
        self.__fixed = None
        self.__moves = []

    # displays board to terminal
    def __repr__(self):
        display = "   ".join(str(i + 1) for i in range(self._grid_size)) + "\n"
        display += "----" * (self._grid_size - 1) + "--" + "\n"
        for row in range(len(self._board)):
            if row % 2 == 0:
                display += " ".join(self._board[row]) + " | " + str(row // 2 + 1) + "\n"
            else:
                display += " ".join(self._board[row]) + " | " + "\n"
        return display

    # getter to return the board
    @property
    def get_board(self):
        return self._board


    ############################
    # Group B                  #
    # Multi-dimensional Arrays #
    ############################

    # the board is represented using a two-dimensional array therefore
    # a value in a cell is represented by its row and column number
    def get_board_num(self, row, col):
        return self._board[row][col]

    # setter which takes in a row and column number, and plays the value to the board at the specified row and column
    # entering a value into the board counts as a move, therefore this is also pushed onto the moves stack
    def set_board(self, row, col, value):
        self.__moves.append((row, col, self._board[row][col]))
        self._board[row][col] = value

    # getter which returns the grid size of the board
    # this should be an integer, e.g. 4 for a 4 by 4 grid
    @property
    def get_grid_size(self):
        return self._grid_size

    # setter which takes in an integer value and sets the grid size
    def set_grid_size(self, value):
        self._grid_size = value

    # each cell in the current board state is assigned the value it should be in the answer grid
    # this method is called when the user wants to see the answer if they have given up the puzzle
    def show_answer(self):
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                self._board[row][col] = self.__answer[row][col]

    # method for creating the grid (takes in size and difficulty)
    def create_grid(self, size, difficulty):
        self.__difficulty = difficulty
        
        # the board is initialised using a 2D numpy array, which is filled with 'empty' cells
        # a row or column of the board is (size * 2 - 1) as inequalities and spaces between cells are also stores in the board
        self.__board_empty = np.full((size * 2 - 1, size * 2 - 1), Game.EMPTY)
        
        # a list of cell numbers are also initialised, so that random cells can be chosen and removed later on during generation
        self.__cells = list(range((self._grid_size * 2 - 1) ** 2))

        # the grid is filled to create a latin square and puzzle is generated from that latin square
        self.__fill(self.__board_empty)
        self.__fill_inequalities()
        self.__generate()

        # TODO HUMAN SOLVER
        self.__human_solver(deepcopy(self.file))

        # changing of inequalities for displaying to gui
        # a step of 2 is used when looping as the inequalities between cells are stored at every odd index
        for i in range(1, len(self.file), 2):
            for j in range(0, len(self.file[i]), 2):
                # for vertical adjacent cells with inequalities between them, ^ and v are used rather than < and >
                if self.file[i][j] == "<":
                    self.file[i][j] = "^"
                if self.file[i][j] == ">":
                    self.file[i][j] = "v"


        ###################
        # GROUP A         #
        # List Operations #
        ###################

        # list of cells that are fixed and cannot be changed by the user
        fixed = []
        for row in range(0, len(self.file), 2):
            for col in range(0, len(self.file[row]), 2):
                # loops through each row and column of the original puzzle (with step of 2 to loop through each value)
                if self.file[row][col] != Game.EMPTY:
                    # if the cell already has a number in it, append it's row and column number
                    # to the list 'fixed'
                    # as the original self.file stores inequalities, the actual row number is row // 2 + 1
                    fixed.append((row // 2 + 1, col // 2 + 1))

        # board has to deepcopy as lists are mutable and board is 2d, have to convert from numpy to list
        self._board = (deepcopy(self.file)).tolist()
        self.__fixed = fixed

    # method to check if there are any mistakes in the user's current answer
    def check(self):
        # return True if the user's answer is the same as the answer of the puzzle
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                if self._board[row][col] != self.__answer[row][col]:
                    # returns false if mismatching values are found in a cell
                    return False
        return True

    # method to check that the user's move entered is a valid move
    def is_valid(self, row, col, choice):
        # notifies the user that there is already the same number in the same row or colum
        # notifies the user if there is an inequality that isn't satisfied

        if (row, col) not in self.__fixed:
            # only checks numbers that are entered by the user, i.e. not a fixed cell
            if choice not in self._board[row * 2 - 2] and choice not in [
                i[col * 2 - 2] for i in self._board
            ]:
                # checks that there are no duplicate numbers in the same row and column
                return True
            print("same number in row or column, so invalid move")
            return False
        
        # if the row and column number happens to be a fixed cell, an appropriate message is displayed to the user
        print("tile is fixed, so invalid move")
        return False

    # method that plays the user entered value into their row and column choice
    def play(self, row, col, choice):
        # the original value in that cell is assigned to a variable
        original = self._board[(row - 1) * 2][(col - 1) * 2]

        # for terminal mode, the the user enters 'x', this clears the cell that they chose
        if choice != "x":
            self._board[(row - 1) * 2][(col - 1) * 2] = choice
        else:
            self._board[(row - 1) * 2][(col - 1) * 2] = Game.EMPTY

        # a message with the value and cell is displayed to the terminal
        print(f"played {choice} at {row},{col}")
        
        # the row and column number, as well as the original number in that cell is pushed onto the moves stack
        self.__moves.append(((row - 1) * 2, (col - 1) * 2, original))

    # method to restart the puzzle if the user wishes to
    def restart(self):
        # restarts puzzle by recopying original file and assigns it to the current board state
        # the moves stack is re-initalised to an empty stack
        self._board = (deepcopy(self.file)).tolist()
        self.__moves = []


    ####################
    # GROUP A          #
    # Stack Operations #
    ####################

    # method to undo the user's most recent move
    def undo(self):
        # undo move by popping from moves stack, if stack empty returns -1
        if len(self.__moves) > 0:
            # if the stack isn't empty, undo the move at the top of the stack, pop the move from the stack, and returns 1
            undomove = self.__moves[-1]
            self._board[undomove[0]][undomove[1]] = undomove[2]
            self.__moves.pop()
            return 1
        else:
            # if the stack is empty, return -1
            return -1

    # method to check if there are any mistakes in the user's answer
    def mistakefound(self):
        # returns true if a mistake is found in player's entered answers. Ignores pencil markings and empty cells
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                # checks that the cell is the wrong value, if it isn't empty and if there are any pencil markings in that cell
                if (
                    self._board[row][col] != self.__answer[row][col]
                    and self._board[row][col] != Game.EMPTY
                    and len(self._board[row][col]) == 1
                ):
                    return True
        return False

    def get_hint(self):
        # fills in a random non-filled in cell and adds it to moves stack, returns -1 if all cells filled in
        empty_cells = []
        for row in range(0, len(self._board), 2):
            for col in range(0, len(self._board[row]), 2):
                if self._board[row][col] == Game.EMPTY:
                    empty_cells.append((row, col))

        try:
            rand_cell = choice(empty_cells)
            rand_ans = self.__answer[rand_cell[0]][rand_cell[1]]
            self._board[rand_cell[0]][rand_cell[1]] = rand_ans
            self.__moves.append((rand_cell[0], rand_cell[1], Game.EMPTY))
            return 1
        except:
            return -1

    
    #############################
    # Group A                   #
    # Reading and Writing Files #
    #############################

    def save_puzzle(self):
        # saves completed puzzle to file
        file = open("puzzle.txt", "w")
        file.write("\n".join([",".join(i) for i in self.__answer]))
        file.close()

    def __possible(self, board, row, col, val):
        # checks if a value can be played at row and column of board by checking for duplicates and whether it satisfies inequality constraints
        for i in range(self._grid_size):
            if board[row][i * 2] == str(val) or board[i * 2][col] == str(val):
                return False

        # checking for inequalities
        if row > 0 and board[row - 2][col] != Game.EMPTY:
            if board[row - 1][col] == "<" and val < int(board[row - 2][col]):
                return False
            if board[row - 1][col] == ">" and val > int(board[row - 2][col]):
                return False
        if row < self._grid_size * 2 - 2 and board[row + 2][col] != Game.EMPTY:
            if board[row + 1][col] == "<" and val > int(board[row + 2][col]):
                return False
            if board[row + 1][col] == ">" and val < int(board[row + 2][col]):
                return False
        if col > 0 and board[row][col - 2] != Game.EMPTY:
            if board[row][col - 1] == "<" and val < int(board[row][col - 2]):
                return False
            if board[row][col - 1] == ">" and val > int(board[row][col - 2]):
                return False
        if col < self._grid_size * 2 - 2 and board[row][col + 2] != Game.EMPTY:
            if board[row][col + 1] == "<" and val > int(board[row][col + 2]):
                return False
            if board[row][col + 1] == ">" and val < int(board[row][col + 2]):
                return False

        return True

    def __fill(self, board):
        # fills in an initial empty board, to satisfy conditions of latin square
        numbers = list(range(1, self._grid_size + 1))
        for row in range(0, self._grid_size * 2, 2):
            for col in range(0, self._grid_size * 2, 2):
                if board[row][col] == Game.EMPTY:
                    shuffle(numbers)
                    for n in numbers:
                        if self.__possible(board, row, col, n):
                            board[row][col] = n
                            if Game.EMPTY in board[::2, ::2]:
                                self.__fill(board)
                                board[row][col] = Game.EMPTY
                            else:
                                self.__answer = np.copy(board)
                    # if none of the numbers are possible return nothing
                    return

    def __fill_inequalities(self):
        # fills in all inequality spaces of a full grid
        for row in range(0, len(self.__answer), 2):
            for col in range(0, len(self.__answer[row]), 2):
                if col + 3 <= len(self.__answer):
                    self.__answer[col + 1, row] = (
                        "<"
                        if self.__answer[col, row] < self.__answer[col + 2, row]
                        else ">"
                    )
                if row + 3 <= len(self.__answer):
                    self.__answer[col, row + 1] = (
                        "<"
                        if self.__answer[col, row] < self.__answer[col, row + 2]
                        else ">"
                    )


    ########################
    # Group A              #
    # Recursive Algorithms #
    ########################

    def __solve(self, temp):
        # checks whether temporary grid is solvable, uses recursive backtracking
        for row in range(0, len(self.__answer), 2):
            for col in range(0, len(self.__answer[row]), 2):
                # loops through each cell of the puzzle
                if temp[row][col] == Game.EMPTY:
                    # if the cell is empty, try possible numbers in that cell
                    for n in range(1, self._grid_size + 1):
                        if self.__possible(temp, row, col, n):
                            # if a certain number can be played, play it and temporarily store the grid state
                            temp[row][col] = n
                            self.__solve(temp)
                            if not (self.__end_solver):
                                temp[row][col] = Game.EMPTY
                    # when no values from 1 to n work for a specific cell
                    return
        self.__n_solutions += 1
        
        # if there is more than 1 solution to a puzzle, then this is invalid
        if self.__n_solutions == 2:
            self.__end_solver = True

    def __get_possible_values(self, grid, row, col, current_values):
        # checks for duplicate numbers in any row or column
        for i in current_values.copy():
            # print(i, row, col)
            if str(i) in [r for r in grid[row]] and i in current_values:
                current_values.remove(i)
            if str(i) in [r[col] for r in grid] and i in current_values:
                current_values.remove(i)

        return current_values
        # now need to take into account inequalities

    def __human_solver(self, grid):
        # returns True or False
        possible_values = {}
        contn = False

        for row in range(0, len(self.__answer), 2):
            for col in range(0, len(self.__answer[row]), 2):
                if grid[row][col] == Game.EMPTY:
                    contn = True
                    possible_values[(row, col)] = self.__get_possible_values(grid, row, col, list(range(1, self._grid_size + 1)))
        
        if not contn:
            return
                
        to_delete = []
        for (row, col), v in possible_values.items():
            if len(v) == 1:
                grid[row][col] = str(v[0])
                to_delete.append((row, col))
        for i in to_delete:
            del possible_values[i]
        
        for i in grid:
            print(i)
        print("")
        
        while True:
            contn = False
            for row in range(0, len(self.__answer), 2):
                for col in range(0, len(self.__answer[row]), 2):
                    if grid[row][col] == Game.EMPTY:
                        possible_values[(row, col)] = self.__get_possible_values(grid, row, col, possible_values[(row, col)])
            
            to_delete = []
            for (row, col), v in possible_values.items():
                if len(v) == 1:
                    contn = True
                    grid[row][col] = str(v[0])
                    to_delete.append((row, col))
            for i in to_delete:
                del possible_values[i]

            if not contn:
                break
        
            for i in grid:
                print(i)
            print("")

        for row in range(0, len(self.__answer), 2):
            for col in range(0, len(self.__answer[row]), 2):
                if grid[row][col] == Game.EMPTY:
                    print("solution is not complete, not human solvable :(")
                    return False
        print("solution is complete! It's human solvable :)")
        return True


    ###################################
    # Group A                         #
    # Complex User-defined Algorithms #
    ###################################

    def __generate(self):
        # generates puzzle by removing random values and inequalities one by one, more values removed the harder the difficulty
        self.file = deepcopy(self.__answer)
        shuffle(self.__cells)
        loop = 1

        #######################################################
        # Group B                                             #
        # User defined algorithms (mathematical calculations) #
        #######################################################

        # difficulty is 1 for easy, 2 for medium and 3 for hard
        if self.__difficulty == 1:
            diff = -((self._grid_size * 2 - 1) ** 2 // 2)
        elif self.__difficulty == 2:
            diff = -(self._grid_size * 4)
        else:
            diff = 0
            loop = 2

        for _ in range(loop):
            i = 0
            while i < (len(self.__cells) + diff):
                row = self.__cells[i] // (self._grid_size * 2 - 1)
                col = self.__cells[i] % (self._grid_size * 2 - 1)
                if self.file[row][col] != Game.EMPTY:
                    backup = self.file[row][col]
                    self.file[row][col] = Game.EMPTY

                    board_copy = np.copy(self.file)
                    self.__n_solutions = 0
                    self.__end_solver = False
                    self.__solve(board_copy)

                    if self.__n_solutions != 1:
                        self.file[row][col] = backup

                i += 1


if __name__ == "__main__":
    pass
