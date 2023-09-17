from copy import deepcopy
import pygame as pg
from graphics import promotionImg, dHeight, dWidth
import time

squareWidth = dWidth/8
squareHeight = dHeight/8

def kingCheck(colour, posDict):
    """checks to see if a king is in check"""
    king = None
    for piece in posDict.values():
        if piece == None:
            continue
        elif piece.type == "king" and piece.colour == colour:
            king = piece
    if king == None:
        return (False, None)
    pos = king.position # note this is as an np array 
    #check horz
    for i in range(7 - pos[0]):
        piece = posDict[(pos[0] + i + 1, pos[1])]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "rook"]:
                return (True, pos)
            break
    for i in range(pos[0]):
        piece = posDict[(pos[0] - i - 1, pos[1])]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "rook"]:
                return (True, pos)
            break
    #checkVert
    for i in range(7 - pos[1]):
        piece = posDict[(pos[0], pos[1] + i + 1)]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "rook"]:
                return (True, pos)
            break
    for i in range(pos[1]):
        piece = posDict[(pos[0], pos[1] - i - 1)]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "rook"]:
                return (True, pos)
            break
    #checkDiag
    i = 1
    while pos[0] + i < 8 and pos[1] + i < 8:
        piece = posDict[(pos[0] + i, pos[1] + i)]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "bishop"]:
                return (True, pos)
            break
        i += 1
    i = 1
    while pos[0] + i < 8 and pos[1] - i > -1:
        piece = posDict[(pos[0] + i, pos[1] - i)]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "bishop"]:
                return (True, pos)
            break
        i += 1
    i = 1
    while pos[0] - i > -1 and pos[1] + i < 8:
        piece = posDict[(pos[0] - i, pos[1] + i)]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "bishop"]:
                return (True, pos)
            break
        i += 1
    i = 1
    while pos[0] - i > -1 and pos[1] - i > -1:
        piece = posDict[(pos[0] - i, pos[1] - i)]
        if piece != None:
            if piece.colour != king.colour and piece.type in ["queen", "bishop"]:
                return (True, pos)
            break
        i += 1
    #check knights
    differences = [(1, 2), (1,-2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    for difference in differences:
        ksquare = (pos[0] + difference[0], pos[1] + difference[1])
        if -1 < ksquare[0] < 8 and -1 < ksquare[1] < 8:
            piece = posDict[ksquare]
            if piece != None:
                if piece.colour != king.colour and piece.type in ["knight"]:
                    return (True, pos)
    #check kings
    differences = [(1, 0), (1, 1), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]
    for difference in differences:
        dsquare = (pos[0] + difference[0], pos[1] + difference[1])
        if -1 < dsquare[0] < 8 and -1 < dsquare[1] < 8:
            piece = posDict[dsquare]
            if piece != None:
                if piece.colour != king.colour and piece.type in ["king"]:
                    return (True, pos)
    #check pawns
    diff = 1 if king.colour == "white" else -1
    differences = [(1, diff), (-1, diff)]
    for difference in differences:
        dsquare = (pos[0] + difference[0], pos[1] + difference[1])
        if -1 < dsquare[0] < 8 and -1 < dsquare[1] < 8:
            piece = posDict[dsquare]
            if piece != None:
                if piece.colour != king.colour and piece.type in ["pawn"]:
                    return (True, pos)
    return (False, pos)

def testCheckmate(board, turn):
    """checks to see if there is a checkmate on board"""
    for piece in board.dict.values():
        if piece != None:
            for i in range(8):
                for j in range(8):
                    if piece.colour != turn:
                        continue
                    tBoard = deepcopy(board)
                    tPiece = deepcopy(piece)
                    moved, _ = tPiece.move((i, j), tBoard.dict, tBoard.move)
                    if moved:
                        if not kingCheck(turn, tBoard.dict)[0]:
                            return False
    return True

def pawnPromote(screen):
    """returns what the piece is promoted to"""
    screen.blit(promotionImg, (dWidth*3/8, dHeight*3/8))
    pg.display.update()
    notClicked = True
    while notClicked:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                clickX, clickY = event.pos
                squareClicked = (int(clickX/squareWidth), 7 - int(clickY/squareHeight))
                if squareClicked == (3,4):
                    return "knight"
                if squareClicked == (3,4):
                    return "rook"
                if squareClicked == (4,4):
                    return "queen"
                if squareClicked == (4,3):
                    return "bishop"
                else:
                    return None
