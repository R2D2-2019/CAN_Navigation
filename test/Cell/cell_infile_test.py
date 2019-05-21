import unittest
from module.Structure import CellInFile


class TestCellInFile(unittest.TestCase):
    """
    Basic test class for the in memory cell. Most cell classes will cohere to this basic implementation.
    Contains:

        - Accessibility access
        - Constructor validation
        - Getting the x_y list
    """

    def test_default_constructor_empty(self):
        """
        Testing if default constructor works with the default parameters
        """
        cell = CellInFile(190, 190)
        self.assertEqual(0, cell.f)
        self.assertEqual(0, cell.g)
        self.assertEqual(0, cell.h)

    def test_default_constructor_filled(self):
        """
        Testing if the default constructor filling does what is expected
        """
        cell = CellInFile(0, 0, 1, 2, 3)
        self.assertEqual(1, cell.f)
        self.assertEqual(2, cell.g)
        self.assertEqual(3, cell.h)

    def test_get_x_y(self):
        """
        Testing if the neighbour for the [limit][limit] index position is working as expected
        """
        cell = CellInFile(0, 0)
        self.assertEqual([0, 0], cell.get_x_y())

    def test_get_accessible_default(self):
        """
        Testing if the default value is as expected
        """
        cell = CellInFile(0, 0)
        self.assertEqual(True, cell.accessible)

    def test_get_accessible_false(self):
        """
        Testing if the accessible value has been updated accordingly (negative)
        """
        cell = CellInFile(0, 0)
        cell.accessible = False
        self.assertEqual(False, cell.accessible)

    def test_get_accessible_accessed(self):
        """
        MIGHT SEEM USELESS NOW, BUT WON'T BE IN THE FUTURE.
        Testing if the accessible value has been updated accordingly (positive)
        """
        cell = CellInFile(0, 0)
        cell.accessible = True
        self.assertEqual(True, cell.accessible)

    def test_previous_cell_correct(self):
        """
        Testing if the adding a correct cell is storing it in the previous variable of a cell
        """
        cell = CellInFile(0, 0)
        cell_previous = CellInFile(0, 1)
        cell.set_previous(cell_previous)

        self.assertEqual(cell_previous.get_x_y(), cell.previous)

    def test_previous_cell_duplicate(self):
        """
        Testing if adding a duplicate to the previous value prevents it from being set
        """
        cell = CellInFile(0, 0)
        cell_previous = CellInFile(0, 0)
        cell.set_previous(cell_previous)

        self.assertEqual(None, cell.previous)

    def test_cell_storage(self):
        """
        Testing if the file contains the expected json string
        """
        cell = CellInFile(0, 0)
        expected_json = '{"file_name": "0_0.json", "f": 0, "g": 0, "h": 0, "x": 0, "y": 0, "neighbours": [], "previous": null, "accessible": true}'
        actual_json = ""
        with open(cell.file_name, 'r') as f:
            actual_json = f.readline()
        self.assertEqual(expected_json, actual_json)

    def test_cell_validating_read_data(self):
        """
        Testing if the addition of an existing field works as expected
        """
        cell = CellInFile(0, 0)
        cell.neighbours = ["test"]
        cell.set_file_content()
        del cell
        cell_reopen = CellInFile(0, 0, read=True)

        self.assertEqual(["test"], cell_reopen.neighbours)

    def test_cell_validating_new_read_data(self):
        """
        Testing if the addition of a unspecified (a.k.a a new cell) field works as expected
        """
        cell = CellInFile(0, 0)
        cell.test_file = "test"
        cell.set_file_content()
        del cell
        cell_reopen = CellInFile(0, 0, read=True)

        self.assertEqual("test", cell_reopen.test_file)


if __name__ == '__main__':
    unittest.main()
