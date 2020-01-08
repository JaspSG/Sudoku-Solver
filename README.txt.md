# Sudoku-Solver

#Disclaimer The following programme is coded along side the tutorial from : http://newcoder.io/gui/

 A programme to solve any given Sudoku Puzzle.

 run this programme at the command line with:
 python sudoku.py
 
 with choice of board:
 python sudoku.py board (board name)

Objectives of this Project:
1.  Learn about recursion and algorithm application (Backtracking)
2.  Learn pygame to create a Basic GUI
3.  Further solidify knowledge on Basic Python (OOP / Classes)

How it works:
1.  Programme starts off with basic Sudoku Puzzle.
2.  Play the game.
4.  If all cells are filled in, a victory tab will appear, else press clear puzzle to try again.
3.  Press Solve puzzle button to solve the puzzle.



Steps for the game:
1.  Create display window for the game
2.  Draw Sudoku 9x9 Grid
3.  Upon start up show board and puzzle.
4.  User input to solve the board.
5.  Check valid spot (empty spot)
6.  Check if input leads to a correct solution
7.  Check if board is completed (full)
    6.1 yes = win
    6.2 no = continue

-click solve puzzle to generate solution

Python features reflection:
argparse library
inherit exception class to create specific program error and raising them.
    class SudokuError(exception)
    raise SudokuError(tuple argument)
isdigit(): checks if string contains digits only
sets() : a collection which is unordered and unindexed.
List comprehensions (grid extraction)
Tkinter event management focus.set() method & event parameter
Backtracking & Recursion

Class object attributes, same for any instance of a class(before init of a class)

Psudocode for solving:

if:
1. find empty space on board
2. if none, return True, solving is complete.

else:

3. for number in range 1-10, try all numbers to fit a number in the empty spot
4. if number fits, call recursive function to solve board.
5. if number doesnt fit, remove number and try again
