from random import randint
from BaseAI import BaseAI
from collections import deque
import math
import sys

class PlayerAI(BaseAI):

    def getMove(self, grid):
        return self.alfaBeta(grid)
        
    def alfaBeta(self, grid):
        moves = grid.getAvailableMoves()

        alfa = float("-inf")
        maxValue = float("-inf")
        betterMove = moves[0]
        for move in moves:
            maxResult = self.maxResult(grid, move)
            val = self.minValue(maxResult,alfa, float("inf"), 2, len(moves))
            alfa = max(alfa,val)
            if val > maxValue:
                maxValue = val
                betterMove = move
        return betterMove   
    
    def maxValue(self, grid, alfa, beta, depth, bf):

        if self.terminalState(grid, depth, bf):
            return self.heuristic(grid, depth)
        
        value = float("-inf")
        actions = self.maxActions(grid)
        bfthis = len(actions)
        for action in actions:
            maxResult = self.maxResult(grid,action)
            value = max(value, self.minValue(maxResult, alfa, beta, depth + 1, max(bf, bfthis)))
            if value >= beta:
                return value
            alfa = max(alfa,value)
        
        return value
    
    def minValue(self, grid, alfa, beta, depth, bf):
        #if self.terminalState(grid, depth, bf):
        #    return self.heuristic(grid, depth)
        value = float("inf")
        actions = self.minActions(grid)
        bfthis = len(actions)
        for action in self.minActions(grid):
            minResult = self.minResult(grid,action)
            value = min(value, self.maxValue(minResult, alfa, beta, depth + 1, max(bf, bfthis)))
            if value <= alfa:
                return value
            beta = min(beta, value)
        
        return value
    
    def maxActions(self, grid):
        return grid.getAvailableMoves()
    
    def minActionsNew(self, grid):
        actions = []
        cells = grid.getAvailableCells()
        posibles = [2, 4]
        for posible in posibles:
            for cell in cells:
                actions.append(tuple([cell, posible]))
        
        return actions
    
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
        for posible in posibles.iterkeys():
            for i, rank in enumerate(posibles[posible]):
                if rank == maxRank:
                    actions.append(tuple([cells[i],posible]))
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
        if numAvblCells > 12 and depth >=2:
            return True
        if numAvblCells > 2 and depth >=4:
            return True
        if depth >= 6:
        #if numAvblCells > 3 and depth >= 6:
            return True
        #if numAvblCells <= 3 and depth >= 6:
        #    return True

        if len(grid.getAvailableMoves()) == 0:
            return True        
        return False
            
    def utility(self, grid):
        return grid.getMaxTile()
        
    def heuristic(self, grid, depth):
        avCells = len(grid.getAvailableCells())
        moves = len(grid.getAvailableMoves())
        #if moves == 0:
        #    return math.log(grid.getMaxTile(),2)
        w0 = 100
        w1 = 8
        w2 = 0
        w3 = 1
        w4 = 0
        w5 = 0
        maxValue = math.log(grid.getMaxTile(),2)
        if maxValue >= 21:
            w0 = 100
            w1 = 75 #math.log(maxValue, 2)
            w2 = 80 #* self.monotonicNew(grid)
            w3 = 0
                
        logAvg = self.average(grid)
        scoreEdges = self.scoreEdges(grid)
        monotonocity = self.monotonic(grid)
        adjacents = self.adjacents(grid)
        #hu = 3.0*avCells  - 100.0*monotonocity + 7.0*adjacents #1.0*maxValue + 11.0*logAvg + 700.0*adjacents + 47.0*monotonocity 
        hu = w0*avCells  + w1*scoreEdges + w2* monotonocity + w3*logAvg + w4*maxValue + w5*adjacents
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
        sumCorners = grid.map[0][0] + grid.map[0][3] + grid.map[3][0] + grid.map[3][3]
        sumEdges = grid.map[0][1] + grid.map[0][2] + grid.map[1][0] + grid.map[2][0] \
            + grid.map[1][3] + grid.map[2][3] + grid.map[3][1] + grid.map[3][2]
        sumCenter = grid.map[1][1] + grid.map[1][2] + grid.map[2][1] + grid.map[2][2] 
        
        if sumCorners > 0:
            sumCorners = math.log(sumCorners * 2,2)
        if sumEdges > 0:
            sumEdges = math.log(sumEdges,2)
        if sumCenter > 0:
            sumCenter = math.log(sumCenter, 2)
    
        return sumCorners + sumEdges - sumCenter
        
    def scoreEdgesOld(self, grid):
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
    
    def monotonicNew (self, grid):
        result = 0
        for row in grid.map:
            monleft = 0
            monright = 0
            for i in range(len(row)-1):
                if row[i] > row[i+1]:
                    if row[i+1] > 0:
                        monleft = monleft + math.log(row[i], 2) - math.log(row[i+1], 2)
                    else:
                        monleft = monleft + math.log(row[i], 2)
                elif row[i+1] > row[i]:
                    if row[i] > 0:
                        monleft = monleft + math.log(row[i+1], 2) - math.log(row[i], 2)
                    else:
                        monright = monright + math.log(row[i+1], 2)
                    
            result = result + min(monleft, monright)
                    
        trans = map(list, zip(*grid.map))
        for col in trans:
            monleft = 0
            monright = 0
            for j in range(len(col)-1):
                if col[j] > col[j+1]:
                    if col[j+1] > 0:
                        monleft = monleft + math.log(col[j], 2) - math.log(col[j+1], 2)
                    else:
                        monleft = monleft + math.log(col[j], 2)
                elif col[j+1] > col[j]:
                    if col[j] > 0:
                        monleft = monleft + math.log(col[j+1], 2) - math.log(col[j], 2)
                    else:
                        monright = monright + math.log(col[j+1], 2)
                    
            result = result + min(monleft, monright)
        
        return result
        
                    
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
        

        return min(totals[0], totals[1]) + min(totals[2], totals[3]) #min(totals[0], totals[1]) + min(totals[2], totals[3])

    
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
    
    def adjacentsNew(self, grid):
        result = 0
        for row in grid.map:
            merges = 0
            prev = 0
            count = 0
            for i in range(len(row)):
                score = row[i]
                if score != 0:
                    if prev == score:
                        count = count + 1
                    elif count > 0:
                        merges = merges + 1 + count
                    prev = score
            
            if count > 0:
                merges = merges + 1 + count
            result = result + merges    
                
        trans = map(list, zip(*grid.map))
        for col in trans:
            merges = 0
            prev = 0
            count = 0
            for j in range(len(col)):
                score = col[i]
                if score != 0:
                    if prev == score:
                        count = count + 1
                    elif count > 0:
                        merges = merges + 1 + count
                    prev = score
            
            if count > 0:
                merges = merges + 1 + count
            result = result + merges    
    
        return result    