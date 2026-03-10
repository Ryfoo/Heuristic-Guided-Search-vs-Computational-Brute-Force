# metrics.py
import csv
import os
from pathlib import Path
from ..config import Metrics



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
                    "maze_size",
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
                metrics.maze_size,
                metrics.density,
                metrics.runtime,
                metrics.cells_explored,
                metrics.path_length,
                metrics.cost,
                metrics.max_memory_used, 
                metrics.seed
            ])
