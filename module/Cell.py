class Cell:

    def __init__(self):
        pass

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        pass


class AstarCell(Cell):
    def __init__(
            self,
            x,
            y,
            f=0,
            g=0,
            h=0,
    ):
        pass

    def get_x_y(self):
        pass

    def set_accessible(self, state):
        pass

    def set_previous(self, item):
        pass


class CellInMemory(AstarCell):
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
        self.previous = list()
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
        return object.__getattribute__(self, key)

    def set_accessible(self, state):
        self.accessible = state

    def get_x_y(self):
        """ Getting the  Cell X and Y coordinates.
                Returns:
                    list: Returns X and Y coordinates.
        """
        return [self.x, self.y]


def generate_file_name(x, y):
    return str(x) + "_" + str(y) + ".json"


class CellInFile(CellInMemory):
    def __init__(self, file_storage, x=0, y=0, f=0, g=0, h=0, read=False):
        self.file_name = None
        CellInMemory.__init__(self, x, y, f, g, h)
        self.x = x
        self.y = y
        self.file_storage = file_storage
        self.file_name = generate_file_name(self.x, self.y)
        if read:
            self.get_file_content()
        else:
            self.set_file_content()

    def __setattr__(self, key, value):
        """ Setting a new attribute to the internal dict.

        Keep in mind that these variables will also be stored in the file.
        """
        self.__dict__[key] = value

    def set_previous(self, item):
        """ Setting the previous Cell.
        Detects if the item points to itself.


        item (obj): Cell like object that has get_x_y function.

        """
        if self.get_x_y() != item.get_x_y():
            self.previous = [item.get_x_y()] + item.get_previous()

    def get_previous(self):
        return self.previous

    def get_file_content(self):
        """ Getting the content from a file and storing it in the object.
        Afterwards removing the file_name, conserve memory and can be generated.
        """
        self.file_storage.get_file_content(self)

    def set_file_content(self):
        """ Setting the content from a cell in file object.
        Using the native json.dump function to store it in a JSON string.
        Uses the __dict__ call to store ALL object attributes
        """
        self.file_storage.set_file_content(self)

    def set_accessible(self, state):
        self.accessible = state
        self.set_file_content()

    def __delete__(self, instance):
        self.set_file_content()
