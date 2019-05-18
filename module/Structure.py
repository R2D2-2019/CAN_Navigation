# TODO: Unit tests to ensure grid class is working as expected

# TODO: must contain a memory check, must return the constructed grid type
# (InMemory or InFile) with the limit Cell type


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

    # TODO: Make it a data class

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


class GridInFile(Grid):

    def __init__(self, columns=0, rows=0):
        Grid.__init__(self, columns, rows)

        # The InFile will create it's own file structure on a hard drive (in the module folder)
        # In Order to prevent collisions we'll be using a random.random AND the epoch time to hash a path
        # While these will prevent MOSTLY prevent collisions, they aren't
        # immune to it.

    def hash_path(self):
        pass

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


# TODO unit tests

class Cell:

    def __init__(self):
        pass

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        pass

    def get_x_y(self):
        pass

    def get_neighbours(self):
        pass

    def set_previous(self, item):
        pass


# TODO: Docs

class CellInMemory(Cell):
    """ InMemory storage for a Cell
    Inherits from the Abstract Cell class.
    """

    def __init__(
            self,
            x,
            y,
            f=0,
            g=0,
            h=0,
    ):
        """
        x: Can't be zero None, because the cell needs to be somewhere
        y: Same as X
        f: Heuristic based distance to end
        g: Cost of getting from the start cell to this cell
        h: Heuristic distance
        """
        Cell.__init__(self)

        #
        self.f = f
        self.g = g
        self.h = h

        self.x = x  # Storing the X coordinate according to the grid
        self.y = y  # Storing the Y coordinate according to the grid

        # Caching mechanism that prevents large scale I/O operations. Can
        # operate without.
        self.neighbours = []
        # Used for path acquiring when an algorithm is done. It while's
        # accessing all previous
        self.previous = None
        self.accessible = True  # Currently we only have accessible as present or not present

    def __setattr__(self, key, value):
        # Currently used to update the f/g/h, accessibility and neighbours
        self.__dict__[key] = value

    def set_previous(self, item):
        """ Setting the previous Cell.
        Detects if the item points to itself.


        item (obj): Cell like object that has get_x_y function.

        """
        if self.get_x_y() != item.get_x_y():
            self.previous = item

    def __getattr__(self, key):
        return self['key']

    def get_x_y(self):
        """ Setting the previous Cell.
                Detects if the item points to itself.

                Returns:
                    list: Returns X and Y coordinates.
        """
        return [self.x, self.y]


def grid_factory(columns=0, rows=0):
    return GridInMemory(columns, rows)


def cell_factory(x, y, f=0, g=0, h=0):
    # Default allocation for the memory grid is inMemory cell
    # However it should be possible to use a different cell type
    # The reason why is unclear at this time.
    return CellInMemory(x, y, f, g, h)
