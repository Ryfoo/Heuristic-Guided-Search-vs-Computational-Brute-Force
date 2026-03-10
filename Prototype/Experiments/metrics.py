# metrics.py

from dataclasses import dataclass
import csv
import os
from pathlib import Path


@dataclass
class Metrics:
    algorithm: str
    maze_width: int
    maze_height: int
    density: float
    runtime: float
    cells_explored: int
    path_length: int
    cost : int
    max_memory_used : int
    seed : int

BASE_DIR = Path(__file__).parent.parent.parent

output_dir = BASE_DIR / "Data" / "benchmark_results"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "results.csv"


class MetricsLogger:

    def __init__(self, filename=output_file):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "algorithm",
                    "maze_width",
                    "maze_height",
                    "density",
                    "runtime",
                    "cells_explored",
                    "path_length",
                    "cost",
                    "max_memory_used",
                    "seed"
                ])

    def log(self, metrics: Metrics):

        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow([
                metrics.algorithm,
                metrics.maze_width,
                metrics.maze_height,
                metrics.density,
                metrics.runtime,
                metrics.cells_explored,
                metrics.path_length,
                metrics.cost,
                metrics.max_memory_used, 
                metrics.seed
            ])
