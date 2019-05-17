# TODO: Unit tests to ensure grid class is working as expected

def GridFactory(columns=0, rows=0):
    columns = columns
    rows = rows
    try:
        columns.grid = [[Cell(j, i) for i in range(columns)]
                        for j in range(rows)]
    except MemoryError as error:
        error_msg = str(error)
        error_msg += " Too much memory is allocated using the column count of: "
        error_msg += str(self.columns) + \
                     " and row count of: " + str(self.rows)
        print(error_msg)


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
    def __init__(self, columns=0, rows=0, cell=None):
        Grid.__init__(self, columns, rows)

        if not cell:
            cell = CellInMemory

        self.grid = [[cell(j, i) for i in range(self.columns)]
                     for j in range(self.rows)]

    def get_neighbours(self, cell):
        neighbour_index = self.get_neighbours_indexes(cell)
        neighbours = list()
        for index in neighbour_index:
            neighbours.append(self.grid[index[0]][index[1]])
        return neighbours

    def get_neighbours_indexes(self, cell):
        if cell.neighbours:
            return cell.neighbours
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

    def __getitem__(self, lst):
        x, y = lst
        return self.grid[x][y]

    def __setitem__(self, lst, value):
        x, y = lst
        self.grid[x][y].f = value

    def __str__(self):
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
        # In Order to prevent collisions we'll be using a random.random AND the epoch time to has a path
        # While these will prevent MOSTLY prevent collisions, they aren't immune to it.

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


# TODO: Docs
class CellInMemory(Cell):
    # TODO: Docs
    # TODO: Make it a data class
    def __init__(self, x, y, f=0, g=0, h=0):
        Cell.__init__(self)
        self.f = f
        self.g = g
        self.h = h

        self.x = x
        self.y = y
        self.neighbours = []
        self.previous = None

        # TODO: Make accessibility conditional
        self.accessible = True  # Currently we only have accessible as present or not present

    # TODO: Docs
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    # TODO: Docs
    def __getattr__(self, key):
        if key in ['f', 'g', 'h']:
            return self['key']
        return False  # make it either an exception or error

    def get_x_y(self):
        return [self.x, self.y]