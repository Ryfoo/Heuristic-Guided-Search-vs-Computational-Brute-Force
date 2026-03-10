# benchmark.py

import time
import random

from ..Environment.maze_generation import Environment
from .metrics import Metrics, MetricsLogger
from .parameters import ExperimentParameters


class Benchmark:
    """
    Benchmark
    """
    def __init__(self, algorithms, parameters: ExperimentParameters):

        self.algorithms = algorithms
        self.parameters = parameters
        self.logger = MetricsLogger()

    def run(self):
        """
        runner
        """
        for width, height, start, goal in self.parameters.maze_dimensions:

            for density in self.parameters.densities:

                for _ in range(self.parameters.runs_per_configuration):

                    seed = random.randint(0, 1_000_000)
                    gen_start_time = time.perf_counter()
                    env = Environment(width=width,height=height, start=start,  goal=goal, density=density, terrain_weight_bool=True)
                    gen_end_time = time.perf_counter()
                    gen_runtime = gen_end_time - gen_start_time
                    print(f"maze {width}x{height} generated in {gen_runtime:.3f}s")
                    for algorithm in self.algorithms:

                        solver = algorithm(env)

                        start_time = time.perf_counter()

                        result = solver.solve()

                        end_time = time.perf_counter()
                        
                        runtime = end_time - start_time
                        print(f"{algorithm.name} solved in {runtime:.3f}s")
                        metrics = Metrics(
                            algorithm=solver.name,
                            maze_width=width,
                            maze_height=height,
                            density=density,
                            runtime=runtime,
                            cells_explored=result["cells_explored"],
                            path_length=result["path_length"],
                            cost=result["cost"],
                            max_memory_used=result["max_memory_used"],
                            seed=seed
                        )

                        self.logger.log(metrics)