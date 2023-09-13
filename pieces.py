import numpy as np

class Piece:
    def __init__(self, postion, type, colour, boardDict):
        self.position = postion # store as a numpy array (1 2) 
        self.type = type
        self.colour = colour
        self.boardDict = boardDict # of form {[1,3] : "None", [1,2] : ("b", "k")}
    
    def move(self, end):
        moveType = self.defineMove(end)
        endPiece = self.getPieceOn(end)
        #check that a move is valid
        if moveType == "invalid":
            return
        if endPiece == self.colour:
            return
        if moveType != "lshap":
            path = self.generatePath(end, moveType=moveType)
            for square in path:
                if self.getPieceOn(square=square) != None:
                    return
        #add castling?
            self.moveOnBoard(end)    

    def generatePath(self, end, moveType):
        """return a list of all coords piece passes thru"""
        if moveType == "diag":
            return [end + x for x in range(abs(self.position[0] - end[0]))] 
        elif moveType == "horz":
            return [np.array(end[0] + x, end[1]) for x in range(abs(self.position[0] - end[0]))] 
        elif moveType == "vert":
            return [np.array(end[0], end[1] + x) for x in range(abs(self.position[1] - end[1]))]
        else:
            assert("Wrong move code")
    
    def defineMove(self, end):
        """define what type of move it is"""
        if -1 < end[0] < 8 and -1 < end[1] < 8:
            pass
        else:
            return "invalid"
        if end[0] == self.position[0] and end[1] != self.position[1]:
            return "vert"
        elif end[0] != self.position[0] and end[1] == self.position[1]:
            return "horz"
        elif (end - self.position)[0] == (end - self.position)[1]:
            return "diag"
        elif abs(abs((end - self.position)[0]) - abs((end - self.position)[1])) == 1:
            return "lshap"
        else:
            return "invalid" # need to add castling and promotion etc
    
    def getPieceOn(self, square):
        """get piece on a certain square, 
        return -none if empty
                -colour"""
        info = self.boardDict[square]
        if info == None:
            return None
        else:
            return info[0]

    def moveOnBoard(self, end):
        """change position on board"""
        self.boardDict[self.position] = None
        self.position = end
        self.boardDict[self.position] = (self.colour, self.type)
    