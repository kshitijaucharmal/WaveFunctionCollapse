import pygame
from tile import Tile
import sys
sys.setrecursionlimit(10000)

WIDTH = 800
HEIGHT = 800
FPS = 60

DIM = 15

cell_size = WIDTH//DIM

pygame.init()
pygame.display.init()

ds = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

tile_images = {
    "BLANK" : pygame.image.load("sprites/full.png"),
    "UP"    : pygame.image.load("sprites/up.png"),
    "RIGHT" : pygame.image.load("sprites/right.png"),
    "DOWN"  : pygame.image.load("sprites/down.png"),
    "LEFT"  : pygame.image.load("sprites/left.png"),
}

grid = []

def draw_lines():
    # draw lines
    for i in range(DIM):
        pygame.draw.line(ds, (10, 200, 10), (0, i * cell_size), (WIDTH, i * cell_size), 4)
    for i in range(DIM):
        pygame.draw.line(ds, (10, 200, 10), (i * cell_size, 0), (i * cell_size, HEIGHT), 4)

def setup():
    ds.fill((35, 35, 35))

    # fill grid
    for i in range(DIM):
        grid.append(list())
        for j in range(DIM):
            # random tile for now
            grid[i].append(Tile(tile_images, cell_size, DIM))
            grid[i][j].set_pos((i,j))

    grid[0][0].collapse(grid)

    pass

def draw():
    ds.fill((11, 11, 11))
    # draw_lines()
    # draw grid
    for i in range(DIM):
        for j in range(DIM):
            grid[i][j].show(ds)
    pass

def main():
    run = True
    setup()
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                y = pos[1] // cell_size
                x = pos[0] // cell_size
                grid[x][y].collapse(grid)

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
