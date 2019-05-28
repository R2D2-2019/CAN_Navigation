import unittest
from modules.CAN_Navigation.module.Grid import GridInMemory


class TestGridInMemory(unittest.TestCase):
    """
    Basic test class for the in memory grid. Most grid classes will cohere to this basic implementation.
    Contains:

        - Accessibility access
        - Edge cases for the neighbour gathering.
        - Default case for the neighbour gathering
    """

    def test_accessibility_GridInMemory(self):
        """ Testing if the accessibility setting is working accordingly on all memory fields """

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
                g[(x, y)].set_accessible(z[x][y])

        found = False
        for x in range(rows - 1):
            for y in range(cols - 1):
                if g[(x, y)].accessible is not z[x][y]:
                    found = True

        self.assertEqual(False, found)

    def test_accessibility_random_access_GridInMemory(self):
        """ Testing if the accessibility setting is working accordingly on a random location """

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
                g[(x, y)].set_accessible(z[x][y])

        self.assertEqual(g[(int(rows / 2), int(cols / 2))
                           ].accessible, z[int(rows / 2)][int(cols / 2)])

    def test_neighbour_zero_zero_GridInMemory(self):
        """ Testing if the neighbour for the [0][0] index position is working as expected """
        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        uid = g[(0, 0)]
        neighbours = g.get_neighbours(uid)

        ls = [[1, 0], [0, 1], [1, 1]]

        duplicates = False
        for neighbour in neighbours:
            if neighbour in ls:
                duplicates = True

        self.assertEqual(False, duplicates)

    def test_neighbour_limit_limit_GridInMemory(self):
        """
            Testing if the neighbour for the [limit][limit] index position is working as expected
        """
        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        uid = g[(9, 9)]
        neighbours = g.get_neighbours(uid)

        ls = [[rows - 2, cols - 1], [rows - 1, cols - 1], [rows - 2, cols - 2]]

        duplicates = False
        for neighbour in neighbours:
            if neighbour in ls:
                duplicates = True

        self.assertEqual(False, duplicates)

    def test_neighbour_limit_bottom_GridInMemory(self):
        """ Testing if the neighbour for the [limit][0] index position is working as expected """

        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        uid = g[(9, 0)]
        neighbours = g.get_neighbours(uid)

        ls = [[rows - 2, 0], [rows - 1, 1]]

        duplicates = False
        for neighbour in neighbours:
            if neighbour in ls:
                duplicates = True

        self.assertEqual(False, duplicates)

    # TODO: Dynamic allocation

    def test_neighbour_bottom_limit_GridInMemory(self):
        """ Testing if the neighbour for the [0][limit] index position is working as expected """
        rows = 10
        cols = 10

        g = GridInMemory(rows, cols)

        uid = g[(int(rows / 2), int(cols / 2))]
        neighbours = g.get_neighbours(uid)

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
