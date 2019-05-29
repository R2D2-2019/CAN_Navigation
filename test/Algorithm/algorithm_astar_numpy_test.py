import unittest
from modules.CAN_Navigation.module.Algorithms import AstarNumpy
from modules.CAN_Navigation.module.Grid import GridInNumpy


class TestAlgorithmAstarNumpy(unittest.TestCase):

    def test_grid_access(self):
        """ Testing if the grid is stored accordingly """
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)
        start = g.array[0, 0]
        end = g[cols - 1, rows - 1]
        a_star = AstarNumpy(g, start, end)
        self.assertEqual(g.array.any(), a_star.grid.array.any())

    def test_grid_start_access(self):
        """ Testing if the astar start location is stored accordingly """
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)
        start = g.array[0, 0]
        end = g[cols - 1, rows - 1]
        a_star = AstarNumpy(g, start, end)

        self.assertEqual(start, a_star.start)

    def test_grid_end_access(self):
        """ Testing if the astar end location is stored accordingly """
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)
        start = g.array[0, 0]
        end = g[cols - 1, rows - 1]
        a_star = AstarNumpy(g, start, end)

        self.assertEqual(end, a_star.end)

    def test_astar_run_check(self):
        """ Checking the false positive for the run_check"""
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)
        a_star = AstarNumpy(g)

        self.assertEqual(False, a_star.run_check())

    def test_astar_run_check_single_condition(self):
        """ Checking the false positive if we are the start location"""
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)

        start = g[(0, 0)]
        a_star = AstarNumpy(g, start)

        self.assertEqual(False, a_star.run_check())

    def test_astar_run_check_correct(self):
        """ Checking the positive if we have supplied all for the algorithm to run"""
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)

        start = g[(0, 0)]
        end = g[(cols - 1, rows - 1)]
        a_star = AstarNumpy(g, start, end)

        self.assertEqual(True, a_star.run_check())

    def test_astar_solve_run_check_correct(self):
        """ Checking the run_check instance of the solve for None variable preventing A* run"""

        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)

        start = g[(0, 0)]
        a_star = AstarNumpy(g, start)

        self.assertEqual(None, a_star.solve())

    def test_astar_empty_run(self):
        """ Testing if the ath through a grid without obstacles is working accordingly"""
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)

        start = g[(0, 0)]
        end = g[(cols - 1, rows - 1)]
        a_star = AstarNumpy(g, start, end)

        expected_path = [
            [
                0, 0], [
                1, 1], [
                2, 2], [
                3, 3], [
                4, 4], [
                5, 5], [
                6, 6], [
                7, 7], [
                8, 8], [
                9, 9]]

        self.assertEqual(expected_path, a_star.solve())

    def test_astar_filled_run(self):
        """ Checking if the run in a filled grid is working accordingly"""
        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)
        occupancy = [[False, True, True, False, True, True, True, False, False, True],
                     [True, False, True, True, True, False, True, True, False, True],
                     [True, False, True, False, True, True, True, False, False, True],
                     [False, False, True, True, False, True, True, True, True, True],
                     [False, True, False, True, True, True, False, True, True, True],
                     [False, True, True, False, True, True, True, True, True, True],
                     [True, True, False, True, True, False, True, True, False, True],
                     [False, True, True, True, True, True, False, True, True, True],
                     [False, True, False, False, True, False, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True]]

        for x in range(rows - 1):
            for y in range(cols - 1):
                g[(x, y)].accessible = occupancy[x][y]

        start = g[(0, 0)]

        end = g[(cols - 9, rows - 1)]

        a_star = AstarNumpy(g, start, end)

        expected_path = [
            [
                0, 0], [
                1, 1], [
                2, 2], [
                3, 3], [
                4, 4], [
                5, 5], [
                6, 6], [
                7, 7], [
                8, 8], [
                9, 9]]

        self.assertEqual(expected_path, a_star.solve())

    def test_astar_impossible_run(self):
        """ Checking if the run in a full grid is stopping accordingly"""

        rows = 10
        cols = 10

        g = GridInNumpy(rows, cols)

        for x in range(rows - 1):
            for y in range(cols - 1):
                g[(x, y)].accessible = False

        start = g[(0, 0)]

        end = g[(cols - 9, rows - 1)]

        a_star = AstarNumpy(g, start, end)

        self.assertEqual(a_star.solve(), False)
