#pragma once

#include <vector>
#include <string>
#include "maze.hpp"

struct SearchResult {
    std::string       algorithm;
    bool              path_found;
    std::vector<Cell> path;
    int               path_length;
    int               nodes_expanded;
    double            time_ms;
    std::vector<int>  frontier_over_time;
    int               max_frontier_size;
    double            parallel_efficiency;
};

void print_result(const SearchResult& result);
