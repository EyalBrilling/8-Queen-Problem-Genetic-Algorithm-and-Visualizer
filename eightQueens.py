import random
import math
import pygame
import time
UNIT_MUTITION,SEP_MUTITION = 0,1
POP_SIZE = 50
MUTATION_PROB = 0.125



def singleCrossover(father,mother):
    randomIndex= random.choice(range(8))
    firstChild= father[:randomIndex] +mother[randomIndex:]
    secondChild= mother[:randomIndex] +father[randomIndex:]
    return [firstChild,secondChild]

def initiateChromosomes(popSize):
    chromosomesList=[]
    for pop in range(popSize):
        # each chromosome get created by 
        # 1) making 2 shuffled lists of rows and columns(no collisions)
        # 2) creating the placement tuples with a "for-in" loop over the shuffled lists
        chromosomesList.append([(row,column) for row,column in \
         zip(random.sample([x for x in range(1,9)],8),random.sample([x for x in range(1,9)],8))])
    return chromosomesList
    

def mutation(chromosome,mutiotionType):
    if mutiotionType== UNIT_MUTITION:
        for placementIndex,placement in enumerate(chromosome):
            placementList = list(placement)
            if random.random() < MUTATION_PROB:
                placementList= (random.randint(1,8),random.randint(1,8))
            chromosome[placementIndex] = tuple(placementList)
        return chromosome

    if mutiotionType== SEP_MUTITION:
        for placementIndex,placement in enumerate(chromosome):
            placementList = list(placement)
            for tupleIndex,cooridinate in enumerate(placementList):
                if random.random() < MUTATION_PROB:
                    placementList[tupleIndex] = (random.randint(1,8))
            chromosome[placementIndex] = tuple(placementList)
        return chromosome

def calculateChromosomeValue(chromosome):
    score=0
    for firstQueenPlacmentTuple in chromosome:
        for secondQueenPlacmentTuple in chromosome:
            # checking if the same queen
            if firstQueenPlacmentTuple==secondQueenPlacmentTuple:
                continue
            # checking if on the same row
            if firstQueenPlacmentTuple[0] == secondQueenPlacmentTuple[0]:
                continue
            # checking if on the same column
            if firstQueenPlacmentTuple[1] == secondQueenPlacmentTuple[1]:
                continue
            # checking left-down and right-up diaognal
            if firstQueenPlacmentTuple[0] - firstQueenPlacmentTuple[1] == \
             secondQueenPlacmentTuple[0] - secondQueenPlacmentTuple[1]:
                continue
            # checking left-up and right-down diaognal
            if firstQueenPlacmentTuple[0] + firstQueenPlacmentTuple[1] == \
             secondQueenPlacmentTuple[0] + secondQueenPlacmentTuple[1]:
                continue

            score +=1
    return int(score/2) # remove duplicates count

def pairingStage(chromosomeList,mutitionType):
    pairs=[]
    children=[]
    scoreList=[]
    for chromosome in chromosomeList:
        scoreList.append(calculateChromosomeValue(chromosome))
    chromosomeWeights = [max([1,math.pow((score-20),3)]) for score in scoreList]
    for pairNum in range(int(POP_SIZE/2)):
        pairs.append(random.choices(chromosomeList,weights=chromosomeWeights,k=2))
    for pair in pairs:
        children += singleCrossover(*pair)
    for child in children:
        child = mutation(child,mutitionType)
    return children

def bruteForce():
    tries=0
    while True:
        tries+=1
        
        chromosome=[]
        for queen in range(8):
            chromosome.append((random.randint(1,8),random.randint(1,8)))
            print(str(tries) +"  " +str(calculateChromosomeValue(chromosome)) + "\n")
        if calculateChromosomeValue(chromosome) == 28:
            print(str(chromosome) +"\n" + "FOUND IN " + str(tries) + " LOOPS.\n")
            return

def printBestChromosome(chromosomeList):
    scoreList=[]
    for chromosome in chromosomeList:
        scoreList.append(calculateChromosomeValue(chromosome))
    bestScore=max(scoreList)
    print(str(chromosomeList[scoreList.index(bestScore)]) + "SCORE:" + str(bestScore) + "\n")
    return chromosomeList[scoreList.index(bestScore)]

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
    time.sleep(0.5)
    return unpaintedBoard
        
def main():
    generationsCounter=0
    loopCounter=0
    overall=0
    NUMBER_OF_LOOPS= 1

    gameDisplay,board,QUEEN_IMAGE_LIST=drawBoard()
    chromosomeList = initiateChromosomes(POP_SIZE)
    while True:
        generationsCounter+=1
        bestChromosome=printBestChromosome(chromosomeList)
        board = drawQueens(bestChromosome,gameDisplay,board,QUEEN_IMAGE_LIST)
        for chromosome in chromosomeList:
            if calculateChromosomeValue(chromosome)== 28:
                print("FOUND SOLUTION:" + str(chromosome))
                chromosomeList = initiateChromosomes(POP_SIZE)
                time.sleep(5)
                overall+=generationsCounter
                generationsCounter=0
                loopCounter+=1
                if loopCounter==NUMBER_OF_LOOPS:
                    print("TOTAL:" + str(overall) + ". " + "MEAN:" + str(overall/NUMBER_OF_LOOPS))
                    ####### bruteForce()
                    return

        chromosomeList=pairingStage(chromosomeList,SEP_MUTITION)
        #print(generationsCounter)
        









if __name__=="__main__":
    main()