import pygame
import time

def drawBoard():
    pygame.init()


    #set display
    gameDisplay = pygame.display.set_mode((800,800))

    QUEEN_IMAGE_LIST= []
    for queenImg in range(8):
        picture = pygame.image.load("queenPiece.png").convert_alpha()
        picture = pygame.transform.scale(picture, (100,100))
        QUEEN_IMAGE_LIST.append(picture)
    #caption
    pygame.display.set_caption("ChessBoard")
    cellSize=100
    board = pygame.Surface(((800,800)))
    for y in range(0, 8):
        for x in range(0, 8,2):
            if y%2==0:
                pygame.draw.rect(board, 	(186,202,68), (x*cellSize+cellSize, y*cellSize, cellSize, cellSize))
                pygame.draw.rect(board,	(238,238,210), (x*cellSize, y*cellSize, cellSize, cellSize))
            else:
                pygame.draw.rect(board, 	(238,238,210), (x*cellSize+cellSize, y*cellSize, cellSize, cellSize))
                pygame.draw.rect(board, 	(186,202,68), (x*cellSize, y*cellSize, cellSize, cellSize))
    gameDisplay.blit(board, board.get_rect())
    pygame.display.flip()
    return gameDisplay,board,QUEEN_IMAGE_LIST

def drawQueens(queenPlacements,gameDisplay,board,QUEEN_IMAGE_LIST):
    unpaintedBoard = board.copy()


    for firstQueenIndex,firstQueenPlacmentTuple in enumerate(queenPlacements):
        for secondQueenIndex,secondQueenPlacmentTuple in enumerate(queenPlacements):
            # checking if the same queen
            if firstQueenIndex!=secondQueenIndex and firstQueenPlacmentTuple==secondQueenPlacmentTuple:
                pygame.draw.rect(board, 	(0,0,255), (100*(firstQueenPlacmentTuple[0]-1),100*(firstQueenPlacmentTuple[1]-1), 100, 100))
                continue
            if firstQueenPlacmentTuple==secondQueenPlacmentTuple:
                continue
            # checking if on the same row
            if firstQueenPlacmentTuple[0] == secondQueenPlacmentTuple[0]:
                pygame.draw.rect(board, 	(255,0,0), (100*(firstQueenPlacmentTuple[0]-1),100*(firstQueenPlacmentTuple[1]-1), 100, 100))
                continue
            # checking if on the same column
            if firstQueenPlacmentTuple[1] == secondQueenPlacmentTuple[1]:
                pygame.draw.rect(board, 	(255,0,0), (100*(firstQueenPlacmentTuple[0]-1),100*(firstQueenPlacmentTuple[1]-1), 100, 100))
                continue
            # checking left-down and right-up diaognal
            if firstQueenPlacmentTuple[0] - firstQueenPlacmentTuple[1] == \
             secondQueenPlacmentTuple[0] - secondQueenPlacmentTuple[1]:
                pygame.draw.rect(board, 	(255,0,0), (100*(firstQueenPlacmentTuple[0]-1),100*(firstQueenPlacmentTuple[1]-1), 100, 100))
                continue
            # checking left-up and right-down diaognal
            if firstQueenPlacmentTuple[0] + firstQueenPlacmentTuple[1] == \
             secondQueenPlacmentTuple[0] + secondQueenPlacmentTuple[1]:
                pygame.draw.rect(board, 	(255,0,0), (100*(firstQueenPlacmentTuple[0]-1),100*(firstQueenPlacmentTuple[1]-1), 100, 100))
                continue


    for queenNum,queenPlacement in enumerate(queenPlacements):
        queenImage = QUEEN_IMAGE_LIST[queenNum]
        queenRect= queenImage.get_rect()
        queenRect= queenRect.move((100*(queenPlacement[0]-1),100*(queenPlacement[1]-1)))
        board.blit(queenImage,queenRect,special_flags=pygame.BLEND_RGBA_MULT)
        gameDisplay.blit(board,board.get_rect())
        pygame.display.flip()
    time.sleep(0.1)
    return unpaintedBoard