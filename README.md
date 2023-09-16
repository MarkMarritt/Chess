# Chess
Chess app made using pygame.
Imports don't work on github, only on local area.
It is missing a few stalemate features.

split into 5 files:
pieces.py contains a Piece class, for each of the pieces on board. Governs being able to move each piece. \n
board.py creates a dictionary that stores all of the piece objects with corresponding positions.
graphics.py generates all of the images used and scales them appropriately.
boardFuncs.py has some miscelaneous functions, testing for checkmate, check and promoting pawns interface.
main.py initialise pygame and selects pieces, makes moves and updates the screen. 

Some messy functions that require making temporary copies of board and can be slow.
