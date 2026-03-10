
from collections import deque
from ..Environment.maze_generation import Environment

class BFS:
    """
    Breadth-first search algorithm for 2D maze
    """
    name = "BFS"

    def __init__(self, env : Environment, debug=False):
        self.start = env.start
        self.goal = env.goal

        self.env : Environment = env

        self.frontier : deque[tuple[int, int]] = deque()

        self.frontier.append(env.start)

        self.visited : set[tuple[int, int]] = set()

        self.visited.add(env.start)

        self.parents: dict[tuple[int, int], tuple[int, int]] = {}

        self.path : list[tuple[int, int]] = []

        self.cells_explored : int = 0

        self.cost : int = 0

        self.max_memory_used : int = 0

    def solve(self) -> dict:
        """
        this the BFS solving function, it takes a maze of type Environment as a parameter
        then returns a dictionary with metrics ()
        """
        found = False

        summary : dict = {}

        while not self._frontier_empty():
            self.max_memory_used = max(self.max_memory_used, len(self.frontier))
            current = self._pop_frontier()
            self.cells_explored += 1
            if self._is_goal(current):
                found = True
                break
    
            for neighbor in self._expand_cell(current):
                if not self._is_visited(neighbor):
                    self._mark_visited(neighbor)
                    self._add_to_frontier(neighbor)
                    self._parent_map(neighbor, current)
        summary['found'] = found
        
        if found:
            self._reconstruct_path()
            summary['cells_explored'] = self.cells_explored
            summary['path_length'] = len(self.path)
            summary['path'] = self.path
            summary['cost'] = self.cost
            summary['max_memory_used'] = self.max_memory_used
        
        return summary

    def _expand_cell(self, cell : tuple[int, int]) -> list[tuple[int, int]]:
        return self.env.neighbors(*cell)

    def _is_goal(self, cell : tuple[int, int]):
        return cell == self.goal

    def _add_to_frontier(self, cell : tuple[int, int]) -> None:
        self.frontier.append(cell)
    
    def _pop_frontier(self) -> tuple[int, int]:
        """
        Remove next node from frontier.
        """
        return self.frontier.popleft()

    def _frontier_empty(self) -> bool:
        
        return not self.frontier


    def _mark_visited(self, cell : tuple[int, int]) -> None:
        self.visited.add(cell)

    def _is_visited(self, cell : tuple[int, int]) -> bool:
        return cell in self.visited


    def _parent_map(self, child : tuple[int, int], parent : tuple[int, int]) -> None:
        self.parents[child] = parent

    def _reconstruct_path(self) -> None:
        current = self.goal
        while current != self.start:
            self.path.append(current)
            current = self.parents[current]
        self.path.append(self.start)
        self.path.reverse()
        self.cost = sum(self.env.grid[x][y] for x,y in self.path)

