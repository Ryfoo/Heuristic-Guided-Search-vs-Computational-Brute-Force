import json
import os
import statistics
from pathlib import Path
from datetime import datetime


MAX_EXPORT_DIM = 50   # skip export if any dimension exceeds this


class MazeExporter:
    """
    Collects all runs per config, picks the median runtime run,
    writes one JSON per config: WxHxD_3d.json
    """

    def __init__(
        self,
        output_dir: str = "visualization/public/data",
        max_dim:    int = MAX_EXPORT_DIM,
    ):
        self.output_dir  = Path(output_dir)
        self.max_dim     = max_dim
        self._runs: dict[str, list[dict]] = {}   # config_key → list of run dicts
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── called by benchmark after every single run ─────────────────────────
    def collect(
        self,
        env,
        results: dict[str, dict],
        seed:    int,
        density: float,
    ) -> None:
        is_3d  = hasattr(env, 'depth')
        width  = env.width
        height = env.height
        depth  = getattr(env, 'depth', 0)

        dims = [width, height] + ([depth] if is_3d else [])
        if any(d > self.max_dim for d in dims):
            return   # silently skip — too large to visualize

        config_key = self._config_key(width, height, depth)

        if config_key not in self._runs:
            self._runs[config_key] = []

        self._runs[config_key].append({
            "env":     env,
            "results": results,
            "seed":    seed,
            "density": density,
            "is_3d":   is_3d,
            # median selector key — average runtime across all algorithms
            "avg_runtime": statistics.mean(
                r.get("runtime", 0) for r in results.values() if r.get("found")
            ) if any(r.get("found") for r in results.values()) else float('inf'),
        })

    # ── called once after all runs for a config are done ──────────────────
    def flush(self, width: int, height: int, depth: int = 0) -> str | None:
        config_key = self._config_key(width, height, depth)
        runs = self._runs.get(config_key)
        if not runs:
            return None

        # pick median runtime run
        sorted_runs = sorted(runs, key=lambda r: r["avg_runtime"])
        median_idx  = len(sorted_runs) // 2
        best        = sorted_runs[median_idx]

        env     = best["env"]
        results = best["results"]
        is_3d   = best["is_3d"]

        data = {
            "meta": {
                "exported_at": datetime.now().isoformat(),
                "seed":        best["seed"],
                "density":     best["density"],
                "maze_size":   config_key,
                "total_runs":  len(runs),
                "selection":   "median runtime",
            },
            "maze": {
                "width":  env.width,
                "height": env.height,
                "depth":  getattr(env, 'depth', 0),
                "grid":   env.grid,
                "start":  list(env.start),
                "goal":   list(env.goal),
            },
            "algorithms": {
                name: self._serialize(result)
                for name, result in results.items()
                if result.get("found", False)
            },
        }

        filename = f"{config_key}_3d.json" if is_3d else f"{config_key}_2d.json"
        path     = self.output_dir / filename

        with open(path, "w") as f:
            json.dump(data, f, separators=(',', ':'))

        size_kb = os.path.getsize(path) / 1024
        print(f"  [exporter] {filename} ({size_kb:.1f} KB) — median of {len(runs)} runs")

        # clear collected runs for this config
        del self._runs[config_key]
        return str(path)

    # ── flush all remaining configs ────────────────────────────────────────
    def flush_all(self) -> list[str]:
        keys   = list(self._runs.keys())
        paths  = []
        for key in keys:
            parts = key.split('x')
            if len(parts) == 3:
                w, h, d = map(int, parts)
            else:
                w, h = map(int, parts); d = 0
            p = self.flush(w, h, d)
            if p: paths.append(p)
        return paths

    # ── helpers ────────────────────────────────────────────────────────────
    def _config_key(self, w, h, d=0) -> str:
        return f"{w}x{h}x{d}" if d else f"{w}x{h}"

    def _serialize(self, result: dict) -> dict:
        return {
            "visited_order":  [list(c) for c in result.get("visited_order", [])],
            "path":           [list(c) for c in result.get("path", [])],
            "path_length":    result.get("path_length",    0),
            "cost":           result.get("cost",           0),
            "nodes_expanded": result.get("cells_explored", 0),
            "runtime":        round(result.get("runtime",  0.0), 4),
        }