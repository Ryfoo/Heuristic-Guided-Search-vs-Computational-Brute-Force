# main.py
from Prototype.Experiments.benchmark_runner import Benchmark
from Prototype.Experiments.parameters import DEFAULT_PARAMETERS
from Prototype.Uniformed_Algorithms.bfs import BFS
from Prototype.Uniformed_Algorithms.dfs import DFS
from Prototype.Informed_Algorithms.astar import ASTAR


if __name__ == "__main__":

    algorithms  = [BFS, DFS, ASTAR]

    benchmark = Benchmark(
        algorithms=algorithms,
        parameters=DEFAULT_PARAMETERS
    )

    benchmark.run()

