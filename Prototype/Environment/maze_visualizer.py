"""
visualizer.py
-------------
Simple static visualizer for the Environment maze grid.
Reads grid (0 = wall, 1 = walkable) and draws it with Pygame.

Usage:
    python visualizer.py
"""

import pygame
import sys
import random
from maze_generation import Environment

# ── Config ─────────────────────────────────────────────────────────────────────
CELL        = 24          # px per cell
WALL_COL    = (20, 24, 40)
PATH_COL    = (220, 225, 240)
START_COL   = (0, 200, 100)
GOAL_COL    = (220, 60, 60)
BG          = (12, 14, 24)
# ── Setup ──────────────────────────────────────────────────────────────────────

env  = Environment()
env.carve()

grid = env.grid        # 2D list: grid[x][y] or grid[row][col] — adjust below
cols = len(grid)
rows = len(grid[0])

WIN_W = cols * CELL
WIN_H = rows * CELL

pygame.init()
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Maze Visualizer")
clock = pygame.time.Clock()

# ── Draw ───────────────────────────────────────────────────────────────────────
def draw():
    screen.fill(BG)
    for x in range(cols):
        for y in range(rows):
            color = PATH_COL if grid[x][y] == 1 else WALL_COL
            pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

    # Start and goal markers — adjust coordinates to match your Environment
    sx, sy = env.start  # e.g. (0, 0)
    gx, gy = env.goal   # e.g. (cols-1, rows-1)

    pygame.draw.rect(screen, START_COL, (sx * CELL, sy * CELL, CELL, CELL))
    pygame.draw.rect(screen, GOAL_COL,  (gx * CELL, gy * CELL, CELL, CELL))

    font = pygame.font.SysFont("consolas", 14, bold=True)
    screen.blit(font.render("S", True, (0,0,0)), (sx * CELL + 6, sy * CELL + 4))
    screen.blit(font.render("G", True, (0,0,0)), (gx * CELL + 6, gy * CELL + 4))

    pygame.display.flip()

# ── Loop ───────────────────────────────────────────────────────────────────────
draw()  # draw once — static display

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.key == pygame.K_SPACE:
                # regenerate maze on SPACE
                env.carve()
                grid = env.grid
                draw()

    clock.tick(30)