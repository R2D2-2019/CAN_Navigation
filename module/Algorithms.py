# TODO: Docs
def calculate_heuristic(neighbor, end):
    # using the raw distance
    distance = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
    return distance


# TODO: Docs

class AStar:

    def __init__(self, grid, end=None, start=None):
        self.grid = grid
        self.end = end
        self.start = start
        self.path = []

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
        if self.pre_run_check():
            self.open_set.append(self.start)
            return self.run()
        else:
            return None

    # TODO: Docs
    def pre_run_check(self):
        if self.end is None or self.start is None:
            return False
        return True

    def traverse_path(self):
        self.path = []
        temp = self.open_set[self.l_index]
        while temp.previous:
            self.path.append(temp.get_x_y())
            temp = temp.previous
        self.path.append(self.start.get_x_y())
        return self.path

    # TODO: Docs
    def run(self):
        while self.continuation_check():  # checking if we still have something to read from
            self.l_index = 0
            for i in range(len(self.open_set)):
                if self.open_set[i].f < self.open_set[self.l_index].f:
                    self.l_index = i

            if self.found_check():
                return self.traverse_path()

            current_cell = self.open_set[self.l_index]

            neighbours = self.grid.get_neighbours(current_cell)
            for cell in neighbours:
                if cell not in self.closed_set and cell.accessible:
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
                        cell.previous = self.open_set[self.l_index]

            self.closed_set.append(self.open_set[self.l_index])
            del self.open_set[self.l_index]

        # make case variable
        return False
