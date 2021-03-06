import argparse
from tkinter import BOTH, BOTTOM, TOP, LEFT, RIGHT, Button, Canvas, Frame, Tk
import time

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


def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--board",
                        default='hard',
                        help="Desired board name",
                        type=str)

    args = parser.parse_args()

    # Creates a dictionary of keys = argument flag, and value = argument
    value = (vars(args))
    return (value['board'])


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
        self.board_file = board_file
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


class SudokuGUI(Frame):
    '''
    Tkinter UI, draws the board and accepts user input
    '''

    def __init__(self, parent, game):
        self.game = game  # Class Object Attribute
        self.parent = parent  # Same for any instance of a class
        Frame.__init__(self, parent)
        self.configure(bg='light goldenrod')
        # Current cell selection (-1 means not selected, works with draw_cursor())
        self.row, self.col = 0, 0

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=True)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT,
                             bg='lemonchiffon')  # Canvas size = 490x490
        # Place canvas on frame
        self.canvas.pack(fill=BOTH, side=TOP)

        self.button_frame = Frame(self)
        self.button_frame.pack(side=LEFT, padx=10)

        clear_button = Button(
            self.button_frame, text='Clear Answers', command=self.clear_answers)
        clear_button.pack(fill=BOTH)

        # command = self.game.solve())
        solve_button = Button(
            self.button_frame, text='Solve Puzzle', command=self.solve)
        solve_button.pack(fill=BOTH)

        self.draw_grid()
        self.draw_puzzle()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

    def draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(0, 10):
            color = "blue" if i % 3 == 0 else "gray"

            # Vertical
            x0 = MARGIN + i * SIDE  # (20,20) , (20,530)
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            # Horizontal
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def draw_puzzle(self):
        self.canvas.delete('numbers')
        for row in range(0, 9):
            for column in range(0, 9):
                answer = self.game.game_board[row][column]
                original = self.game.board[row][column]
                if answer != 0:
                    # continue here
                    x = MARGIN + SIDE / 2 + (SIDE * column)
                    y = MARGIN + SIDE / 2 + (SIDE * row)

                    # Differentiate between original board & game board to have different colors
                    if answer == original:
                        color = "black"
                    else:
                        color = "sea green"

                    self.canvas.create_text(
                        x, y, text=answer, tag='numbers', fill=color)

    def clear_answers(self):
        self.game.game_start()
        self.canvas.delete('victory')
        self.draw_puzzle()

    def cell_clicked(self, event):
        if self.game.game_over == True:
            return None

        x, y = event.x, event.y
        print(x, y)
        # Check if click is within board
        if (MARGIN < x < MARGIN + SIDE * 9 and MARGIN < y < MARGIN + SIDE * 9):
            self.canvas.focus_set()
            # get row / column
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE
            print(row, col)

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.game_board[row][col] == 0:
                self.row, self.col = row, col

        self.draw_cursor()

    def draw_cursor(self):
        self.canvas.delete('cursor')  # Delete the tags cursor
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + SIDE * self.col
            y0 = MARGIN + SIDE * self.row
            x1 = MARGIN + SIDE + self.col * SIDE
            y1 = MARGIN + SIDE + self.row * SIDE
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline='red', tag='cursor')

    def key_pressed(self, event):
        if self.game.game_over:
            return
        if event.char in '1234567890' and self.row >= 0 and self.col >= 0:
            self.game.game_board[self.row][self.col] = int(event.char)
            # reset cursor
            self.row, self.col = -1, -1
            self.draw_puzzle()
            self.draw_cursor()
            if self.game.check_win() == True:
                print("VICTORY")
                self.victory()

    def victory(self):
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1, fill='dark orange', outline='orange', tag='victory')
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2, text=' YOU WIN!', tag='victory', fill='white', font=50)

    def solve(self):

        position = self.find_empty()

        if not position:
            return True

        else:
            row, col = position

            for number in range(1, 10):
                if self.valid(self.game.game_board, number, (row, col)):
                    self.game.game_board[row][col] = number

                    if self.solve():
                        self.draw_puzzle()
                        return True

                self.game.game_board[row][col] = 0

        return False

    def find_empty(self):

        for i in range(len(self.game.game_board)):
            for j in range(len(self.game.game_board)):
                if self.game.game_board[i][j] == 0:
                    return (i, j)

    def valid(self, board, num, pos):
        for col in range(0, 9):
            if board[pos[0]][col] == num and pos[1] != col:
                return False

        for row in range(0, 9):
            if board[row][pos[1]] == num and pos[0] != row:
                return False

        grid_x = pos[1] // 3
        grid_y = pos[0] // 3

        for i in range(grid_y * 3, grid_y * 3 + 3):
            for j in range(grid_x*3, grid_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True


if __name__ == '__main__':
    board_name = parse_arguments()

    try:
        with open('%s.sudoku.txt' % board_name, 'r') as board_file:
            game = SudokuGame(board_file)
            game.game_start()
    except:
        raise SudokuError('No such board exists')

    root = Tk()
    SudokuGUI(root, game)
    # 80 is the space below the main board
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 80))
    root.mainloop()
