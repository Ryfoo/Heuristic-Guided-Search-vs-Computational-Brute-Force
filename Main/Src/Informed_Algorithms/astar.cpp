#include "../include/astar.hpp"

const std::string AStar::NAME = "AStar";

namespace Heuristics {
    double manhattan(Cell node, Cell goal) {
        // TODO
    }

    double euclidean(Cell node, Cell goal) {
        // TODO
    }

    double zero(Cell node, Cell goal) {
        // TODO
    }
}

SearchResult AStar::solve(
    const Maze&        maze,
    Heuristic          heuristic,
    const std::string& heuristic_name,
    double             weight)
{
    // TODO
}

std::vector<Cell> AStar::reconstruct_path(
    const std::vector<std::vector<Cell>>& parent,
    Cell start,
    Cell goal)
{
    // TODO
}
