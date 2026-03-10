
import heapq
from typing import Union
from ..config import Cell
from ..Environment.maze_generation       import Environment2D
from ..Environment3D.maze_generation_3d  import Environment3D


Environment = Union[Environment2D, Environment3D]
class Greedy:
    """
    GREEDY search algorithm for 2D/3D maze
    """
    name = "Greedy"

    def __init__(self, env : Environment, debug=False, heuristic="manhattan"):
        self.start = env.start
        self.goal = env.goal

        self.env : Environment = env

        self.frontier: list[tuple[int, Cell]] = []

        heapq.heappush(self.frontier, (0, self.start))

        self.visited : set[Cell] = set()
        
        self.h_costs : dict[Cell, int] = {}

        self.h_costs[self.start] = 0

        self.parents: dict[Cell, Cell] = {}

        self.path : list[Cell] = []

        self.cells_explored : int = 0

        self.cost : int = 0

        self.max_memory_used : int = 0

        self.debug = debug

        self.heuristic = heuristic
    def solve(self) -> dict:
        """
        this the BFS solving function, it takes a maze of type Environment as a parameter
        then returns a dictionary with metrics ()
        """
        found = False

        summary : dict = {}

        while not self._frontier_empty():
            self.max_memory_used = max(self.max_memory_used, len(self.frontier))
            _, current = self._pop_frontier()
            if self._is_visited(current):
                continue
            self._mark_visited(current)
            
            if self._is_goal(current):
                found = True
                break
            self.cells_explored += 1
            for neighbor in self._expand_cell(current):
                if self.heuristic == "Euclidean":
                    h_value = self._manhattan_distance(current)
                else:
                    h_value = self._euclidean_distance(current)
                if neighbor not in self.h_costs:
                    self.h_costs[neighbor] = h_value
                    self._add_to_frontier(h_value, neighbor)
                    if self.debug :
                        print(f'''
                            at stage : {self.cells_explored}
                            Manhattan distance : {self._manhattan_distance(neighbor)}
                            Euclidean distance : {self._euclidean_distance(neighbor)}
                            h-cost : {h_value}
                        ''')
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

    def _manhattan_distance(self, cell : Cell, weight : int = 1) -> int:
        return sum(abs(a - b) for a, b in zip(cell, self.goal)) * weight
    def _euclidean_distance(self, cell : Cell, weight : int = 1) -> int:
        return (sum((a - b)**2 for a, b in zip(cell, self.goal))**0.5) * weight
    def _expand_cell(self, cell : Cell) -> list[Cell]:
        return self.env.neighbors(*cell)

    def _is_goal(self, cell : Cell):
        return cell == self.goal

    def _add_to_frontier(self, h_value : int, cell : Cell) -> None:
        heapq.heappush(self.frontier, (h_value , cell))
    
    def _pop_frontier(self) -> tuple[int, Cell]:
        return heapq.heappop(self.frontier)
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
                            self.env.terrain_cost(*cell) for cell in self.path
                        )

