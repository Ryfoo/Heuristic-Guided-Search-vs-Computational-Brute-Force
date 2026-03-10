#pragma once

#include <functional>
#include <string>
#include "maze.hpp"
#include "search_result.hpp"

using Heuristic = std::function<double(Cell, Cell)>;

namespace Heuristics {
    double manhattan(Cell node, Cell goal);
    double euclidean(Cell node, Cell goal);
    double zero(Cell node, Cell goal);
}

class AStar {
public:
    static const std::string NAME;

    static SearchResult solve(
        const Maze&        maze,
        Heuristic          heuristic      = Heuristics::manhattan,
        const std::string& heuristic_name = "manhattan",
        double             weight         = 1.0
    );

private:
    static std::vector<Cell> reconstruct_path(
        const std::vector<std::vector<Cell>>& parent,
        Cell start,
        Cell goal
    );
};
