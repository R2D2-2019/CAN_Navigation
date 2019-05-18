import unittest
from module.Algorithms import AStar
from module.Structure import grid_factory


class TestCellInMemory(unittest.TestCase):

    def test_grid_access(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)
        start = g[(0, 0)]
        end = g[(cols - 1, rows - 1)]
        a_star = AStar(g, end, start)

        self.assertEqual(g, a_star.grid)

    def test_grid_start_access(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)
        start = g[(0, 0)]
        end = g[(cols - 1, rows - 1)]
        a_star = AStar(g, end, start)

        self.assertEqual(start, a_star.start)

    def test_grid_end_access(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)
        start = g[(0, 0)]
        end = g[(cols - 1, rows - 1)]
        a_star = AStar(g, end, start)

        self.assertEqual(end, a_star.end)

    def test_astar_pre_check(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)
        a_star = AStar(g)

        self.assertEqual(False, a_star.run_check())

    def test_astar_pre_check_single_condition(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)

        start = g[(0, 0)]
        a_star = AStar(g, start)

        self.assertEqual(False, a_star.run_check())

    def test_astar_pre_check_correct(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)

        start = g[(0, 0)]
        end = g[(cols - 1, rows - 1)]
        a_star = AStar(g, start, end)

        self.assertEqual(True, a_star.run_check())

    def test_astar_solve_pre_check_correct(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)

        start = g[(0, 0)]
        a_star = AStar(g, start)

        self.assertEqual(None, a_star.solve())

    def test_astar_empty_run(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)

        start = g[(0, 0)]
        end = g[(cols - 1, rows - 1)]
        a_star = AStar(g, start, end)

        expected_path = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

        self.assertEqual(expected_path, a_star.solve())

    def test_astar_filled_run(self):
        rows = 10
        cols = 10

        g = grid_factory(rows, cols)
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

        a_star = AStar(g, start, end)

        expected_path = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

        self.assertEqual(expected_path, a_star.solve())

    def test_astar_impossible_run(self):

        rows = 10
        cols = 10

        g = grid_factory(rows, cols)

        for x in range(rows - 1):
            for y in range(cols - 1):
                g[(x, y)].accessible = False

        start = g[(0, 0)]

        end = g[(cols - 9, rows - 1)]

        a_star = AStar(g, start, end)

        self.assertEqual(a_star.solve(), False)
