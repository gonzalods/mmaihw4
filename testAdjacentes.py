from Grid       import Grid
from PlayerAITest   import PlayerAI

def main():
    playerAI  = PlayerAI()
    grid = Grid()
    grid.map = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 2, 0, 0]] #[[2, 0, 0, 2], [0, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0]]
    print playerAI.adjacents(grid)
    print playerAI.monotonic(grid)


if __name__ == '__main__':
    main()