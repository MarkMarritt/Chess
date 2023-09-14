from pieces import Piece

class Board:
    def __init__(self):
        self.turn = "white"
        self.dict = self.createDict()

    def createDict(self):
        """creates an empty dictionary of the board"""
        boardDict = {}
        for column in range(8):
            for row in range(8):
                boardDict[[column, row]] = None
        
        return boardDict
    
    def addPieces(self):
        """adds all of the pieces in their stating positions"""
        for column in range(8):
            self.dict[[column, 1]] = Piece([column, 1], "pawn", "white", self.dict)
            self.dict[[column, 6]] = Piece([column, 1], "pawn", "black", self.dict)
        #rooks
        self.dict[[0, 0]] = Piece([0, 0], "rook", "white", self.dict)
        self.dict[[7, 0]] = Piece([7, 0], "rook", "white", self.dict)
        self.dict[[0, 7]] = Piece([0, 7], "rook", "black", self.dict)
        self.dict[[7, 7]] = Piece([7, 7], "rook", "black", self.dict)
        
        #knights
        self.dict[[1, 0]] = Piece([1, 0], "knight", "white", self.dict)
        self.dict[[6, 0]] = Piece([6, 0], "knight", "white", self.dict)
        self.dict[[1, 7]] = Piece([1, 7], "knight", "black", self.dict)
        self.dict[[6, 7]] = Piece([6, 7], "knight", "black", self.dict)
        
        #bishops
        self.dict[[2, 0]] = Piece([2, 0], "bishop", "white", self.dict)
        self.dict[[5, 0]] = Piece([5, 0], "bishop", "white", self.dict)
        self.dict[[2, 7]] = Piece([2, 7], "bishop", "black", self.dict)
        self.dict[[5, 7]] = Piece([5, 7], "bishop", "black", self.dict)

        #queens
        self.dict[[3, 0]] = Piece([3, 0], "queen", "white", self.dict)
        self.dict[[3, 7]] = Piece([3, 7], "queen", "black", self.dict)

        #kings
        self.dict[[4, 0]] = Piece([4, 0], "king", "white", self.dict)
        self.dict[[4, 7]] = Piece([4, 7], "king", "black", self.dict)

    def changeTurn(self):
        """change colour of whos turn it is"""
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"