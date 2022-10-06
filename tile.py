import pygame
from random import choice, randint
import time

edge_info = {
    "BLANK" : [0, 0, 0, 0],
    "UP"    : [1, 1, 0, 1],
    "RIGHT" : [1, 1, 1, 0],
    "DOWN"  : [0, 1, 1, 1],
    "LEFT"  : [1, 0, 1, 1],
}

class Tile:
    def __init__(self, imgs, cell_size, DIM):
        self.imgs = imgs
        self.cell_size = cell_size
        self.DIM = DIM

        self.values = ["BLANK", "UP", "RIGHT", "DOWN", "LEFT"]
        self.value = choice(self.values) # random choice
        self.entropy = len(self.values)
        self.collapsed = False
        pass

    def set_pos(self, pos):
        self.pos = pos

    def show(self, ds):
        if self.entropy == 1:
            img = pygame.transform.scale(self.imgs[self.value], (self.cell_size, self.cell_size))
            ds.blit(img, (self.pos[0] * self.cell_size, self.pos[1] * self.cell_size))
        else:
            # draw all Possible tiles in a small grid
            size = self.cell_size/3
            for i in range(len(self.values)):
                img = pygame.transform.scale(self.imgs[self.values[i]], (size, size))
                xoffset = i
                yoffset = 0
                if xoffset >= 3:
                    xoffset -= 3
                    yoffset = 1
                pos = (self.pos[0] * self.cell_size + xoffset * size, self.pos[1] * self.cell_size + yoffset * size) 
                ds.blit(img, pos)
            pass
        pass

    def fix_tile(self, d):
        self.value = d
        self.values = [d]
        self.entropy = 1
        self.edges = edge_info[d]
        pass

    def collapse(self, grid, tile=None):
        if self.collapsed:
            return

        if not tile:
            tile = choice(self.values)
        if not self.pos:
            print("Please call this after calling set_pos")
            return

        self.fix_tile(tile)
        self.collapsed = True

        # get neighbors
        i = self.pos[0]
        j = self.pos[1]

        up = None
        right = None
        down = None
        left = None

        if j != 0:
            up      = grid[i][j - 1]
            self.set_new_values(up, 0)
        if i != self.DIM - 1:
            right   = grid[i + 1][j]
            self.set_new_values(right, 1)
        if j != self.DIM - 1:
            down    = grid[i][j + 1]
            self.set_new_values(down, 2)
        if i != 0:
            left    = grid[i - 1][j]
            self.set_new_values(left, 3)

        # recursion
        if up:
            up.collapse(grid)
        if right:
            right.collapse(grid)
        if down:
            down.collapse(grid)
        if left:
            left.collapse(grid)

        pass

    def set_new_values(self, dir, fr):
        if dir.entropy != 1:
            dir.values = self.calculate_new_values(dir, fr)
            dir.set_entropy()
        pass

    def set_entropy(self):
        self.entropy = len(self.values)
        if self.entropy == 1:
            self.value = self.values[0]

    def set_to(self, fr):
        if fr == 0:
            to = 2
        elif fr == 2:
            to = 0
        elif fr == 1:
            to = 3
        elif fr == 3:
            to = 1
        else:
            print("Not GOod from");
            to = -1
        return to

    def calculate_new_values(self, dir, fr):
        to = self.set_to(fr)
        new_vals = []
        for v in dir.values:
            if edge_info[v][to] == self.edges[fr]:
                new_vals.append(v)
        return new_vals
