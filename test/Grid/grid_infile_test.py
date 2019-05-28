import unittest, time
from module.Structure import GridInFile


class TestGridInFile(unittest.TestCase):
    """
    Basic test class for the in file grid. Most grid classes will cohere to this basic implementation.
    Contains:

        - Accessibility access
        - Edge cases for the neighbour gathering.
        - Default case for the neighbour gathering
    """

    def test_accessibility_GridInFile(self):
        """ Testing if the accessibility setting is working accordingly on all file fields """

        rows = 10
        cols = 10

        g = GridInFile(rows, cols)

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
        g.file_storage.delete_folder()

    def test_accessibility_random_access_GridInFile(self):
        """ Testing if the accessibility setting is working accordingly on a random location """

        rows = 10
        cols = 10

        g = GridInFile(rows, cols)

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

        self.assertEqual(g[(int(rows / 2), int(cols / 2))
                         ].accessible, z[int(rows / 2)][int(cols / 2)])
        g.file_storage.delete_folder()

    def test_neighbour_zero_zero_GridInFile(self):
        """ Testing if the neighbour for the [0][0] index position is working as expected """
        rows = 10
        cols = 10

        g = GridInFile(rows, cols)

        uid = g[(0, 0)]

        ls = [[1, 0], [0, 1], [1, 1]]

        validation = list()
        for neighbour in g.get_neighbours(uid):
            validation.append(neighbour.get_x_y())

        self.assertEqual(ls, validation)
        g.file_storage.delete_folder()

    def test_neighbour_limit_limit_GridInFile(self):
        """
            Testing if the neighbour for the [limit][limit] index position is working as expected
        """
        rows = 10
        cols = 10

        g = GridInFile(rows, cols)

        uid = g[(9, 9)]

        ls = [[rows - 2, cols - 1], [rows - 1, cols - 2], [rows - 2, cols - 2]]

        self.assertEqual(g.get_neighbours(uid), ls)
        g.file_storage.delete_folder()

    def test_neighbour_limit_bottom_GridInFile(self):
        """ Testing if the neighbour for the [limit][0] index position is working as expected """

        rows = 10
        cols = 10

        g = GridInFile(rows, cols)

        uid = g[(9, 0)]

        ls = [[rows - 2, 0], [rows - 1, 1]]

        self.assertEqual(g.get_neighbours(uid), ls)
        g.file_storage.delete_folder()

    def test_neighbour_bottom_limit_GridInFile(self):
        """ Testing if the neighbour for the [0][limit] index position is working as expected """
        rows = 10
        cols = 10

        g = GridInFile(rows, cols)

        uid = g[(int(rows / 2), int(cols / 2))]

        ls = [[6, 5],
              [4, 5],
              [5, 6],
              [5, 4],
              [4, 4],
              [6, 4],
              [4, 4],
              [6, 6]]

        self.assertEqual(g.get_neighbours(uid), ls)
        g.file_storage.delete_folder()

    def test_hash(self):
        """ Testing if our hash method works as expected,
        hashing can be made far more difficult so this will serve as a template.
        """
        rows = 10
        cols = 10

        g = GridInFile(rows, cols)

        file_name = "grid.json"

        self.assertEqual(file_name, g.file_name)
        g.file_storage.delete_folder()


if __name__ == '__main__':
    unittest.main()
