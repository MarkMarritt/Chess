import numpy as np
from boardFuncs import kingCheck
from copy import deepcopy


class Piece:
    def __init__(self, postion, type, colour, boardDict):
        self.position = np.array(postion) # store as a tuple (1 2) 
        self.type = type
        self.colour = colour
        self.boardDict = boardDict # of form {(1,3) : "None", (1,2) : piece obj}
        self.onStart = True
        self.lastMove = None
        self.pawnDoubleLast = False

    def move(self, endSquare, boardDict, moveNo):
        """move piece, returns if moved and updated dictionary"""
        self.pawnDoubleLast = False, self.boardDict
        self.boardDict = boardDict
        moveType = self.defineMove(endSquare, moveNo)
        endPiece = self.getPieceOn(endSquare)
        #check that a move is valid
        if moveType == "invalid":
            return False, self.boardDict
        if endPiece == None:
            pass
        elif endPiece.colour == self.colour:
            self.pawnDoubleLast = False
            return False, self.boardDict
        if moveType not in ["lshap", "single", "castle"]:
            path = self.generatePath(endSquare, moveType=moveType)
            for square in path:
                if self.getPieceOn(square=square) != None:
                    self.pawnDoubleLast = False
                    return False, self.boardDict
        #castling
        if moveType == "castle":
            rookPos = self.canCastle(endSquare, moveNo=moveNo)[1]
            rook = self.boardDict[rookPos]
            rookSquare = ((endSquare -self.position)[0]/2 + self.position[0], self.position[1])
            rookSquare = (int(rookSquare[0]), int(rookSquare[1]))
            self.boardDict[rookSquare] = rook
            self.boardDict[rookPos] = None
            rook.position = rookSquare
            

        self.moveOnBoard(endSquare, moveNo=moveNo)
        return True, self.boardDict
    
    def generatePath(self, end, moveType):
        """return a list of all coords piece passes thru"""
        end = np.array(end)
        x0, y0, x1, y1 = self.position[0], self.position[1], end[0], end[1]
        pathOut = []
        if moveType == "diag":
            incrx = 1 if x0 - x1 < 0 else -1
            xcoords = np.arange(x0, x1, incrx)
            incry = 1 if y0 - y1 < 0 else -1
            ycoords = np.arange(y0, y1, incry)
            for x in range(abs(x0 - x1)):
                if x == 0:
                    continue
                pathOut.append((xcoords[x], ycoords[x]))
        elif moveType == "horz":
            incrx = 1 if x0 - x1 < 0 else -1
            xcoords = np.arange(x0, x1, incrx)
            for x in range(abs(x0-x1)):
                if x == 0:
                    continue
                pathOut.append((xcoords[x], y0))
        elif moveType == "vert":
            incry = 1 if y0 - y1 < 0 else -1
            ycoords = np.arange(y0, y1, incry)
            for x in range(abs(y0 - y1)):
                if x == 0:
                    continue
                pathOut.append((x0, ycoords[x]))

        else:
            assert("Wrong move code")
        return pathOut
    
    def defineMove(self, end, moveNo):
        """define what type of move it is"""
        end = np.array(end)
        if -1 < end[0] < 8 and -1 < end[1] < 8:
            pass
        else:
            return "invalid"
        if end[0] == self.position[0] and end[1] != self.position[1] and self.type in ["rook", "queen"]:
            return "vert"
        elif end[0] != self.position[0] and end[1] == self.position[1] and self.type in ["rook", "queen"]:
            return "horz"
        elif abs((end - self.position)[0]) == abs((end - self.position)[1]) and self.type in ["bishop", "queen"]:
            return "diag"
        elif ((abs((end - self.position)[0]) == 1 and abs((end - self.position)[1]) == 2) or (abs((end - self.position)[0]) == 2 and abs((end - self.position)[1]) == 1)) and self.type == "knight":
            return "lshap"
        elif end[0] == self.position[0] and abs(end[1] - self.position[1]) == 2 and self.type == "pawn" and self.onStart and self.getPieceOn(end) == None:
            if ((end[1] > self.position[1]) and self.colour == "white") or ((end[1] < self.position[1]) and self.colour == "black"):
                self.pawnDoubleLast = True
                return "vert"
            else:
                return "invalid"
        elif end[0] == self.position[0] and abs(end[1] - self.position[1]) == 1 and self.type == "pawn":
            if ((end[1] > self.position[1]) and self.colour == "white") or ((end[1] < self.position[1]) and self.colour == "black"):
                return "vert"
            else:
                return "invalid"
        elif abs((end - self.position)[0]) == abs((end - self.position)[1]) and abs((end - self.position)[1]) == 1 and self.type in ["pawn"]:
            if self.canPawnTake(end=end, moveNo=moveNo):
                return "diag"
            else:
                return "invalid"
        elif abs((end - self.position)[0]) < 2 and abs((end - self.position)[1]) < 2 and self.type == "king":
            return "single"
        elif abs((end - self.position)[0]) == 2 and end[1] == self.position[1] and self.type == "king" and self.onStart and self.canCastle(end, moveNo=moveNo)[0]:
            return "castle"
        else:
            return "invalid" # need to add castling and promotion etc
    
    def getPieceOn(self, square):
        """get piece on a certain square, 
        return -none if empty
                -colour"""
        square = (square[0], square[1])
        if not -1 < square[0] < 8 or  not -1 < square[1] < 8:
            return None 
        info = self.boardDict[square]
        if info == None:
            return None
        else:
            return info
    
    def canPawnTake(self, end, moveNo):
        """determine wheter a pawn can take to the end position"""
        endPiece = self.getPieceOn(end)
        if (end[1] > self.position[1] and self.colour == "black") or (end[1] < self.position[1] and self.colour == "white"):
            return False
        if endPiece != None:
            if endPiece.colour == self.colour:
                return False
            else:
                return True
        else:
            #check enpassent
            direction = 1 if self.colour == "black" else -1
            end[1] = end[1] + direction
            endPiece = self.getPieceOn(end)
            if endPiece != None:
                if endPiece.type == "pawn" and endPiece.lastMove == moveNo - 1 and endPiece.pawnDoubleLast:
                    if endPiece.colour == self.colour:
                        return False
                    else:
                        self.boardDict[(end[0], end[1])] = None
                        return True
                else:
                    return False
    
    #very messy function :(
    def canCastle(self, end, moveNo):
        """checks to see if castling is possible"""
        #check that there is nothing between rook and king and that the rook is on starting square
        endDir = 1 if end[0] - self.position[0] > 0 else -1
        diff = endDir
        rookPos = None
        for _ in range(2):
            rook = self.getPieceOn((end[0] + endDir, end[1]))
            if rook != None:
                if rook.type == "rook" and rook.onStart:
                    rookPos = (end[0] + endDir, end[1])
                    break
            endDir += diff
        if rookPos == None:
            return (False, None)
        
        tempDict = deepcopy(self.boardDict) # save a copy of the current state and replace back after checking
        tempPos = np.array([self.position[0], self.position[1]])
        if kingCheck(self.colour, self.boardDict)[0]:
            self.boardDict = tempDict
            self.position = tempPos
            return (False, None)
        path = self.generatePath(end, "horz") 
        path.append(end)
        for pos in path:
            self.move(pos, self.boardDict, moveNo)
            if kingCheck(self.colour, self.boardDict)[0]:
                self.boardDict = tempDict
                self.position = tempPos
                return (False, None)
        self.boardDict = tempDict
        self.position = tempPos
        return (True, rookPos) 

    def moveOnBoard(self, end, moveNo):
        """change position on board"""
        self.boardDict[(self.position[0], self.position[1])] = None
        self.position = np.array(end)
        self.boardDict[(self.position[0], self.position[1])] = self
        self.onStart = False
        self.lastMove = moveNo
    
    
