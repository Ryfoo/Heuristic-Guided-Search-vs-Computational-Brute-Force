import json
import os
from pathlib import Path
from datetime import datetime


# ── export threshold ───────────────────────────────────────────────────────
MAX_EXPORT_DIM = 50   # skip export if any dimension exceeds this


class MazeExporter:
    """
    Exports a single benchmark run to JSON for the Three.js visualizer.
    Triggered after each full run in benchmark.py.

    JSON schema:
    {
        "meta": {
            "exported_at": str,
            "seed":        int,
            "density":     float,
            "maze_size":   str,
        },
        "maze": {
            "width":  int,
            "height": int,
            "depth":  int,       # 0 if 2D
            "grid":   list,      # [x][y] or [x][y][z], 0=wall else terrain weight
            "start":  list,      # [x, y] or [x, y, z]
            "goal":   list,
        },
        "algorithms": {
            "<name>": {
                "path":           list[list[int]],
                "path_length":    int,
                "cost":           int,
                "nodes_expanded": int,
                "runtime":        float,
            }
        }
    }
    """

    def __init__(
        self,
        output_dir: str = "visualization/public/data",
        max_dim:    int = MAX_EXPORT_DIM,
    ):
        self.output_dir = Path(output_dir)
        self.max_dim    = max_dim
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        env,
        results:  dict[str, dict],
        seed:     int,
        density:  float,
    ) -> str | None:
        """
        Export one run to JSON.

        Parameters
        ----------
        env     : Environment2D or Environment3D instance
        results : { algorithm_name: result_dict from solver.solve() }
        seed    : seed used for this run
        density : density used for this run

        Returns
        -------
        str  — path to written file
        None — if maze exceeds size threshold (skipped silently)
        """
        is_3d  = hasattr(env, 'depth')
        width  = env.width
        height = env.height
        depth  = getattr(env, 'depth', 0)

        # ── size gate ──────────────────────────────────────────────────────
        dims = [width, height] + ([depth] if is_3d else [])
        if any(d > self.max_dim for d in dims):
            print(f"  [exporter] skipped — maze {dims} exceeds threshold {self.max_dim}")
            return None

        # ── build payload ──────────────────────────────────────────────────
        data = {
            "meta": {
                "exported_at": datetime.now().isoformat(),
                "seed":        seed,
                "density":     density,
                "maze_size":   f"{width}x{height}" + (f"x{depth}" if is_3d else ""),
            },
            "maze": {
                "width":  width,
                "height": height,
                "depth":  depth,
                "grid":   env.grid,
                "start":  list(env.start),
                "goal":   list(env.goal),
            },
            "algorithms": {
                name: self._serialize_result(result)
                for name, result in results.items()
                if result.get("found", False)
            }
        }

        # ── write file ─────────────────────────────────────────────────────
        filename = (
            f"maze_{'3d' if is_3d else '2d'}"
            f"_{width}x{height}" + (f"x{depth}" if is_3d else "")
            + ".json"
        )
        path = self.output_dir / filename

        with open(path, "w") as f:
            json.dump(data, f, separators=(',', ':'))   # compact — no whitespace

        # also write a fixed-name file for the live visualizer
        with open(latest_path, "w") as f:
            json.dump(data, f, separators=(',', ':'))

        size_kb = os.path.getsize(path) / 1024
        print(f"  [exporter] wrote {filename} ({size_kb:.1f} KB)")
        return str(path)

    def _serialize_result(self, result: dict) -> dict:
        return {
            "path":           [list(cell) for cell in result.get("path", [])],
            "path_length":    result.get("path_length", 0),
            "cost":           result.get("cost", 0),
            "nodes_expanded": result.get("cells_explored", 0),
            "runtime":        round(result.get("runtime", 0.0), 4),
        }