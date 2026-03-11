from dataclasses import dataclass
from typing import Union, List




# ── cell types ─────────────────────────────────────────────────────────────
Cell2D = tuple[int, int]
Cell3D = tuple[int, int, int]
Cell   = Union[Cell2D, Cell3D]

# ── test config ────────────────────────────────────────────────────────────
@dataclass
class Test:
    debug  : bool = True
    n_tests: int  = 100

# ── dimensions ─────────────────────────────────────────────────────────────
@dataclass
class Dimensions2D:
    width  : int   = 20
    height : int   = 20
    start  : Cell  = (0, 0)
    goal   : Cell  = (19, 19)
    dx     : int   = 1
    dy     : int   = 1
    density: float = 0.35

@dataclass
class Dimensions3D:
    width  : int   = 20
    height : int   = 20
    depth  : int   = 20
    start  : Cell  = (0, 0, 0)
    goal   : Cell  = (19, 19, 19)
    dx     : int   = 1
    dy     : int   = 1
    dz     : int   = 1
    density: float = 0.35
# ── Metrics ─────────────────────────────────────────────────────────────

@dataclass
class Metrics:
    algorithm: str
    maze_size: str
    density: float
    runtime: float
    cells_explored: int
    path_length: int
    cost : int
    max_memory_used : int
    seed : int
# ── ExperimentParameters ─────────────────────────────────────────────────────────────
@dataclass
class HeuristicParameters:
    weight : int = 1

@dataclass
class ExperimentParameters:
    maze_dimensions: Union[
        List[tuple[int, int, Cell2D, Cell2D]],
        List[tuple[int, int, int, Cell3D, Cell3D]]
    ]   
    densities: List[float]
    runs_per_configuration: int
    seed: int = 42
    three_d : bool = False

#───Default configuration────────────────────────────────────────

DEFAULT_PARAMETERS_2D = ExperimentParameters(
    maze_dimensions=[
        (10,  10,  (0, 0),   (9, 9)),     
        (20,  20,  (0, 0),   (19, 19)),   
        (50,  50,  (0, 0),   (49, 49)),
        (100, 100, (0, 0),   (99, 99)),
        (200,  200,  (0, 0),   (199, 199)),     
        (400,  400,  (0, 0),   (399, 399)),   
        (800,  800,  (0, 0),   (799, 799)),
        (1600, 1600, (0, 0),   (1599, 1599)),
        (3200, 3200, (0, 0),   (3199, 3199)),
        (5000, 5000, (0, 0),   (4999, 4999)),
    ],
    densities=[0.25, 0.35, 0.45],
    runs_per_configuration=10,
)
DEFAULT_PARAMETERS_3D = ExperimentParameters(
    maze_dimensions=[
        (10,  10, 10,  (0, 0, 0),   (9, 9, 9)),     
        (20,  20,  20, (0, 0, 0),   (19, 19, 19)),   
        (50,  50,  50, (0, 0, 0),   (49, 49, 49)),
        (100, 100, 100, (0, 0, 0),   (99, 99, 99)),
        # (200,  200,  200, (0, 0, 0),   (199, 199, 199)),     
        # (400,  400,  400, (0, 0, 0),   (399, 399, 399)),   
        # (800,  800,  800, (0, 0, 0),   (799, 799, 799)),
        # (1600, 1600, 1600, (0, 0, 0),   (1599, 1599, 1599)),
    ],
    densities=[0.5, 0.6, 0.7],
    runs_per_configuration=10,
)