# main.py
# main.py
import random
from Prototype import BFS, DFS, ASTAR, Greedy, Dijkstra,  Environment2D, Environment3D, Benchmark, ExperimentParameters, DEFAULT_PARAMETERS_3D, DEFAULT_PARAMETERS_2D

# ── environment factories ──────────────────────────────────────────────────

def env_factory_2d(config, density):
    width, height, start, goal = config
    return Environment2D(
        width=width, height=height,
        start=start, goal=goal,
        density=density,
        terrain_weight_bool=True,
    )

def env_factory_3d(config, density):
    width, height, depth, start, goal = config
    return Environment3D(
        width=width, height=height, depth=depth,
        start=start, goal=goal,
        density=density,
    )


# ── algorithms ─────────────────────────────────────────────────────────────

algorithms = [ASTAR, Dijkstra, Greedy]

# ── run ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = "3d"   # ← switch to "3d" to run 3D benchmark

    if mode == "2d":
        print("Running 2D benchmark")
        benchmark = Benchmark(
            algorithms  = algorithms,
            parameters  = DEFAULT_PARAMETERS_2D,
            env_factory = env_factory_2d,
        )
        benchmark.run()
    elif mode == "3d":
        print("Running 3D benchmark")
        benchmark = Benchmark(
            algorithms  = algorithms,
            parameters  = DEFAULT_PARAMETERS_3D,
            env_factory = env_factory_3d,
        )
        benchmark.run()

    

