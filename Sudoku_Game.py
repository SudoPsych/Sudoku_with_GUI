"""
12/25/20
This program does many a things. It generates random Sudoku grids from a file. It checks if a particular grid is valid or not.
It displays grids in the terminal all pretty n shit. It lets you play the game and the piece of resistance:
it fucking solves them for you (using recursion :O).
"""

import random
from PuzzleListFile import puzzleList
count = 0


def emptyGridMaker():
    # Creates a 9x9 grid full of 0's
    grid = [[0 for _ in range (9)] for _ in range (9)]
    return grid

def splitGrid(grid):
    # This function reassigns the numbers into row, column, and block groupings
    probRow = grid
    probCol = [[] for _ in range(9)]
    probBlock   = [[] for _ in range(9)]

    # grouping the columns
    for rowPos in range(9):
         for colPos in range(9):
             probCol[rowPos].append(grid[colPos][rowPos])

    # Grouping the blocks
    for rowPos in range(9):
        for colPos in range(9):
            # This is a fancy equation I made to append the position in the grid
            # to the correct list in the block space.
            assignedBlock = ((colPos + 3) // 3) + (3 * (rowPos // 3)) - 1
            probBlock[assignedBlock].append(grid[rowPos][colPos])

    # grouping the spaces into a single function for easy use

    gridSpace = [probRow, probCol, probBlock]
    return gridSpace


def checkIfValid(grid):
    # These algs check for duplicates, if it finds any then its not a proper sudoku grid.
    isValid = bool
    gridSpace = splitGrid(grid)


    # Checks the row, col, and block space to see if any of the inputted nums are duplicates
    for space in gridSpace:
        # Copies the spaces so no shenanigans occur
        copySpace = [x[:] for x in space]
        for row in copySpace:
            # Removes all 0's from the list
            row = [num for num in row if num is not 0]
            # Checks if there are duplicates among the remaining numbers
            if len(set(row)) != len(row):
                isValid = False
                return isValid

    for row in gridSpace[0]:
        # This checks if the grid still has zeroes and return a null bool if it does
        if 0 in row:
            return isValid

    isValid = True
    return isValid


def display(grid):
    # Displays the grid, turns 0's into blank spaces

    # Assigning 'displayGrid' equal to 'grid' will tie the variables together and
    # any changes to one will affect the other. Since we're dealing with a list
    # of lists this definition is necessary.
    displayGrid = [row[:] for row in grid]
    for i in range(9):
        for num in range(9):
            if displayGrid[i][num] == 0:
                displayGrid[i][num] = ' '
        row = " ".join(str(v) + ' |' * (c == 2 or c == 5) for c, v in enumerate(displayGrid[i]))
        print(row)
        if i == 2 or i == 5:
            print("".join(['-'] * 21))
    print("\n")
    return


def printResults(isValid):
    # Checks if the solution is valid, invalid, or incomplete.
    if isValid == True:
        print("This solution is valid :)")
    elif isValid == False:
        print("This solution is not valid :(")
    else:
        print("There are still empty squares :O")

def getRandPuz():
    pass


def getRandomPuzzle():
    # No longer need this function. Since I got lazy with pyinstaller (or maybe what I was trying to do was impossible)
    # I turned the .txt file into a single list stored in a separate .py file and pull from that instead.

    # Read file; get lines
    puzzleFile = open('5000_puzzles.txt')
    puzzleGrids = puzzleFile.readlines()

    # Get random line from file
    randNum = random.randrange(0, len(puzzleGrids))
    randomPuzzle = puzzleGrids[randNum]

    # Convert string into two lists of nums
    problemNum, solutionNum = randomPuzzle.split(',')
    problemNum, solutionNum = list(problemNum.rstrip()), list(solutionNum.rstrip())
    problemNum = [int(num) for num in problemNum]
    solutionNum = [int(num) for num in solutionNum]

    # Convert list of nums into 9x9 grid
    # Takes 9 numbers at a time from the string
    problemGrid = [problemNum[(9*i):(9*i)+9] for i in range(9)]
    solutionGrid = [solutionNum[(9*i):(9*i)+9] for i in range(9)]

    puzzleFile.close()

    return problemGrid, solutionGrid

def playGame(prob):

    # This function allows the user to play a game of sudouku

    alteredProb = [row[:] for row in prob]
    display(prob)
    print("Type 'end' at anytime to stop editing.")
    rowPos, colPos, posValue = str, str, str

    while True:
        try:
            print("Enter position of number you want to change.")

            # These must be separate lines so the variables will save the 'end' value
            # if it is input.
            rowPos = input("Row: ")
            rowPos = int(rowPos) - 1
            colPos = input("Col: ")
            colPos = int(colPos) - 1
            posValue = input("New value: ")
            posValue = int(posValue)

            if posValue < 0 or posValue > 9:
                # This triggers an error to send the code to the exception.
                int('lol')

            # Check if the value desired to alter was given by the original problem grid.
            if prob[rowPos][colPos] != 0:
                print("\nCannot change that number.\n")
            else:
                alteredProb[rowPos][colPos] = int(posValue)

            display(alteredProb)

        except:
            if 'end' in (rowPos, colPos, posValue):
                display(alteredProb)
                return alteredProb
            else:
                print("Invalid entry, try again.")


def possible(x, y, n, probGrid):
    # Determines if a number can legally go into a given space using only
    # exclusion information from that spaces row, column, block
    probRow, probCol, probBlock = splitGrid(probGrid)
    b = (y // 3) + (3 * (x // 3))
    if n in probRow[x] or n in probCol[y] or n in probBlock[b]:
        return False
    return True

def solve(probGrid):
    # This code is explained in the GUI version
    global count
    for x in range(9):
        for y in range(9):
            if probGrid[x][y] == 0:
                for i in range(1, 10):
                    if possible(x, y, i, probGrid):
                        probGrid[x][y] = i
                        solve(probGrid)
                        if 0 not in [num for row in probGrid for num in row]:
                            return probGrid
                        probGrid[x][y] = 0
                return
    display(probGrid)
    count += 1
    print(count)
    return probGrid

def main():
    # This file only exists to supply the GUI file with some functions
    pass
