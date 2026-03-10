#pragma once

#include <vector>
#include <utility>

using Cell = std::pair<int, int>;

class Maze {
public:
    int   width;
    int   height;
    Cell  start;
    Cell  goal;
    float density;
    int   seed;

    std::vector<std::vector<int>> grid;

    Maze(int width, int height, Cell start, Cell goal, float density, int seed);

    bool              in_bounds(int x, int y)  const;
    bool              is_free(int x, int y)    const;
    bool              is_wall(int x, int y)    const;
    std::vector<Cell> neighbors(int x, int y)  const;
    bool              is_connected()            const;
    void              display()                 const;

private:
    void generate();
    void carve(int x, int y);
};
