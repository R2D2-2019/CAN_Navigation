from modules.CAN_Navigation.module.Cell import CellInMemory, CellInFile
import time
import json
import numpy as np
from itertools import product


def cell_factory(x, y, f=0, g=0, h=0):
    # Default allocation for the memory grid is inMemory cell
    # However it should be possible to use a different cell type
    # The reason why is unclear at this time.
    return CellInMemory(x, y, f, g, h)


class Grid:

    def __init__(self, columns=0, rows=0):
        self.columns = columns
        self.rows = rows

    def get_neighbours(self, cell):
        pass

    def get_neighbours_indexes(self, cell):
        pass

    def __getitem__(self, lst):
        pass

    def __setitem__(self, lst, value):
        pass

    def __str__(self):
        pass


class GridInMemory(Grid):

    def __init__(
            self,
            columns=0,
            rows=0,
            cell=None,
    ):

        # Initialise the super

        Grid.__init__(self, columns, rows)

        # Scaling the grid to contain all all the cells.
        # Cells are still empty at this time, merely allocation.
        self.grid = [[cell_factory(j, i) for i in range(self.columns)] for j in
                     range(self.rows)]

    def get_neighbours_indexes(self, cell):
        """
        Returns the indexes of the neighbours of a cell in a list

        """
        # Checking if there's a cached version
        if cell.neighbours:
            return cell.neighbours

        #  Building up a new cache.

        if cell.x < self.rows - 1:
            cell.neighbours.append([cell.x + 1, cell.y])
        if cell.x > 0:
            cell.neighbours.append([cell.x - 1, cell.y])
        if cell.y < self.columns - 1:
            cell.neighbours.append([cell.x, cell.y + 1])
        if cell.y > 0:
            cell.neighbours.append([cell.x, cell.y - 1])
        if cell.x > 0 and cell.y > 0:
            cell.neighbours.append([cell.x - 1, cell.y - 1])
        if cell.x < self.rows - 1 and cell.y > 0 and cell.x:
            cell.neighbours.append([cell.x + 1, cell.y - 1])
        if cell.x > 0 and cell.y < self.columns - 1 and cell.y:
            cell.neighbours.append([cell.x - 1, cell.y - 1])
        if cell.x < self.rows - 1 and cell.y < self.columns - 1:
            cell.neighbours.append([cell.x + 1, cell.y + 1])
        return cell.neighbours

    # Based on the neighbour indexes, acquiring the cell objects

    def get_neighbours(self, cell):
        neighbour_index = self.get_neighbours_indexes(cell)
        neighbours = list()
        for index in neighbour_index:
            neighbours.append(self.grid[index[0]][index[1]])
        return neighbours

    def __getitem__(self, lst):
        (x, y) = lst
        return self.grid[x][y]

    def __setitem__(self, lst, value):
        (x, y) = lst
        self.grid[x][y].f = value

    def __str__(self):
        """Returns printable version of the grid"""
        text = ''
        for column in range(self.columns):
            for row in range(self.rows):
                text += str(self.grid[column][row].f)
            text += '\n'
        return text


class GridInNumpy(Grid):
    """The entire numpy grid should be"""

    def __init__(self, columns, rows):
        Grid.__init__(self, columns, rows)

        # Numpy has a function that allows us to set the default value (zero) and make a NumPy array out of it.
        self.array = np.zeros((columns, rows), dtype=int)

    def __setitem__(self, lst, value):
        """Allowing cases to be set"""
        (x, y) = lst
        self.array[x][y].f = value

    def get_neighbours(self, cell):
        """Numpy way of returning the expected structure"""

        """Side note, numpy will catch this if impossible, we don't have to worry about it.
        We can simply use all the possible outcomes, we don't need to catch it using a series of if statements.
        I've initially done these values in a loop, but it's a waste of doing so considering they're static.
        """
        possible_neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Initialising our soon-to-be return type.
        neighbours = list()

        # Appending the possibilities based on the cell index to return the possible neighbours.
        for x, y in possible_neighbours:
            neighbours.append((cell[0] + x, cell[1] + y))
        return neighbours


class GridInFile(GridInMemory):

    def __init__(self, columns=0, rows=0):
        # The InFile will create it's own file structure on a hard drive (in the module folder)
        # In Order to prevent collisions we'll be using the epoch time and the grid size to hash a path
        # While these will prevent MOSTLY prevent collisions, they aren't
        # immune to it.
        GridInMemory.__init__(self, columns, rows)
        self.grid = list()

        self.epoch_time = int(time.time())
        self.file_name = None

        self.directory_name = "Cell/"
        import os
        if not os.path.exists(self.directory_name):
            os.mkdir(self.directory_name)
        self.hash_path()
        self.initialize_grid()

    def hash_path(self):
        self.file_name = "Cell/" + str(self.epoch_time) + "_" + str(self.columns) + "_" + str(self.rows) + ".json"

    def generate_grid(self):
        # Ensuring that the cell objects exist
        for i in range(0, self.columns):
            for j in range(0, self.rows):
                CellInFile(i, j)  # We don't need to store them, because we can just rebuild them when we need them

        for i in range(0, self.columns):
            for j in range(0, self.rows):
                self.grid.append([i, j])

    def initialize_grid(self):
        self.generate_grid()
        self.set_file_content()

    def get_neighbours(self, cell):
        self.get_grid()
        neighbour_index = self.get_neighbours_indexes(cell)  # Redirecting the call to the super.
        neighbours = list()
        neighbour_index = [x for x in neighbour_index if x != []]  # Unsure what causes empty lists
        for x, y in neighbour_index:
            neighbours.append([x, y])
        return neighbours

    def get_file_content(self):
        """ Getting the content from a file and storing it in the object.
        """
        with open(self.file_name, 'r') as f:
            for key, values in json.load(f).items():
                setattr(self, key, values)

    def set_file_content(self):
        """ Setting the content from a grid file in file object.
        Using the native json.dump function to store it in a JSON string.
        Uses the __dict__ call to store ALL object attributes
        """
        with open(self.file_name, 'w') as f:
            json.dump(self.__dict__, f)
        self.grid = None

    def get_grid(self):
        if not self.in_memory():
            self.get_file_content()
        return self.grid

    def in_memory(self):
        return True if self.grid else False

    def in_grid(self, x, y, clear=True):
        self.get_grid()
        found = False
        if [x, y] in self.grid:
            found = True
        if clear:
            self.grid = None
        return found

    def __getitem__(self, coordinates):
        (x, y) = coordinates
        if self.in_grid(x, y):
            return CellInFile(x, y, read=True)
        return False

    def __setitem__(self, lst, value):
        (x, y) = lst
        c = CellInFile(x, y, read=True)
        CellInFile(x, y, c.f, c.g, c.h, read=False)

    def remove_json_files(self):
        """ Clears the directory that's been created to store the files """
        import shutil
        shutil.rmtree(self.directory_name)

    def __str__(self):
        pass


def grid_factory(columns=0, rows=0):
    return GridInMemory(columns, rows)
