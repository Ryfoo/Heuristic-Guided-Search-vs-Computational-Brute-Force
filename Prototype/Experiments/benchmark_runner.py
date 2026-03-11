import time
import random
from typing import Union
from typing import Callable
from .metrics import MetricsLogger
from ..config import ExperimentParameters, Metrics
from ..Environment.maze_generation       import Environment2D
from ..Environment3D.maze_generation_3d  import Environment3D
from .exporter import MazeExporter

Environment = Union[Environment2D, Environment3D]


class Benchmark:
    """
    Dimension-agnostic benchmark runner.
    Accepts any environment factory and any set of algorithms.
    """

    def __init__(
        self,
        algorithms:   list,
        parameters:   ExperimentParameters,
        env_factory:  Callable,
    ):
        self.algorithms  = algorithms
        self.parameters  = parameters
        self.env_factory = env_factory
        self.logger      = MetricsLogger()
        self.exporter    = MazeExporter(
            output_dir="visualization/public/data",
            max_dim=200,
        )

    def run(self) -> None:
        for config in self.parameters.maze_dimensions:
            for density in self.parameters.densities:
                for _ in range(self.parameters.runs_per_configuration):
                    seed = random.randint(0, 1_000_000)
                    env, gen_runtime = self._build_environment(config, density, seed)
                    self._run_algorithms(env, config, density, seed, gen_runtime)

    def _build_environment(
        self,
        config:  tuple,
        density: float,
        seed:    int,
    ) -> tuple[Environment, float]:
        start = time.perf_counter()
        env   = self.env_factory(config, density)
        runtime = time.perf_counter() - start
        print(f"maze {config} | density={density} | generated in {runtime:.3f}s")
        return env, runtime

    def _run_algorithms(
        self,
        env:         Environment,
        config:      tuple,
        density:     float,
        seed:        int,
        gen_runtime: float,
    ) -> None:
        run_results = {}
        for algorithm in self.algorithms:
            solver  = algorithm(env)
            start   = time.perf_counter()
            result  = solver.solve()
            runtime = time.perf_counter() - start
            result["runtime"] = runtime

            print(f"  {solver.name:<12} "
                  f"cells={result['cells_explored']:<8} "
                  f"path={result['path_length']:<6} "
                  f"time={runtime:.3f}s")
            run_results[solver.name.lower()] = result
            self.logger.log(Metrics(
                algorithm      = solver.name,
                maze_size      = str(config),
                density        = density,
                runtime        = runtime,
                cells_explored = result["cells_explored"],
                path_length    = result["path_length"],
                cost           = result["cost"],
                max_memory_used= result["max_memory_used"],
                seed=seed
            ))


            self.exporter.export(
                        env     = env,
                        results = run_results,
                        seed    = seed,
                        density = density,
                    )