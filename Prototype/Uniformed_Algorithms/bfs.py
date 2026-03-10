
from collections import deque
from typing import Union
from ..config import Cell
from ..Environment.maze_generation       import Environment2D
from ..Environment3D.maze_generation_3d  import Environment3D


Environment = Union[Environment2D, Environment3D]


class BFS:
    """
    Breadth-first search algorithm for 2D/3D maze
    """
    name = "BFS"

    def __init__(self, env : Environment, debug=False):
        self.start = env.start
        self.goal = env.goal

        self.env : Environment = env

        self.frontier : deque[Cell] = deque()

        self.frontier.append(env.start)

        self.visited : set[Cell] = set()

        self.visited.add(env.start)

        self.parents: dict[Cell, Cell] = {}

        self.path : list[Cell] = []

        self.cells_explored : int = 0

        self.cost : int = 0

        self.max_memory_used : int = 0

        self.debug = debug

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

    def _expand_cell(self, cell : Cell) -> list[Cell]:
        return self.env.neighbors(*cell)

    def _is_goal(self, cell : Cell) -> bool:
        return cell == self.goal

    def _add_to_frontier(self, cell : Cell) -> None:
        self.frontier.append(cell)
    
    def _pop_frontier(self) -> Cell:
        """
        Remove next node from frontier.
        """
        return self.frontier.popleft()

    def _frontier_empty(self) -> bool:
        
        return not self.frontier


    def _mark_visited(self, cell : Cell) -> None:
        self.visited.add(cell)

    def _is_visited(self, cell : Cell) -> bool:
        return cell in self.visited


    def _parent_map(self, child : Cell, parent : Cell) -> None:
        self.parents[child] = parent

    def _reconstruct_path(self) -> None:
        current = self.goal
        while current != self.start:
            self.path.append(current)
            current = self.parents[current]
        self.path.append(self.start)
        self.path.reverse()
        self.cost = sum(
                            self.env.terrain_cost(*cell) 
                            for cell in self.path
                        )

