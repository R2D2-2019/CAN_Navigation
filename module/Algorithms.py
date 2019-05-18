# TODO: Docs
def calculate_heuristic(neighbor, end):
    # using the raw distance
    distance = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
    return distance


# TODO: Docs


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

    def __init__(self, grid, end=None, start=None):
        PathfindingAlgorithm.__init__(self)
        self.grid = grid
        self.end = end
        self.start = start
        self.path = []

        self.l_index = 0
        # These lists are empty by default
        self.open_set, self.closed_set = list(), list()

    # TODO: Docs
    def interval_control(self):
        pass

    def found_check(self):
        return True if self.open_set[self.l_index] is self.end else False

    def continuation_check(self):
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
        self.path = []
        temp = self.open_set[self.l_index]
        while temp.previous:
            self.path.append(temp.get_x_y())
            temp = temp.previous
        self.path.append(self.start.get_x_y())
        return self.path

    def is_accessible(self, cell):
        return True if cell not in self.closed_set and cell.accessible else False

    def get_lowest_index_open_set(self):
        self.l_index = 0
        for i in range(len(self.open_set)):
            if self.open_set[i].f < self.open_set[self.l_index].f:
                self.l_index = i

    def run(self):
        while self.continuation_check():  # checking if we still have something to read from
            self.get_lowest_index_open_set()
            if self.found_check():
                return self.reconstruct_path()
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
            del self.open_set[self.l_index]
        return False
