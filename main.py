import os
import sys
import threading
import webbrowser
import http.server
import socketserver
from pathlib import Path

from Prototype import (
    BFS, DFS, ASTAR, Greedy, Dijkstra,
    Environment2D, Environment3D,
    Benchmark,
    ExperimentParameters,
    DEFAULT_PARAMETERS_2D,
    DEFAULT_PARAMETERS_3D,
)
from Prototype.Experiments.exporter import MazeExporter

# ── config ─────────────────────────────────────────────────────────────────
PORT     = 8000
VIS_DIR  = Path(__file__).parent / "visualization"
DATA_DIR = VIS_DIR / "public" / "data"

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

# ── HTTP server ────────────────────────────────────────────────────────────
def launch_server():
    """Start a silent HTTP server serving visualization/ on port 8000."""

    class SilentHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass   # suppress all request logs

    os.chdir(VIS_DIR)
    with socketserver.TCPServer(("", PORT), SilentHandler) as httpd:
        httpd.serve_forever()

def launch_visualization():
    """Start server in background thread, open browser immediately."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    server_thread = threading.Thread(target=launch_server, daemon=True)
    server_thread.start()

    url = f"http://localhost:{PORT}/index.html"
    print(f"\n  [visualizer] serving at {url}")
    print(f"  [visualizer] JSON files land in visualization/public/data/")
    print(f"  [visualizer] press Ctrl+C to stop\n")

    webbrowser.open(url)

# ── algorithms ─────────────────────────────────────────────────────────────
algorithms = [BFS, DFS, ASTAR, Dijkstra, Greedy]

# ── run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mode = "3d"

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

        exporter = MazeExporter(
            output_dir = str(DATA_DIR),
            max_dim    = 50,
        )
        launch_visualization()

        benchmark = Benchmark(
            algorithms  = algorithms,
            parameters  = DEFAULT_PARAMETERS_3D,
            env_factory = env_factory_3d,
            exporter    = exporter
        )

        try:
            benchmark.run()
            print("\n  [benchmark] complete — browser still open at "
                  f"http://localhost:{PORT}/index.html")
            print("  [visualizer] press Ctrl+C to stop server\n")
            threading.Event().wait()

        except KeyboardInterrupt:
            print("\n  [visualizer] shutting down")
            sys.exit(0)