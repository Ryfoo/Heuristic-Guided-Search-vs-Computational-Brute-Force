import random
from .maze_generation_3d import Environment3D, Cell3D


class DatasetBuilder3D:
    """
    Generates batches of 3D mazes for benchmarking.
    Mirrors DatasetBuilder from 2D — same interface, 3D environment.
    """

    def __init__(
        self,
        sizes:    list[tuple[int, int, int]],   # (width, height, depth)
        densities: list[float],
        runs_per_config: int = 10,
    ):
        self.sizes           = sizes
        self.densities       = densities
        self.runs_per_config = runs_per_config

    def generate(self) -> list[dict]:
        """
        Returns a list of configs:
        {
            "env":     Environment3D instance,
            "seed":    int,
            "size":    (width, height, depth),
            "density": float,
        }
        """
        # TODO: loop over sizes × densities × runs
        # generate a random seed per run
        # instantiate Environment3D
        # collect and return configs
        pass