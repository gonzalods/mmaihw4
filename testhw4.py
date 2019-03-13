from Grid       import Grid
from PlayerAI   import PlayerAI
from random     import randint
import time

defaultProbability = 0.9
possibleNewTiles = [2, 4]
over       = False
timeLimit = 0.2
allowance = 0.05
#prevTime = time.clock()
def getNewTileValue():
    if randint(0,99) < 100 * defaultProbability:
        return possibleNewTiles[0]
    else:
        return possibleNewTiles[1]

def updateAlarm(currTime, prevTime):
    if currTime - prevTime > timeLimit + allowance:
        print "Tiempo Excedido",
        over = True
    else:
        while time.clock() - prevTime < timeLimit + allowance:
            pass

        prevTime = time.clock()
        
def main():
    prevTime = time.clock()
    playerAI  = PlayerAI()
    grid = Grid()
    cells = grid.getAvailableCells()
    for i in range(2):
        cell = cells[randint(0, len(cells) - 1)]
        grid.setCellValue(cell, getNewTileValue())
    #grid.map = [[4, 8, 16, 2], [16, 32, 64, 32], [4, 128, 512, 256], [2, 2, 4, 64]] 
    #grid.map = [[0, 0, 0, 0], [0, 0, 0, 2], [0, 0, 4, 0], [0, 0, 0, 0]]
    grid.map = [[2, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    print playerAI.getMove(grid)
    updateAlarm(time.clock(), prevTime)
    
if __name__ == '__main__':
    main()