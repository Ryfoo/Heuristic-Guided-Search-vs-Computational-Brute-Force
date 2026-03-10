#include <cuda_runtime.h>
#include <device_launch_parameters.h>

// ── BFS kernel ─────────────────────────────────────────────────────────────
// One thread per frontier node.
// Expands neighbors and appends unvisited ones to next frontier atomically.

__global__ void bfs_kernel(
    const int* grid,
    int*       visited,
    const int* frontier,
    int        frontier_size,
    int*       next_frontier,
    int*       next_size,
    int        goal_id,
    int*       found_flag,
    int        height,
    int        width)
{
    // TODO
}

// ── host-side parallel BFS ─────────────────────────────────────────────────

struct ParallelBFSResult {
    bool path_found;
    int  nodes_expanded;
    int  levels;
    int  max_frontier_size;
};

ParallelBFSResult parallel_bfs(
    const int* host_grid,
    int height, int width,
    int start_x, int start_y,
    int goal_x,  int goal_y)
{
    // TODO: allocate device memory
    // TODO: initialize visited, frontier
    // TODO: level loop — launch bfs_kernel per level
    // TODO: check found_flag after each level
    // TODO: reconstruct path from visited array
    // TODO: free device memory

    ParallelBFSResult result = {};
    return result;
}

int main() {
    // TODO: build a test maze
    // TODO: call parallel_bfs
    // TODO: print result
    return 0;
}
