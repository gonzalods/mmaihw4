from random import randint
from BaseAI import BaseAI
from collections import deque
import math
import sys

class PlayerAI(BaseAI):

    def __init__(self):
        self.LIMIT = 4
        #self.depth = 0
        #self.iniAvCells = 0
    
    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0, len(moves) - 1)] if moves else None
        return self.alfaBeta(grid)
        
    def alfaBeta(self, grid):
        #print(grid.map)
        #iniAvCells = len(grid.getAvailableCells())
        #maxTile = grid.getMaxTile()
        #exponent = int(log(maxTile,2))
        #if iniAvCells <= 6:
        #    self.LIMIT = 6
        #print(self.LIMIT)
        moves = grid.getAvailableMoves()
        #print("Initial Actions {}".format(moves))
        alfa = float("-inf")
        maxValue = float("-inf")
        betterMove = moves[0]
        for move in moves:
            #print("Max action {}:".format(move))
            val = self.minValue(self.maxResult(grid, move),alfa, float("inf"), 2)
            #print("valor {} para movimiento {}".format(val,move))
            alfa = max(alfa,val)
            if val > maxValue:
                maxValue = val
                betterMove = move
        return betterMove   
    
    def maxValue(self, grid, alfa, beta, depth):
        #self.depth = self.depth + 1
        if self.terminalState(grid, depth):
            return self.heuristic(grid)
        
        value = float("-inf")
        for action in self.maxActions(grid):
            #print("Max action {}:".format(action))
            value = max(value, self.minValue(self.maxResult(grid,action),alfa,beta, depth + 1))
            if value >= beta: return value
            alfa = max(alfa,value)
        
        #self.depth = self.depth - 1
        return value
    
    def minValue(self, grid, alfa, beta, depth):
        #self.depth = self.depth + 1
        #if self.terminalState(grid, depth):
        #    return self.heuristic(grid)
        
        value = float("inf")
        for action in self.minActions(grid):
            value = min(value, self.maxValue(self.minResult(grid,action),alfa,beta, depth + 1))
            if value <= alfa: return value
            beta = min(beta, value)
        
        #self.depth = self.depth - 1
        return value
    
    def maxActions(self, grid):
        return grid.getAvailableMoves()
    
    def minActions(self, grid):
        actions = []
        cells = grid.getAvailableCells()
        posibles = {2:[], 4:[]}
        for posible in posibles.iterkeys():
            for cell in cells:
                newGrid = grid.clone()
                newGrid.insertTile(cell, posible)
                rank = -self.adjacents(newGrid)
                posibles[posible].append(rank)
        
        maxRank = min(min(posibles[2]), min(posibles[4]))
        #print("maxRank: {} -- posibles {}".format(maxRank, posibles))
        for posible in posibles.iterkeys():
            for i, rank in enumerate(posibles[posible]):
                if rank == maxRank:
                    actions.append(tuple([cells[i],posible]))
        #print("action {}".format(actions))
        return actions                

        
    def maxResult(self, grid, move):
        newGrid = grid.clone()
        newGrid.move(move)
        return newGrid
        
    def minResult(self, grid, (cell, value)):
        newGrid = grid.clone()
        newGrid.insertTile(cell, value)
        return newGrid
    
    def terminalState(self, grid, depth):
        numAvblCells = len(grid.getAvailableCells())
        if numAvblCells > 4 and depth >= 4:
            return True
        if numAvblCells <= 4 and depth >= 6:
            #self.depth = self.depth - 1
            return True
        #if grid.getMaxTile() == self.LIMIT:
        #if len(grid.getAvailableMoves()) == 0:
        #if len(grid.getAvailableCells()) == 0 or len(grid.getAvailableMoves()) == 0:
            #print("Se llenan rama {} con profundidad {}".format(grid.map, self.depth))
            #self.depth = self.depth - 1
            #sys.exit()
        #    return True        
        #if self.heuristic(grid):
            #print("Se llega al destino {} con profundidad {}".format(grid.map, self.depth))
            #self.depth = self.depth - 1
            #if self.depth == 32:
            #    sys.exit()
            #return True
        return False
    
    def utility(self, grid):
        return grid.getMaxTile()
        
    def heuristic(self, grid):
        avCells = len(grid.getAvailableCells())
        #if(avCells == 0):
        #    return grid.getMaxTile()
        #else:
        #    avCells = math.log(avCells)
        #print("celdas: {} -- grid: {}".format(avCells, grid.map))
        maxValue = math.log(grid.getMaxTile(),2)
        #logAvg = self.average(grid)
        #scoreEdges = self.scoreEdges(grid)
        monotonocity = self.monotonic(grid)
        adjacents = self.adjacents(grid)
        return 2.7*avCells +1.0*monotonocity + 1.5*maxValue + 1.0*adjacents #11.0*logAvg + 700.0*adjacents + 47.0*monotonocity 

    def average(self,grid):
        avg = 0
        count = 0
        for rows in grid.map:
            for elm in rows:
                if elm > 4:
                    avg = avg + math.log(elm, 2)
                    count = count + 1
        if count > 0:
            avg = float(avg) / count
        return avg
        
    def scoreEdges(self, grid):
        maxTile = grid.getMaxTile()
        trans = map(list, zip(*grid.map))
        if grid.map[0][0] >= maxTile/2 or grid.map[0][3] >= maxTile/2 \
            or grid.map[3][0] >= maxTile/2 or grid.map[3][3] >= maxTile/2:
            maxTile = (grid.map[0][0] + grid.map[0][3] + grid.map[3][0] + grid.map[3][3]) * 2
        elif max(grid.map[0]) >= maxTile/2 or max(grid.map[3]) >= maxTile/2 \
            or max(trans[0]) >= maxTile/2 or max(trans[3]) >= maxTile/2:
            maxTile = max(grid.map[0]) + max(grid.map[3]) + max(trans[0]) + max(trans[3])
        else:
            maxTile = maxTile / (math.log(maxTile,2) - 1)

        if maxTile > 0:
            maxTile = math.log(maxTile, 2)
        return maxTile
        
    def monotonic(self, grid):
        totals = [0, 0, 0, 0]
            
        for row in grid.map:
            for i in range(len(row)-1):
                current = row[i]
                next = row[i+1]
                if current > 0:
                    current = math.log(current,2)
                if next > 0:
                    next = math.log(next,2)
                if current > next:
                    totals[0] = totals[0] + next - current
                elif next > current:
                    totals[1] = totals[1] + current - next

        
        trans = map(list, zip(*grid.map))
        for col in trans:
            for i in range(len(col)-1):
                current = col[i]
                next = col[i+1]
                if current > 0:
                    current = math.log(current,2)
                if next > 0:
                    next = math.log(next,2)
                if current > next:
                    totals[2] = totals[0] + next - current
                elif next > current:
                    totals[3] = totals[1] + current - next
        

        return max(totals[0], totals[1]) + max(totals[2], totals[3])
    
    def adjacents(self, grid):
        result = 0
        prevVal = 0
        count = 0
        for row in grid.map:
            prevVal = 0
            for i in range(len(row)):
                val = row[i]
                if val != 0:
                    if val == prevVal:
                        count = count + 1
                    elif count > 0:
                        result = result + (count + 1) * math.log(prevVal,2)
                        count = 0
                    
                    prevVal = val

            if count > 0:
                result = result + (count + 1) * math.log(prevVal,2)
            prevVal = 0
            count = 0
        
        trans = map(list, zip(*grid.map))
        for col in trans:
            prevVal = 0
            for i in range(len(col)):
                val = col[i]
                if val != 0:
                    if val == prevVal:
                        count = count + 1
                    elif count > 0:
                        result = result + (count + 1) * math.log(prevVal,2)
                        count = 0
                    
                    prevVal = val

            if count > 0:
                result = result + (count + 1) * math.log(prevVal,2)
            prevVal = 0
            count = 0
            
        return result      