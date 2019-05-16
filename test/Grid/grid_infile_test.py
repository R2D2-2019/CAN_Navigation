import unittest
from module.Structure import GridInFile


class TestGridInFile(unittest.TestCase):
    """
    Our basic test class
    """

    def test_accessibility_GridInMemory(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """

        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        z = [[False, True, True, False, True, True, True, False, False, True],
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
                g[(x, y)].accessible = z[x][y]

        found = False
        for x in range(rows - 1):
            for y in range(cols - 1):
                if g[(x, y)].accessible is not z[x][y]:
                    found = True

        self.assertEqual(False, found)

    def test_accessibility_random_access_GridInMemory(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """

        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        z = [[False, True, True, False, True, True, True, False, False, True],
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
                g[(x, y)].accessible = z[x][y]

        self.assertEqual(g[(int(rows / 2), int(cols / 2))].accessible, z[int(rows / 2)][int(cols / 2)])

    def test_neighbour_zero_zero_GridInMemory(self):
        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        id = g[(0, 0)]
        neighbours = g.get_neighbours(id)

        ls = [[1, 0], [0, 1], [1, 1]]

        duplicates = False
        for neighbour in neighbours:
            if neighbour in ls:
                duplicates = True

        self.assertEqual(False, duplicates)

    def test_neighbour_limit_limit_GridInMemory(self):
        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        id = g[(9, 9)]
        neighbours = g.get_neighbours(id)

        ls = [[rows - 2, cols - 1], [rows - 1, cols - 1], [rows - 2, cols - 2]]

        duplicates = False
        for neighbour in neighbours:
            if neighbour in ls:
                duplicates = True

        self.assertEqual(False, duplicates)

    def test_neighbour_limit_bottom_GridInMemory(self):
        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        id = g[(9, 0)]
        neighbours = g.get_neighbours(id)

        ls = [[rows - 2, 0], [rows - 1, 1]]

        duplicates = False
        for neighbour in neighbours:
            if neighbour in ls:
                duplicates = True

        self.assertEqual(False, duplicates)

    # TODO: Dynamic allocation
    def test_neighbour_bottom_limit_GridInMemory(self):
        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        id = g[(int(rows / 2), int(cols / 2))]
        neighbours = g.get_neighbours(id)

        ls = [[6, 5],
              [4, 5],
              [5, 6],
              [5, 4],
              [4, 4],
              [6, 4],
              [4, 4],
              [6, 6]]

        duplicates = False
        for neighbour in neighbours:
            if neighbour in ls:
                duplicates = True

        self.assertEqual(False, duplicates)


if __name__ == '__main__':
    unittest.main()
