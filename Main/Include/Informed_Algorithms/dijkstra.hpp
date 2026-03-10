#pragma once

#include "maze.hpp"
#include "search_result.hpp"

class Dijkstra {
public:
    static const std::string NAME;

    static SearchResult solve(const Maze& maze);

private:
    static std::vector<Cell> reconstruct_path(
        const std::vector<std::vector<Cell>>& parent,
        Cell start,
        Cell goal
    );
};
