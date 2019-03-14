from random import randint
from BaseAI import BaseAI
from collections import deque
import math
import sys

class PlayerAI(BaseAI):

    def __init__(self):
        self.LIMIT = 4
        self.debug = True
        #self.depth = 0
        #self.iniAvCells = 0
    
    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0, len(moves) - 1)] if moves else None
        return self.alfaBeta(grid)
        
    def alfaBeta(self, grid):
        if self.debug:
            with open("test.txt",'w') as f:
                f.write("{}\n".format(grid.map))
        #iniAvCells = len(grid.getAvailableCells())
        #maxTile = grid.getMaxTile()
        #exponent = int(log(maxTile,2))
        #if iniAvCells <= 6:
        #    self.LIMIT = 6
        #print(self.LIMIT)
        moves = grid.getAvailableMoves()
        movesrem = 0
        #print("Initial Actions {}".format(moves))
        alfa = float("-inf")
        maxValue = float("-inf")
        betterMove = moves[0]
        for move in moves:
            maxResult = self.maxResult(grid, move)
            if self.debug:
                movesrem = movesrem + 1
                with open("test.txt",'a') as f:
                    f.write("Max action {} -- depth:{} -- bf:{}-{} -- result {}\n".format(move, 1, movesrem, len(moves), maxResult.map))
                    f.flush()
            val = self.minValue(maxResult,alfa, float("inf"), 2, len(moves))
            if self.debug:
                with open("test.txt",'a') as f:
                    f.write("valor {} para movimiento {}\n".format(val,move))
                    f.flush()
            alfa = max(alfa,val)
            if val > maxValue:
                maxValue = val
                betterMove = move
        return betterMove   
    
    def maxValue(self, grid, alfa, beta, depth, bf):
        #self.depth = self.depth + 1
        #if self.terminalState(grid, depth, bf):
        #    return self.heuristic(grid, depth)
        
        value = float("-inf")
        actions = self.maxActions(grid)
        bfthis = len(actions)
        bfrem = 0
        tabs = "\t"*(depth -1)
        for action in actions:
            maxResult = self.maxResult(grid,action)
            if self.debug:
                bfrem = bfrem + 1    
                with open("test.txt",'a') as f:
                    f.write("{}Max action {} -- depth:{} -- bf:{}-{} -- result {}\n".format(tabs,action, depth, bfrem, bfthis, maxResult.map))
                    f.flush()
            value = max(value, self.minValue(maxResult, alfa, beta, depth + 1, max(bf, bfthis)))
            if value >= beta:
                if self.debug:
                    with open("test.txt",'a') as f:
                        f.write("{}prune Max -- depth:{} -- (alfa){} >= {}(beta)\n".format(tabs, depth, value, beta))
                        f.flush()
                return value
            alfa = max(alfa,value)
        
        #self.depth = self.depth - 1
        return value
    
    def minValue(self, grid, alfa, beta, depth, bf):
        #self.depth = self.depth + 1
        if self.terminalState(grid, depth, bf):
            return self.heuristic(grid, depth)
        
        value = float("inf")
        actions = self.minActions(grid)
        bfthis = len(actions)
        bfrem = 0
        tabs = "\t"*(depth -1)
        for action in self.minActions(grid):
            minResult = self.minResult(grid,action)
            if self.debug:
                bfrem = bfrem + 1  
                with open("test.txt",'a') as f:
                    f.write("{}Min action {} -- depth:{} -- bf:{}-{} -- result {}\n".format(tabs, action, depth, bfrem, bfthis, minResult.map))
                    f.flush()
            value = min(value, self.maxValue(minResult, alfa, beta, depth + 1, max(bf, bfthis)))
            if value <= alfa:
                if self.debug:
                    with open("test.txt",'a') as f:
                        f.write("{}prune Min -- depth:{} -- (beta){} <= {}(alfa)\n".format(tabs, depth, value, alfa))
                        f.flush()
                return value
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
        
        maxRank = max(max(posibles[2]), max(posibles[4]))
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
    
    def terminalState(self, grid, depth, bf):
        numAvblCells = len(grid.getAvailableCells())
        complexity = bf**(depth - 2)
        tabs = "\t" * (depth - 2)
        if numAvblCells > 4 and depth >= 4:
        #if complexity >= 50625:
            if self.debug:
                with open("test.txt",'a') as f:
                    f.write("{}depth {} -- bf {} -- complexity {}\n".format(tabs, depth-1, bf, complexity))
            return True
        if numAvblCells <= 4 and depth >= 6:
            #self.depth = self.depth - 1
            if self.debug:
                with open("test.txt",'a') as f:
                    f.write("{}depth {} -- bf {} -- complexity {}\n".format(tabs, depth-1, bf, complexity))
                    f.flush()
            return True
        #if grid.getMaxTile() == self.LIMIT:
        if len(grid.getAvailableMoves()) == 0:
        #if len(grid.getAvailableCells()) == 0 or len(grid.getAvailableMoves()) == 0:
            #print("Se llenan rama {} con profundidad {}".format(grid.map, self.depth))
            #self.depth = self.depth - 1
            #sys.exit()
            return True        
        #if self.heuristic(grid):
            #print("Se llega al destino {} con profundidad {}".format(grid.map, self.depth))
            #self.depth = self.depth - 1
            #if self.depth == 32:
            #    sys.exit()
            #return True
        return False
    
    def utility(self, grid):
        return grid.getMaxTile()
        
    def heuristic(self, grid, depth):
        avCells = len(grid.getAvailableCells())
        moves = len(grid.getAvailableMoves())
        #if avCells == 0 or moves == 0:
        #if moves == 0:
        #    return grid.getMaxTile()
        #else:
        #    avCells = math.log(avCells)
        #print("celdas: {} -- grid: {}".format(avCells, grid.map))
        maxValue = math.log(grid.getMaxTile(),2)
        #logAvg = self.average(grid)
        #scoreEdges = self.scoreEdges(grid)
        monotonocity = self.monotonic(grid)
        adjacents = self.adjacents(grid)
        hu = 3.0*avCells  +1.0*monotonocity + 2.0*maxValue + 0.7*adjacents #11.0*logAvg + 700.0*adjacents + 47.0*monotonocity 
        tabs = "\t" * (depth - 2)
        if self.debug:
            with open("test.txt",'a') as f:
                f.write("{}heuristica {} -- ({}) -- ({}) -- ({}) -- ({})\n".format(tabs, hu, avCells, monotonocity, maxValue, adjacents))
                f.flush()
        return hu

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
                    totals[2] = totals[2] + next - current
                elif next > current:
                    totals[3] = totals[3] + current - next
        

        return min(totals[0], totals[1]) + min(totals[2], totals[3])#max(totals[0], totals[1]) + max(totals[2], totals[3])

    
    def adjacents(self, grid):
        result = 0
        for row in grid.map:
            for i in range(len(row)):
                if row[i] != 0:
                    for j in range((i+1), len(row)):
                        if row[j] != 0:
                            result = result - abs(math.log(row[i],2) - math.log(row[j],2))

        trans = map(list, zip(*grid.map))
        for col in trans:
            for i in range(len(col)):
                if col[i] != 0:
                    for j in range((i+1), len(col)):
                        if col[j] != 0:
                            result = result - abs(math.log(col[i],2) - math.log(col[j],2))

        return result