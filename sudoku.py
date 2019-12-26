import argparse
from tkinter import BOTH, BOTTOM, TOP, LEFT, RIGHT, Button, Canvas, Frame, Tk

# Globals
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

# Create Own Error specific to application:


class SudokuError(Exception):
    '''
    Application Specific Error
    '''
    pass

#Objects#


class SudokuBoard():
    '''
    Sudoku Board Representation
    '''

    def __init__(self, board_file):
        self.board = self.create_board(board_file)

    def create_board(self, board_file):
        board = []
        # iterate over each line
        for line in board_file:
            line = line.strip()
            # Check each line in file is 9 characters long
            if len(line) != 9:
                board = []
                raise SudokuError(
                    'Each line must be 9 characters long')

            # Create each row
            board.append([])

            for c in line:
                if c.isdigit():
                    board[-1].append(int(c))
                else:
                    raise SudokuError(
                        "Line consists of characters other then integers")

            # Check column length = 9
        if len(board) != 9:
            raise SudokuError(
                'The length of the board must be 9 lines long')

        return board


class SudokuGame():
    '''
    Store game state, logic and checking for puzzle completion
    '''

    def __init__(self, board_file):
        self.board = SudokuBoard(board_file).board

    def game_start(self):
        self.game_over = False
        # Main board to play the game
        self.game_board = []
        for i in range(0, 9):
            self.game_board.append([])
            for j in range(0, 9):
                self.game_board[i].append(self.board[i][j])


#  check_win() checks by by pulling out a row/column/grid of data from the board in the form of : [a,b,c,d,...9]
#  and uses the check_block() to compare with a set of values {1,2,3,4,5,6,7,8,9} to return T/F

    def check_win(self):
        if self.check_row() or self.check_column() or self.check_grid() == False:
            return False
        else:
            self.game_over = True
            return True

    def check_block(self, block):
        return set(block) == set(range(1, 10))

    def check_row(self):
        for row in self.game_board:
            if self.check_block(row) != True:
                return False

    def check_column(self):
        for column in range(len(self.game_board)):
            if self.check_block([row[column] for row in self.game_board]) == False:
                return False

    def check_grid(self):
        '''
        Passes each grid to the check_block function
        '''
        # Iterates through the grid starting from row in range (0,3), column in range (0,3) -> row(0,3),column(3,6)....
        for x in range(3):
            for y in range(3):
                if self.check_block([self.game_board[row][column]
                                     for row in range(3*x, 3*(x+1))
                                     for column in range(3*y, 3*(y+1))]) != True:
                    return False

    def solve():
        # backtracking
        pass


class SudokuGUI(Frame):
    '''
    Tkinter UI, draws the board and accepts user input
    '''

    def __init__(self, parent, game):
        self.game = game  # Class Object Attribute
        self.parent = parent  # Same for any instance of a class
        Frame.__init__(self, parent)
        self.configure(bg='yellow')
        self.row, self.col = 0, 0

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=True)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, #Canvas size = 490x490
                             bg='red')  # Place canvas on frame
        self.canvas.pack(fill=BOTH, side=TOP)

        self.button_frame = Frame(self)
        self.button_frame.pack(side = LEFT, padx = 10)

        clear_button = Button(self.button_frame, text='Clear Answers')
                             #command=self._clear_answers)
        clear_button.pack(fill = BOTH)

        solve_button = Button(self.button_frame, text ="Solve Puzzle")
        solve_button.pack(fill = BOTH)

        self.draw_grid()
        self.draw_puzzle()

        #self.canvas.bind("<Button-1>", self.cell_clicked)
        #self.canvas.bind("<Key>", self.key_pressed)

    def draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(0,10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            # x0 = MARGIN
            # y0 = MARGIN + i * SIDE
            # x1 = WIDTH - MARGIN
            # y1 = MARGIN + i * SIDE
            # self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def draw_puzzle(self):
        pass

    def cell_clicked(self):
        pass

    def key_pressed(self):
        pass


#         Test
with open('board.sudoku.txt', 'r') as board_file:
    game = SudokuGame(board_file)
    game.game_start()

    root = Tk()
    SudokuGUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 80)) #width = 490 , height = 570
    root.mainloop()
