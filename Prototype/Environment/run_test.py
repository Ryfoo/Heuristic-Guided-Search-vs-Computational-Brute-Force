# run_tests.py
import unittest
from test_maze import TestMaze  # import the test class you wrote

if __name__ == "__main__":
    suite = unittest.TestSuite()

    # Add tests manually
    suite.addTest(TestMaze("test_connected"))
    suite.addTest(TestMaze("test_connected_multiple_runs"))
    suite.addTest(TestMaze("test_start_and_goal_are_open"))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)