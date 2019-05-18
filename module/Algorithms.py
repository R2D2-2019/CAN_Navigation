# TODO: Docs
def calculate_heuristic(neighbor, end):
    # using the raw distance
    distance = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
    return distance

class Algorithm:
    def __init__(self):
        pass

    def solve(self):
        pass

    def run(self):
        pass

    def run_check(self):
        pass


class PathfindingAlgorithm(Algorithm):

    def __init__(self):
        Algorithm.__init__(self)

    def continuation_check(self):
        pass

    def found_check(self):
        pass


class AStar(PathfindingAlgorithm):
    """ The AStar class is the basic implementation of the A* search algorithm.

        The class is built using the basics of the basics, but keeping expandability in mind.
        As of writing the class there's been talk of:
            - more complex heuristics,
            - different level of accessibility
            - Field D* implementation
        In order to scale accordingly most of the validation checks are done not in the main while loop.
        They are done using class methods.
        The reason this might be useful is because it allows an inheritance class to merely change one of these functions.
        Not requiring a future user to rebuild an entire algorithm seemed like the smart thing to do.

    """

    def __init__(self, grid, start=None, end=None):
        """

        :param grid: A grid or node based structure that knows indexes
        :param start: The start cell
        :param end: The end cell
        """
        PathfindingAlgorithm.__init__(self)
        self.grid = grid
        self.end = end
        self.start = start
        self.path = []

        self.l_index = 0
        # These lists are empty by default
        self.open_set, self.closed_set = list(), list()

    # TODO: Docs

    def found_check(self):
        """ Checking if we found our end point """
        return True if self.open_set[self.l_index] is self.end else False

    def continuation_check(self):
        """ Checking if we can still continue searching """
        return True if self.open_set else False

    def solve(self):
        """ :returns list | bool """
        if self.run_check():
            self.open_set.append(self.start)
            return self.run()
        else:
            return None

    def run_check(self):
        """
        Done to validate if the main run function can be called (all variables present)
        :return: True | False
        """
        if self.end is None or self.start is None:
            return False
        return True

    def reconstruct_path(self):
        """
        Starting at the last index, looping backwards to finding the path and adding to a list.
        List is reversed in the end.
        :return: List: The Path
        """
        self.path = []
        temp = self.open_set[self.l_index]
        while temp.previous:
            self.path.append(temp.get_x_y())
            temp = temp.previous
        self.path.append(self.start.get_x_y())
        self.path.reverse()
        return self.path

    def is_accessible(self, cell):
        """
        Checking if our cell is a wall and if we've already checked if we couldn't access it.
        :param cell: Potential new cell
        :return: True if we can access it false if we can't
        """
        return True if cell not in self.closed_set and cell.accessible else False

    def get_lowest_index_open_set(self):
        """
        Acquiring the lowest index by comparing all cell.f values in open set
        :return: None
        """
        self.l_index = 0
        for i in range(len(self.open_set)):
            if self.open_set[i].f < self.open_set[self.l_index].f:
                self.l_index = i

    def run(self):
        """
        The main implementation of the A* algorithm. Recommend reading the wiki pseudo-code to understand it.

        :return: False if no path is found or list when path is found
        """
        while self.continuation_check():  # checking if we still have something to read from
            self.get_lowest_index_open_set()  # We need to use the lowest available index to continue our search
            if self.found_check():  # If we've found our goal, ready to finalize
                return self.reconstruct_path()  # return with a path reconstruct function call
            current_cell = self.open_set[self.l_index]
            neighbours = self.grid.get_neighbours(current_cell)
            for cell in neighbours:
                if self.is_accessible(cell):
                    temp_g = cell.g + 1
                    new_path = False
                    if cell in self.open_set:
                        if temp_g < cell.g:
                            cell.g = temp_g
                            new_path = True
                    else:
                        cell.g = temp_g
                        new_path = True

                        self.open_set.append(cell)
                    if new_path:
                        cell.h = calculate_heuristic(cell, self.end)
                        cell.f = cell.g + cell.h
                        cell.set_previous(self.open_set[self.l_index])

            self.closed_set.append(self.open_set[self.l_index])
            del self.open_set[self.l_index]  # ensuring that we don't come across the same element again
        return False
