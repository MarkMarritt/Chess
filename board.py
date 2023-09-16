from pieces import Piece
from copy import deepcopy

class Board:
    def __init__(self):
        self.turn = "white"
        self.highlightedSquare = None
        self.highlightedPiece = None
        self.dict = self.createDict()
        self.addPieces()
        self.move = 1
        self.check = None


    def createDict(self):
        """creates an empty dictionary of the board"""
        boardDict = {}
        for column in range(8):
            for row in range(8):
                boardDict[(column, row)] = None
        
        return boardDict
    
    def addPieces(self):
        """adds all of the pieces in their stating positions"""
        for column in range(8):
            self.dict[(column, 1)] = Piece((column, 1), "pawn", "white", self.dict)
            self.dict[(column, 6)] = Piece((column, 6), "pawn", "black", self.dict)
        #rooks
        self.dict[(0, 0)] = Piece((0, 0), "rook", "white", self.dict)
        self.dict[(7, 0)] = Piece((7, 0), "rook", "white", self.dict)
        self.dict[(0, 7)] = Piece((0, 7), "rook", "black", self.dict)
        self.dict[(7, 7)] = Piece((7, 7), "rook", "black", self.dict)
        
        #knights
        self.dict[(1, 0)] = Piece((1, 0), "knight", "white", self.dict)
        self.dict[(6, 0)] = Piece((6, 0), "knight", "white", self.dict)
        self.dict[(1, 7)] = Piece((1, 7), "knight", "black", self.dict)
        self.dict[(6, 7)] = Piece((6, 7), "knight", "black", self.dict)
        
        #bishops
        self.dict[(2, 0)] = Piece((2, 0), "bishop", "white", self.dict)
        self.dict[(5, 0)] = Piece((5, 0), "bishop", "white", self.dict)
        self.dict[(2, 7)] = Piece((2, 7), "bishop", "black", self.dict)
        self.dict[(5, 7)] = Piece((5, 7), "bishop", "black", self.dict)

        #queens
        self.dict[(3, 0)] = Piece((3, 0), "queen", "white", self.dict)
        self.dict[(3, 7)] = Piece((3, 7), "queen", "black", self.dict)

        #kings
        self.dict[(4, 0)] = Piece((4, 0), "king", "white", self.dict)
        self.dict[(4, 7)] = Piece((4, 7), "king", "black", self.dict)

    def changeTurn(self):
        """change colour of whos turn it is"""
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    
    def selectPiece(self, square):
        """select a piece if there is one on the square"""
        square = (square[0], square[1])
        piece = self.dict[square]
        if piece != None:
            self.highlightedSquare = square
            self.highlightedPiece = piece
        else:
            return
        
    def kingCheck(self, colour, posDict):
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
                        moved = tPiece.move((i, j), tBoard.dict, tBoard.move)
                        if not tBoard.kingCheck(turn, tBoard.dict)[0]:
                            return False
        return True
