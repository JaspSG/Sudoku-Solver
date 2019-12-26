# Sudoku-Solver
 A programme to solve any given Sudoku Puzzle.

Objectives of this Project:
1.  Learn about recursion and algorithm application (Backtracking)
2.  Learn pygame to create a Basic GUI
3.  Further solidify knowledge on Basic Python (OOP / Classes)

How it works:
1.  Programme starts off with basic Sudoku Puzzle.
2.  Play the game.
3.  Press (Spacebar?) to watch algorithm solve the puzzle.

Features to add:
1.  Enter own puzzle.
2.  Generate puzzle.


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

Step 4 considerations:
Backtrack every input or store the first solution?
Test by timeit?s

Python features reflection:
argparse library ?
inherit exception class to create specific program error and raising them.
    class SudokuError(exception)
    raise SudokuError(tuple argument)
isdigit(): checks if string contains digits only
sets() : a collection which is unordered and unindexed.
List comprehensions (grid extraction)

Class object attributes, same for any instance of a class(before init of a class)