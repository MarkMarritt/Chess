import pygame as pg

dWidth = 720
dHeight = 720
background = pg.image.load("images/board.png")
background = pg.transform.scale(background, (dWidth, dHeight))
highlightedImg = pg.image.load("images/greyboarder.png")
highlightedImg = pg.transform.scale(highlightedImg, (dWidth/8, dHeight/8))
checkImg = pg.image.load("images/redboarder.png")
checkImg = pg.transform.scale(checkImg, (dWidth/8, dHeight/8))
promotionImg = pg.image.load("images/pawnpromotion.png")
promotionImg = pg.transform.scale(promotionImg, (dWidth/4, dHeight/4))
pieceImages = {
    "whitepawn": pg.transform.scale(pg.image.load("images/white-pawn.png"), (dWidth/8, dHeight/8)),
    "blackpawn": pg.transform.scale(pg.image.load("images/black-pawn.png"), (dWidth/8, dHeight/8)),
    "whiterook": pg.transform.scale(pg.image.load("images/white-rook.png"), (dWidth/8, dHeight/8)),
    "blackrook": pg.transform.scale(pg.image.load("images/black-rook.png"), (dWidth/8, dHeight/8)),
    "whiteknight": pg.transform.scale(pg.image.load("images/white-knight.png"), (dWidth/8, dHeight/8)),
    "blackknight": pg.transform.scale(pg.image.load("images/black-knight.png"), (dWidth/8, dHeight/8)),
    "whitebishop": pg.transform.scale(pg.image.load("images/white-bishop.png"), (dWidth/8, dHeight/8)),
    "blackbishop": pg.transform.scale(pg.image.load("images/black-bishop.png"), (dWidth/8, dHeight/8)),
    "whitequeen": pg.transform.scale(pg.image.load("images/white-queen.png"), (dWidth/8, dHeight/8)),
    "blackqueen": pg.transform.scale(pg.image.load("images/black-queen.png"), (dWidth/8, dHeight/8)),
    "whiteking": pg.transform.scale(pg.image.load("images/white-king.png"), (dWidth/8, dHeight/8)),
    "blackking": pg.transform.scale(pg.image.load("images/black-king.png"), (dWidth/8, dHeight/8))
}