import unittest
from maze_generation import Environment
import random

class TestMaze(unittest.TestCase):

    def test_connected(self):
        maze = Environment(width=30, height=30, goal=(29,29))
        self.assertTrue(maze.is_connected(), "S and G must be connected after carving")

    def test_connected_multiple_runs(self):
        """Stress test — carve is random, so test many seeds"""
        for seed in range(100):
            random.seed(seed)
            maze = Environment(width=30, height=30, goal=(29,29))
            self.assertTrue(maze.is_connected(), f"Failed on seed {seed}")

    def test_start_and_goal_are_open(self):
        maze = Environment(width=30, height=30, goal=(29,29))
        sx, sy = maze.start
        gx, gy = maze.goal
        self.assertEqual(maze.grid[sx][sy], 1, "Start must be open")
        self.assertEqual(maze.grid[gx][gy], 1, "Goal must be open")