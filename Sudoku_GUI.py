"""
1/5/21
Finished on 1/7/21
Really happy with how this program turned out. I wanted to make it user proof so nothing the
user could do would break the program. It came out better than I expected and the different
functions do everything I originally set out to do. (Except display the solving process)
I learned a lot from this whole 2 week project and I hope to do more in the future :)
"""

"""
Things to add:
Save Progress
Different types of Sudoku grids
Different difficulties
Find a way to display the solving process
Confirm entries with the <Enter> key
Make the program a clickable Desktop Icon
"""

from tkinter import *
from Sudoku_Game import *
from PuzzleListFile import puzzleList
import random

root = Tk()

class Sudoku:

    def __init__(self, root_, puzzleList):
        self.root = root_
        self.root.title("Sudoku")
        self.puzzleList = puzzleList
        self.gridEntryList = []
        self.buttonList = []




    def getCurrentGridState(self):
        # Gets current state of the puzzle and returns a 9x9 list of the numbers
        currentNums = [[] for _ in range(9)]

        for x in range(9):
            for y in range(9):
                # Adds the number as int if it exists otherwise it appends a 0
                try:
                    currentNums[x].append(int(self.buttonList[x][y]['text']))
                except:
                    currentNums[x].append(0)
        return currentNums




    def null(self):
        # setting ['command'] equal to None doesn't work so here's a function that does nothing ig :)
        pass




    def nullifyGrid(self):
        # Erases the lingering entry boxes in case the user is dumb/lazy and left them open
        for entry in self.gridEntryList:

            rowPos = entry.grid_info()['row']
            colPos = entry.grid_info()['column']
            x = rowPos - (rowPos // 4)
            y = colPos - (colPos // 4)
            entry.destroy()

            self.buttonList[x][y].grid(row=rowPos, column=colPos)

        self.gridEntryList.clear()
        # Its me, I'm dumb and lazy

    def getRandPuzzle(self):
        # Retrieves a random puzzle from the provided list

        # Gets random number within length of the list
        randNum = random.randrange(0, len(self.puzzleList))
        randomPuzzle = self.puzzleList[randNum]
        # Converts string into list of ints
        randomPuzzle = [int(num) for num in randomPuzzle]
        # Turns list of 81 nums into 9x9 grid
        randPuzzleList = [randomPuzzle[(9*i):(9*i)+9] for i in range(9)]

        return randPuzzleList


    """
    This set of functions serves as commands for the sidebar buttons.
    """
    def confirmButtonFunc(self):

        for entry in self.gridEntryList:

            # Bad redundancy is bad and makes me sad
            rowPos = entry.grid_info()['row']
            colPos = entry.grid_info()['column']
            x = rowPos - (rowPos // 4)
            y = colPos - (colPos // 4)
            num = entry.get()

            # Checks if the user input a valid num and reinstates the button with that num if true else blank
            try:
                if int(num) in range(1,10):
                    self.buttonList[x][y]['text'] = num
                else:
                    self.buttonList[x][y]['text'] = '  '
            except:
                self.buttonList[x][y]['text'] = '  '

        self.nullifyGrid()




    def getNewPuzzle(self):
        self.nullifyGrid()

        # Gets a random puzzle from the provided file
        self.randPuzzle = self.getRandPuzzle()

        for x in range(9):
            for y in range(9):

                if self.randPuzzle[x][y] is 0:
                    # If position on grid is blank (0), the button gets the cool function
                    self.buttonList[x][y]['text'] = '  '
                    self.buttonList[x][y]['command'] = lambda butt=self.buttonList[x][y]: self.gridButtonFunc(butt)
                else:
                    # Otherwise it just displays the given number and does jack shit
                    self.buttonList[x][y]['command'] = self.null
                    self.buttonList[x][y]['text'] = self.randPuzzle[x][y]





    def checkSolutionFunc(self):
        self.nullifyGrid()

        currentNums = self.getCurrentGridState()
        isValid = checkIfValid(currentNums)

        # Create new window that tells the user the result

        resultsRoot = Tk()
        resultsRoot.title("Results")

        resultsLabel = Label(resultsRoot)
        resultsLabel.pack()

        exitResultsButton = Button(resultsRoot, text="OK", command=resultsRoot.destroy)
        exitResultsButton.pack()

        # Checks if the puzzle is solved/not/incomplete and alters the label accordingly
        if isValid == True:
            resultsLabel['text'] = "It is solved :)"
        elif isValid == False:
            resultsLabel['text'] = "Oop, try again :("
        else:
            resultsLabel['text'] = "It's not even done yet :/"




    def solveButtonFunc(self):
        # This function is the command for the button as nullify grid and
        # getting the current grid state should only be called once.

        self.nullifyGrid()
        currentGrid = self.getCurrentGridState()

        # Does a soft check to see if the program is solvable first. There are still edge cases this
        # function does not detect, however, and a runtime error will still occur.
        if checkIfValid(currentGrid):
            self.solvePuzzle(currentGrid)




    def solvePuzzle(self, currentGrid):
        # Loop through all the grid spaces
        for x in range(9):
            for y in range(9):
                # Stop when first empty space is found
                if currentGrid[x][y] == 0:
                    # Look for first number that is a valid entry in that square
                    for i in range(1, 10):

                        if possible(x, y, i, currentGrid):

                            # Put that number there and recur
                            self.buttonList[x][y]['text'] = i
                            currentGrid[x][y] = i
                            self.solvePuzzle(currentGrid)

                            # Checks if the grid is solved after function comes off the stack
                            if 0 not in [num for row in currentGrid for num in row]:
                                return

                            # Backtracks when no valid entries can be found for an empty square
                            self.buttonList[x][y]['text'] = '  '
                            currentGrid[x][y] = 0
                    return
        return




    def eraseButtonFunc(self):
        self.nullifyGrid()

        # Erases the progress the user input
        for subList in self.buttonList:
            for button in subList:
                # If the button has no command i.e. it is not a 'given clue' its text is erased
                if 'null' not in str(button['command']):
                    button['text'] = '  '





    def emptyGridFunc(self):
        self.nullifyGrid()
        # Removes all values from the grid

        for subList in self.buttonList:
            for button in subList:
                button['command'] = lambda butt=button: self.gridButtonFunc(butt)
                button['text']    = '  '




    def gridButtonFunc(self, thisButton):
        # Cool function that only empty buttons get to execute

        x = thisButton.grid_info()['row']
        y = thisButton.grid_info()['column']
        thisButton.grid_forget()

        tempEntry = Entry(width=3)
        tempEntry.grid(row=x, column=y)

        self.gridEntryList.append(tempEntry)




    def createGridButtons(self):
        # Creates the 81 buttons and puts them on the grid
        self.buttonList = [[] for _ in range(9)]

        for x in range(9):
            for y in range(9):

                gridButton = Button(self.root, text="  ", padx=4)
                gridButton['command'] = lambda butt=gridButton: self.gridButtonFunc(butt)

                gridButton.grid(
                    row   =int(x + (x // 3 )),
                    column=int(y + (y // 3 )))

                self.buttonList[x].append(gridButton)

        # Add extra space to delineate boxes
        self.root.grid_rowconfigure(3, minsize=4)
        self.root.grid_rowconfigure(7, minsize=4)
        self.root.grid_columnconfigure(3, minsize=4)
        self.root.grid_columnconfigure(7, minsize=4)
        self.root.grid_columnconfigure(11, minsize=4)




    def createSideButtons(self):
        # Side bar buttons :)

        # Names
        confirmButton   = Button(self.root, text="Confirm Value",  width=11)
        newPuzzleButton = Button(self.root, text="New Puzzle",     width=11)
        checkSolButton  = Button(self.root, text="Check Solution", width=11)
        solveButton     = Button(self.root, text="Solve",          width=11)
        eraseButton     = Button(self.root, text="Erase Progress", width=11)
        emptyGridButton = Button(self.root, text="Empty the Grid", width=11)
        exitButton      = Button(self.root, text="Exit Program",   width=11)


        # Positions on the grid
        confirmButton.grid(  row=1, column=12)
        newPuzzleButton.grid(row=2, column=12)
        checkSolButton.grid( row=4, column=12)
        solveButton.grid(    row=5, column=12)
        eraseButton.grid(    row=6, column=12)
        emptyGridButton.grid(row=8, column=12)
        exitButton.grid(     row=9, column=12)

        # Commands that the buttons execute
        confirmButton['command']   = self.confirmButtonFunc
        newPuzzleButton['command'] = self.getNewPuzzle
        checkSolButton['command']  = self.checkSolutionFunc
        solveButton['command']     = self.solveButtonFunc
        eraseButton['command']     = self.eraseButtonFunc
        emptyGridButton['command'] = self.emptyGridFunc
        exitButton['command']      = self.root.destroy




    def main(self):
        # Super epic main function

        Game = Sudoku(root, puzzleList)
        Game.createGridButtons()
        Game.createSideButtons()

        self.root.mainloop()


Sudoku(root, puzzleList).main()
