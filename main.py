import pygame as pg
from graphics import dWidth, dHeight, background, pieceImages, highlightedImg, checkImg
from board import Board
from boardFuncs import testCheckmate, kingCheck, pawnPromote
import copy
import time
# pygame setup
pg.init()

screen = pg.display.set_mode((dWidth, dHeight))
clock = pg.time.Clock()
running = True

board = Board()
squareWidth = dWidth/8
squareHeight = dHeight/8

moved = False
gameStates = [] # save previous states of game

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            clickX, clickY = event.pos
            squareClicked = (int(clickX/squareWidth), 7 - int(clickY/squareHeight)) # convert click position to a square on board
            if board.highlightedPiece == None:
                board.selectPiece(squareClicked) # select square and make it the highlighted piece
                if board.highlightedPiece != None:
                    if board.highlightedPiece.colour != board.turn:
                        board.highlightedPiece, board.highlightedSquare = None, None
            else:
                moved, board.dict = board.highlightedPiece.move(squareClicked, board.dict, board.move)
                #check for pawn promotion
                if moved and board.highlightedPiece.type == "pawn" and board.highlightedPiece.position[1] in [0, 7]:
                    promotion = pawnPromote(screen=screen)
                    if promotion == None:
                        board = gameStates[-1]
                        gameStates[-1] = copy.deepcopy(board)
                    else:
                        board.highlightedPiece.type = promotion
                
                #reset highlighted piece
                board.highlightedPiece, board.highlightedSquare = None, None
                
                #reject the move if it makes the players king go into check
                if board.kingCheck(board.turn, board.dict)[0]:
                    board = gameStates[-1]
                    gameStates[-1] = copy.deepcopy(board) # make sure not editing last safe position
                elif moved:
                    board.move += 1
                    board.changeTurn()
                    gameStates.append(copy.deepcopy(board))

    
    screen.blit(background, (0,0))
        
    
    #display all of the pieces based on contents of board.dict
    mapping = board.dict

    for key in mapping.keys():
        piece = mapping[key]
        if piece == None:
            pass
        else:
            pieceImage = pieceImages[piece.colour+piece.type]
            screen.blit(pieceImage, (key[0]*squareWidth, dHeight - squareHeight - key[1]*squareHeight ))
    
    #put a box around highlighted piece
    if board.highlightedSquare != None:
            screen.blit(highlightedImg, (board.highlightedSquare[0]*squareWidth, dHeight - squareHeight - board.highlightedSquare[1]*squareHeight ))
    
    #put a box around king if in check
    wCheck, bCheck = kingCheck("white", board.dict), kingCheck("black", board.dict)
    if wCheck[0]:
        screen.blit(checkImg, (wCheck[1][0]*squareWidth, dHeight - squareHeight - wCheck[1][1]*squareHeight ))
    if bCheck[0]:
        screen.blit(checkImg, (bCheck[1][0]*squareWidth, dHeight - squareHeight - bCheck[1][1]*squareHeight ))
    
    #if in check, check for checkmate
    if moved:
        if testCheckmate(board=board, turn=board.turn):
            board.changeTurn()
            pg.display.update()
            if  (wCheck[0] or bCheck[0]):
                print(f"Checkmate, {board.turn} wins!")
            else:
                print("Stalemate! No avaliable moves.")
            time.sleep(1)
            pg.quit()
    moved = False
    pg.display.update()
    time.sleep(0.1)

pg.quit()
