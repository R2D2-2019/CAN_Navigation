# TODO: Docs
def calculate_heuristic(neighbor, end):
    # using the raw distance
    distance = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
    return distance


# TODO: Docs

class AStar:
    # TODO: Make it a data class
    def __init__(self, grid, end=None, start=None):
        self.grid = grid
        self.end = end
        self.start = start
        self.path = []

        # TODO: Closed set can be converted to a priority queue or tree to
        # speed up the process
        self.closed_set = list()

        # TODO: Same as closed_set
        self.open_set = list()

    # TODO: Docs

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

    # TODO: Docs

    def run(self):
        while self.open_set:  # checking if we still have something to read from
            lowest_index = 0
            for i in range(len(self.open_set)):
                if self.open_set[i].f < self.open_set[lowest_index].f:
                    lowest_index = i

            if self.open_set[lowest_index] is self.end:
                self.path = []
                temp = self.open_set[lowest_index]
                self.path.append(temp.get_x_y())
                while temp.previous:
                    self.path.append(temp.get_x_y())
                    temp = temp.previous
                return self.path

            # TODO: Shorten line
            indexes = self.open_set[lowest_index].get_neighbors(
                self.grid.rows, self.grid.columns)

            neighbors = list()
            for index in indexes:
                neighbors.append(self.grid[(index[0], index[1])])
            for cell in neighbors:
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
                        cell.previous = self.open_set[lowest_index]

            self.closed_set.append(self.open_set[lowest_index])
            del self.open_set[lowest_index]

        # make case variable
        return False
