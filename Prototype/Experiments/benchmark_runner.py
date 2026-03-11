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


# This shows the changes needed in benchmark.py
# The key changes:
# 1. Accept exporter in __init__
# 2. Call exporter.collect() after each run
# 3. Call exporter.flush() after all runs for a config complete

import time
import random
from .metrics import MetricsLogger
from ..config import ExperimentParameters, Metrics
from .exporter import MazeExporter


class Benchmark:

    def __init__(self, algorithms, parameters: ExperimentParameters,
                 env_factory, exporter: MazeExporter | None = None):
        self.algorithms  = algorithms
        self.parameters  = parameters
        self.env_factory = env_factory
        self.logger      = MetricsLogger()
        self.exporter    = exporter   # None when running 2D

    def run(self):
        for config in self.parameters.maze_dimensions:
            for density in self.parameters.densities:

                # ── all runs for this config ───────────────────────────────
                for _ in range(self.parameters.runs_per_configuration):
                    seed = random.randint(0, 1_000_000)
                    env, gen_runtime = self._build_environment(config, density)
                    run_results      = self._run_algorithms(env, config, density, seed)

                    # collect this run for median selection
                    if self.exporter:
                        self.exporter.collect(env, run_results, seed, density)

                # ── flush best run for this config to JSON ─────────────────
                if self.exporter:
                    self._flush_config(config)

    def _flush_config(self, config):
        if len(config) == 5:          # 3D: (w, h, d, start, goal)
            w, h, d = config[0], config[1], config[2]
            self.exporter.flush(w, h, d)
        else:                          # 2D: (w, h, start, goal)
            w, h = config[0], config[1]
            self.exporter.flush(w, h)

    def _build_environment(self, config, density):
        start = time.perf_counter()
        env   = self.env_factory(config, density)
        runtime = time.perf_counter() - start
        print(f"maze {config} | density={density} | generated in {runtime:.3f}s")
        return env, runtime

    def _run_algorithms(self, env, config, density, seed):
        run_results = {}
        for algorithm in self.algorithms:
            solver  = algorithm(env)
            start   = time.perf_counter()
            result  = solver.solve()
            runtime = time.perf_counter() - start
            result["runtime"] = runtime

            print(f"  {solver.name:<12} "
                  f"cells={result.get('cells_explored',0):<8} "
                  f"path={result.get('path_length',0):<6} "
                  f"time={runtime:.3f}s")

            run_results[solver.name.lower()] = result

            self.logger.log(Metrics(
                algorithm      = solver.name,
                maze_size      = config[0],
                density        = density,
                runtime        = runtime,
                cells_explored = result.get("cells_explored", 0),
                path_length    = result.get("path_length",    0),
                cost           = result.get("cost",           0),
                max_memory_used= result.get("max_memory_used",0),
                seed           = seed,
            ))

        return run_results