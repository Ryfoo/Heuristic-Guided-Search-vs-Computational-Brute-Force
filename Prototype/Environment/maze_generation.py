import random
from collections import Counter
from collections import deque
import sys
from dataclasses import dataclass


@dataclass
class Dimensions:
    """
    Dimensions
    """

    width: int = 20
    height: int = 20
    start: tuple[int, int] = (0, 0)
    goal: tuple[int, int] = (19, 19)
    dx: int = 1
    dy: int = 1
    density: float = 0.35


class Environment:
    def __init__(
        self,
        width=Dimensions.width,
        height=Dimensions.height,
        start=Dimensions.start,
        goal=Dimensions.goal,
        dx=Dimensions.dx,
        dy=Dimensions.dy,
        density=Dimensions.density,
        terrain_weight_bool=False,
        debug=False
    ):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.dx = dx
        self.dy = dy
        self.density = density
        sys.setrecursionlimit(self.width * self.height + 100)
        self.grid = [
            [0 if random.random() < self.density else 1 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.grid[start[0]][start[1]] = 1
        self.grid[goal[0]][goal[1]] = 1
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

        print("start value:", self.grid[start[0]][start[1]])
        print("goal value:", self.grid[goal[0]][goal[1]])

        self._set_maze()

    def neighbors(self, x, y, obstacles=False):
        neighbors = []
        dirs = [(self.dx, 0), (-self.dx, 0),(0, self.dy),(0, -self.dy),]

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if obstacles:
                if(0 <= nx < self.width) and (0 <= ny < self.height):
                    neighbors.append((nx, ny))
            else:
                if(0 <= nx < self.width) and (0 <= ny < self.height) and self.grid[nx][ny] != 0:
                    neighbors.append((nx, ny))
                


        return neighbors

    def display(self, details=False):
        print("-" * 100 + "\n")
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) == self.start:
                    print("S", end=" ")
                elif (x, y) == self.goal:
                    print("G", end=" ")
                else:
                    if self.grid[x][y] != 0: 
                        if details:
                            print(self.grid[x][y], end=" ")
                        else:
                            print(" ", end=" ")
                    else:
                        print("*", end=" ")
            print()
        print("-" * 100 + "\n")

    def _carve(self, x=0, y=0):
        self.grid[x][y] = 1
        self.visited.add((x, y))
        if self.goal_test(x, y):
            return True

        neighbors = list(self.neighbors(x, y, True))
        random.shuffle(neighbors)

        for a, b in neighbors:
            if (a, b) not in self.visited:
                if self._carve(a, b):
                    return True

        return False
    
    def goal_test(self, x, y):
        return (x, y) == self.goal

    def is_connected(self):
        """Returns True if S and G are connected through open cells."""
        start = self.start
        goal = self.goal

        visited = set()
        queue = deque([start])

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                return True
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for a, b in self.neighbors(x, y):
                if self.grid[a][b] != 0 and (a, b) not in visited:
                    queue.append((a, b))

        return False

    def _set_maze(self):
        self._carve()
        if self.debug:
            gx, gy = self.goal

            for dx in [-1,0,1]:
                nx = gx + dx
                if 0 <= nx < self.width:
                    for dy in [-1,0,1]:
                        ny = gy + dy
                        if 0 <= ny < self.height:
                            print(self.grid[nx][ny], end=" ")
                    print()

        if self.terrain_weight_bool:
            keys = list(self.terrain_weights.keys())
            probs = list(self.terrain_weights.values())
            for x in range(self.width):
                for y in range(self.height):
                    if self.grid[x][y] == 1:
                        self.grid[x][y] = random.choices(keys, probs)[0]

        self.grid[self.start[0]][self.start[1]] = 1
        self.grid[self.goal[0]][self.goal[1]] = 1
        if self.debug:
            self.display()
            flat = [cell for row in self.grid for cell in row if cell > 0]
            print(Counter(flat))


env = Environment(1000, 1000, terrain_weight_bool=True, debug=True)




