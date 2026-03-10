cmake_minimum_required(VERSION 3.18)
project(MazeSearchBenchmark LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

set(COMMON_SOURCES
    src/maze.cpp
    src/bfs.cpp
    src/dijkstra.cpp
    src/astar.cpp
    src/search_result.cpp
)

add_executable(benchmark
    ${COMMON_SOURCES}
    src/benchmark.cpp
)

find_package(CUDA)
if(CUDA_FOUND OR CMAKE_CUDA_COMPILER)
    add_executable(parallel_bfs
        cuda/parallel_bfs.cu
    )
    message(STATUS "CUDA found — parallel_bfs target enabled")
else()
    message(WARNING "CUDA not found — parallel_bfs target skipped")
endif()
