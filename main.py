import pygame, random, sys
from time import sleep
pygame.init()
pygame.font.init()

screenX = 1000
screenY = 1000
cellSize = 4
cellColorAlive = (0,0,0)
cellColorDead  = (255,255,255)
pygame.display.set_caption('Game of life')
screen = pygame.display.set_mode([screenX, screenY])

cells = [
    [random.randint(0, 2) for _ in range(int(screenX/cellSize))]
    for _ in range(int(screenY/cellSize))
]


def drawCell(x, y, isEmpty = False):
    if screenX > x * cellSize >= 0 and screenY > y * cellSize >= 0:
        if isEmpty:
            pygame.draw.rect(screen, cellColorDead, (x * cellSize, y * cellSize, cellSize, cellSize), 0)
        else:
            pygame.draw.rect(screen, cellColorAlive, (x * cellSize, y * cellSize, cellSize, cellSize), 0)


def clear():
    screen.fill((255, 255, 255))

def canMakeLife(x, y):
    global cells
    totalAlifeAround = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            try:
                if cells[i][j] != 0 and (i != x or j != y):
                    totalAlifeAround = totalAlifeAround + 1
            except IndexError:
                pass


    if cells[x][y] == 0:
        if totalAlifeAround == 3:
            return True
        else:
            return False
    else:
        if totalAlifeAround == 3 or totalAlifeAround == 2:
            return True
        else:
            return False


drawingEvent = False

running = True
iterations = 0
while running:
    iterations = iterations + 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if drawingEvent:
                pos = pygame.mouse.get_pos()
                cellX, cellY = pos
                cellX = int(cellX/cellSize)
                cellY = int(cellY/cellSize)
                cells[cellX][cellY] = 1
                cells[cellX - 1][cellY - 1] = 1
                cells[cellX - 1][cellY + 1] = 1
                cells[cellX - 1][cellY + 2] = 1
                cells[cellX + 1][cellY + 2] = 1
                print('drawing')

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawingEvent = True
            print('trigger down')
        if event.type == pygame.MOUSEBUTTONUP:
            drawingEvent = False
            print('trigger up')

    clear()
    nextCells = [
        [0 for _ in range(int(screenX / cellSize))]
        for _ in range(int(screenY / cellSize))
    ]

    #random
    # for i in range(len(nextCells)):
    #     for j in range(len(nextCells[i])):
    #         rnd = random.randint(0, 10)
    #         if rnd == 1:
    #             cells[i][j] = 1

    #rules
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if canMakeLife(i, j):
                nextCells[i][j] = 1
            else:
                nextCells[i][j] = 0

    #draw cells
    for i in range(len(nextCells)):
        for j in range(len(nextCells[i])):
            if nextCells[i][j] != 0:
                drawCell(i, j)
            else:
                drawCell(i, j, True)

    cells = nextCells
    #if iterations == 1:
    pygame.display.flip()
    sleep(0.01)


    # if iterations < -1:
    #     s = [[str(e) for e in row] for row in cells]
    #     lens = [max(map(len, col)) for col in zip(*s)]
    #     fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    #     table = [fmt.format(*row) for row in s]
    #     print('\n'.join(table))
    #     print('------------')

pygame.quit()