import unittest

from modules.CAN_Navigation.module.Grid import CellInFile
from modules.CAN_Navigation.module.FileStorage import FileStorage

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
        cell = CellInFile(FileStorage(), 190, 190)
        self.assertEqual(0, cell.f)
        self.assertEqual(0, cell.g)
        self.assertEqual(0, cell.h)
        cell.file_storage.delete_folder()

    def test_default_constructor_filled(self):
        """
        Testing if the default constructor filling does what is expected
        """
        cell = CellInFile(FileStorage(), 0, 0, 1, 2, 3)
        self.assertEqual(1, cell.f)
        self.assertEqual(2, cell.g)
        self.assertEqual(3, cell.h)
        cell.file_storage.delete_folder()

    def test_get_x_y(self):
        """
        Testing if the neighbour for the [limit][limit] index position is working as expected
        """
        cell = CellInFile(FileStorage(), 0, 0)
        self.assertEqual([0, 0], cell.get_x_y())

        cell.file_storage.delete_folder()

    def test_get_accessible_default(self):
        """
        Testing if the default value is as expected
        """
        cell = CellInFile(FileStorage(), 0, 0)
        self.assertEqual(True, cell.accessible)
        cell.file_storage.delete_folder()

    def test_get_accessible_false(self):
        """
        Testing if the accessible value has been updated accordingly (negative)
        """
        cell = CellInFile(FileStorage(), 0, 0)
        cell.accessible = False
        self.assertEqual(False, cell.accessible)
        cell.file_storage.delete_folder()

    def test_get_accessible_accessed(self):
        """
        MIGHT SEEM USELESS NOW, BUT WON'T BE IN THE FUTURE.
        Testing if the accessible value has been updated accordingly (positive)
        """
        cell = CellInFile(FileStorage(), 0, 0)
        cell.accessible = True
        self.assertEqual(True, cell.accessible)
        cell.file_storage.delete_folder()

    def test_previous_cell_correct(self):
        """
        Testing if the adding a correct cell is storing it in the previous variable of a cell
        """
        cell = CellInFile(FileStorage(), 0, 0)
        cell_previous = CellInFile(FileStorage(), 0, 1)
        cell.set_previous(cell_previous)
        self.assertEqual([[0, 1]], cell.get_previous())
        cell.file_storage.delete_folder()
        cell_previous.file_storage.delete_folder()

    def test_previous_cell_duplicate(self):
        """
        Testing if adding a duplicate to the previous value prevents it from being set
        """
        cell = CellInFile(FileStorage(), 0, 0)
        cell_previous = CellInFile(FileStorage(), 0, 0)
        cell.set_previous(cell_previous)

        self.assertEqual([], cell.previous)
        cell.file_storage.delete_folder()
        cell_previous.file_storage.delete_folder()

    def test_cell_storage(self):
        """
        Testing if the file contains the expected json string
        """
        cell = CellInFile(FileStorage(), 0, 0)
        expected_json = '{"file_name": "0_0.json", "f": 0, "g": 0, "h": 0, "x": 0, "y": 0, "neighbours": [], "previous": [], "accessible": true}'
        actual_json = ""
        with open(cell.file_storage.path(cell), 'r') as f:
            actual_json = f.readline()
        self.assertEqual(expected_json, actual_json)

        cell.file_storage.delete_folder()

    def test_cell_validating_read_data(self):
        """
        Testing if the addition of an existing field works as expected
        """

        fs = FileStorage()

        cell = CellInFile(fs, 0, 0)
        cell.neighbours = ["test"]
        cell.set_file_content()
        del cell
        cell_reopen = CellInFile(fs, 0, 0, read=True)

        self.assertEqual(["test"], cell_reopen.neighbours)
        fs.delete_folder()

    def test_cell_validating_new_read_data(self):
        """
        Testing if the addition of a unspecified (a.k.a a new cell) field works as expected
        """
        fs = FileStorage()
        cell = CellInFile(fs, 0, 0)
        cell.test_file = "test"
        cell.set_file_content()
        del cell
        cell_reopen = CellInFile(fs, 0, 0, read=True)

        self.assertEqual("test", cell_reopen.test_file)
        fs.delete_folder()


if __name__ == '__main__':
    unittest.main()
