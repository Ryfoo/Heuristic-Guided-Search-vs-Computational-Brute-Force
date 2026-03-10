
import heapq
from ..Environment.maze_generation import Environment

class ASTAR:
    """
    A* search algorithm for 2D maze
    """
    name = "ASTAR"

    def __init__(self, env : Environment, debug=False):
        self.start = env.start
        self.goal = env.goal

        self.env : Environment = env

        self.frontier: list[tuple[int, tuple[int, int]]] = []

        heapq.heappush(self.frontier, (0, self.start))

        self.visited : set[tuple[int, int]] = set()
        
        self.g_costs : dict[tuple[int, int], int] = {}

        self.g_costs[self.start] = 0

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
            _, current = self._pop_frontier()
            if self._is_visited(current):
                continue
            self._mark_visited(current)
            self.cells_explored += 1
            if self._is_goal(current):
                found = True
                break
            
            for neighbor in self._expand_cell(current):
                tentative_g = self._cost_function(current, neighbor)
                if neighbor not in self.g_costs or tentative_g < self.g_costs[neighbor]:
                    self.g_costs[neighbor] = tentative_g
                    self._add_to_frontier(tentative_g, neighbor)
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

    def _cost_function(self, previous : tuple[int, int], current : tuple[int, int]) -> int:
        return self.g_costs[previous] + self.env.grid[current[0]][current[1]]

    def _manhattan_distance(self, cell : tuple[int, int]) -> int:
        dx = abs(cell[0] - self.goal[0])
        dy = abs(cell[1] - self.goal[1])
        min_cost = min(self.env.terrain_weights.keys())
        return (dx + dy) * min_cost

    def _f_value(self,g_value : int, cell : tuple[int, int]) -> int:
        return  g_value + self._manhatten_distance(cell)

    def _expand_cell(self, cell : tuple[int, int]) -> list[tuple[int, int]]:
        return self.env.neighbors(*cell)

    def _is_goal(self, cell : tuple[int, int]):
        return cell == self.goal

    def _add_to_frontier(self, g_value : int, cell : tuple[int, int]) -> None:
        heapq.heappush(self.frontier, (self._f_value(g_value, cell), cell))
    
    def _pop_frontier(self) -> tuple[int, tuple[int, int]]:
        return heapq.heappop(self.frontier)
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

