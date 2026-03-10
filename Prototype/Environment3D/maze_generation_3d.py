import random
from collections import Counter
from collections import deque
import sys
from dataclasses import dataclass
from ..config import Cell3D, Dimensions3D, Test
# ── cell type ──────────────────────────────────────────────────────────────
# A cell is now (x, y, z) instead of (x, y)
# Neighbors: up, down, left, right, front, back → b ≤ 6


class Environment3D:
    """
    3D extension of Environment.
    Grid is width × height × depth.
    Algorithms are dimension-agnostic — only neighbors() changes.
    """

    def __init__(
        self,
        width=Dimensions3D.width,
        height=Dimensions3D.height,
        depth=Dimensions3D.height,
        start=Dimensions3D.start,
        goal=Dimensions3D.goal,
        dx=Dimensions3D.dx,
        dy=Dimensions3D.dy,
        dz=Dimensions3D.dz,
        density=Dimensions3D.density,
        terrain_weight_bool=False,
        debug=False
    ):
        self.width = width
        self.height = height
        self.depth = depth
        self.start = start
        self.goal = goal
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.density = density
        sys.setrecursionlimit(self.width * self.height * self.depth + 100)
        self.grid = [
            [
                [0 if random.random() < self.density else 1 for _ in range(self.depth)]
                for _ in range(self.height)
            ]
            for _ in range(self.width)
        ]
        self.grid[start[0]][start[1]][start[2]] = 1
        self.grid[goal[0]][goal[1]][goal[2]] = 1
        self.visited = set()
        self.terrain_weight_bool = terrain_weight_bool
        if self.terrain_weight_bool:
            self.terrain_weights = {
                1: 0.50,  # grass
                2: 0.20,   # sand
                4: 0.15,   # water
                8: 0.10,   # mud
                10: 0.05     # rocks
            }
        self.debug = debug

        print("start value:", self.grid[start[0]][start[1]][start[2]])
        print("goal value:", self.grid[goal[0]][goal[1]][goal[2]])

        self._set_maze()

    def neighbors(self, x, y,z, obstacles=False):
        """
        returns the adjacent cells for a specified cell (x,y,z)
        """
        neighbors = []
        dirs = [
            (self.dx, 0, 0), (-self.dx, 0, 0),
            (0, self.dy, 0),(0, -self.dy, 0),
            (0, 0, self.dz), (0, 0, -self.dz)
        ]

        for dx, dy, dz in dirs:
            nx, ny, nz = x + dx, y + dy, z + dz
            if obstacles:
                if(
                    (0 <= nx < self.width) and
                    (0 <= ny < self.height) and
                    (0 <= nz < self.depth)
                ):
                    neighbors.append((nx, ny, nz))
            else:
                if(
                    (0 <= nx < self.width) and 
                    (0 <= ny < self.height) and
                    (0 <= nz < self.depth) and
                    self.grid[nx][ny][nz] != 0
                ):
                    neighbors.append((nx, ny, nz))
                


        return neighbors

    def display_layer(self, z=0 , details=False):
        """
        the display_layer function is basic
        used for later debugging
        instead of 3D rendering
        display_layer each matrix (X * Y) at depth Z

        """
        print("-" * 100 + "\n")
        for x in range(self.width):
            for y in range(self.height):
                if (x, y, z) == self.start:
                    print("S", end=" ")
                elif (x, y, z) == self.goal:
                    print("G", end=" ")
                else:
                    if self.grid[x][y][z] != 0: 
                        if details:
                            print(self.grid[x][y][z], end=" ")
                        else:
                            print(" ", end=" ")
                    else:
                        print("*", end=" ")
            print()
        print("-" * 100 + "\n")

    def _carve(self, x=0, y=0, z=0):
        self.grid[x][y][z] = 1
        self.visited.add((x, y, z))
        if self.goal_test(x, y, z):
            return True

        neighbors = list(self.neighbors(x, y, z, True))
        random.shuffle(neighbors)

        for a, b, c in neighbors:
            if (a, b, c) not in self.visited:
                if self._carve(a, b, c):
                    return True

        return False
    def terrain_cost(self, x, y, z):
        """
        Returns the weight at each cell (x, y, z)
        """
        return self.grid[x][y][z]
    def goal_test(self, x, y, z):
        """
        checks whethere the cell (x, y,z) is a goal or no
        """
        return (x, y, z) == self.goal

    def is_connected(self):
        """Returns True if S and G are connected through open cells."""
        start = self.start
        goal = self.goal

        visited = set()
        queue = deque([start])

        while queue:
            x, y, z= queue.popleft()
            if (x, y, z) == goal:
                return True
            if (x, y, z) in visited:
                continue
            visited.add((x, y, z))
            for a, b, c in self.neighbors(x, y, z):
                if self.grid[a][b][c] != 0 and (a, b, c) not in visited:
                    queue.append((a, b, c))

        return False

    def _set_maze(self):
        self._carve()
        if self.debug:
            gx, gy, gz = self.goal

            for dx in [-1,0,1]:
                nx = gx + dx
                if 0 <= nx < self.width:
                    for dy in [-1,0,1]:
                        ny = gy + dy
                        if 0 <= ny < self.height:
                            for dz in [-1,0,1]:
                                nz = gz + dz
                                if 0 <= nz < self.depth:
                                    print(self.grid[nx][ny][nz], end=" ")
                            print()

        if self.terrain_weight_bool:
            keys = list(self.terrain_weights.keys())
            probs = list(self.terrain_weights.values())
            for x in range(self.width):
                for y in range(self.height):
                    for z in range(self.depth):
                        if self.grid[x][y][z] == 1:
                            self.grid[x][y][z] = random.choices(keys, probs)[0]

        self.grid[self.start[0]][self.start[1]][self.start[2]] = 1
        self.grid[self.goal[0]][self.goal[1]][self.goal[2]] = 1
        if self.debug:
            self.display_layer()
            flat = [
                cell
                for matrix in self.grid
                for row in matrix 
                for cell in row 
                if cell > 0
            ]
            print(Counter(flat))



