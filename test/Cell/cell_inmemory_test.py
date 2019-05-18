import unittest
from module.Structure import CellInMemory


class TestCellInMemory(unittest.TestCase):
    """
    Basic test class for the in memory cell. Most cell classes will cohere to this basic implementation.
    Contains:

        - Accessibility access
        - Constructor validation
        - Getting the x_y list
    """

    def test_default_constructor_empty(self):
        cell = CellInMemory(0, 0)
        self.assertEqual(0, cell.f)
        self.assertEqual(0, cell.g)
        self.assertEqual(0, cell.h)

    def test_default_constructor_filled(self):
        cell = CellInMemory(0, 0, 1, 2, 3)
        self.assertEqual(1, cell.f)
        self.assertEqual(2, cell.g)
        self.assertEqual(3, cell.h)

    def test_get_x_y(self):
        cell = CellInMemory(0, 0)
        self.assertEqual([0, 0], cell.get_x_y())

    def test_get_accessible_default(self):
        cell = CellInMemory(0, 0)
        self.assertEqual(True, cell.accessible)

    def test_get_accessible_false(self):
        cell = CellInMemory(0, 0)
        cell.accessible = False
        self.assertEqual(False, cell.accessible)

    def test_get_accessible_accessed(self):
        cell = CellInMemory(0, 0)
        cell.accessible = True
        self.assertEqual(True, cell.accessible)

    def test_previous_cell_correct(self):
        cell = CellInMemory(0, 0)
        cell_previous = CellInMemory(0, 1)
        cell.set_previous(cell_previous)

        self.assertEqual(cell_previous, cell.previous)

    def test_previous_cell_duplicate(self):
        cell = CellInMemory(0, 0)
        cell_previous = CellInMemory(0, 0)
        cell.set_previous(cell_previous)

        self.assertEqual(None, cell.previous)


if __name__ == '__main__':
    unittest.main()
