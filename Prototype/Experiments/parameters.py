
from dataclasses import dataclass
from typing import List

@dataclass
class ExperimentParameters:
    maze_dimensions: List[tuple[int, int, tuple[int, int], tuple[int, int]]]
    densities: List[float]
    runs_per_configuration: int
    seed: int = 42


# Default configuration
DEFAULT_PARAMETERS = ExperimentParameters(
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