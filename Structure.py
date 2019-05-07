import types


# TODO: Unit tests to ensure grid class is working as expected

class Grid:

    # TODO: Make it a data class
    def __init__(self, columns=0, rows=0):
        self.columns = columns
        self.rows = rows

        # TODO: Implement the array as a numPy Array would speed it up and require a lot less memory usage.
        # It would drop the flexibility, however we aren't doing that many
        # unique operations with it anyway
        self.grid = list()
        try:
            self.grid = [[Cell(j, i) for i in range(self.columns)]
                         for j in range(self.rows)]
        except MemoryError as error:
            error_msg = str(error)
            error_msg += " Too much memory is allocated using the column count of: "
            error_msg += str(self.columns) + \
                " and row count of: " + str(self.rows)
            print(error_msg)

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


# TODO unit tests

# TODO: Docs
class Cell:
    # TODO: Docs
    # TODO: Make it a data class
    def __init__(self, x, y, f=0, g=0, h=0):
        self.f = f
        self.g = g
        self.h = h

        self.x = x
        self.y = y
        self.neighbors = []
        self.previous = None

        # TODO: Make accessability conditional
        self.accessible = True  # Currently we only have accessible as present or not present

    # TODO: Docs
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    # TODO: Docs
    def __getattr__(self, key):
        if key in ['f', 'g', 'h']:
            return self['key']
        return False  # make it either an exception or error

    # TODO: Docs
    def get_neighbors(self, x, y):

        # TODO: Loop-based not if statement based

        if self.x < x - 1:
            self.neighbors.append([self.x + 1, self.y])
        if self.x > 0:
            self.neighbors.append([self.x - 1, self.y])
        if self.y < y - 1:
            self.neighbors.append([self.x, self.y + 1])
        if self.y > 0:
            self.neighbors.append([self.x, self.y - 1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append([self.x - 1, self.y - 1])
        if self.x < x - 1 and self.y > 0:
            self.neighbors.append([self.x + 1, self.y - 1])
        if self.x > 0 and self.y < y - 1:
            self.neighbors.append([self.x - 1, self.y - 1])
        if self.x < x - 1 and self.y < y - 1:
            self.neighbors.append([self.x + 1, self.y + 1])
        return self.neighbors
