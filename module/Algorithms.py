from heapq import heappush, heappop


def calculate_heuristic(neighbor, end):
    """
    Calculating the heuristic based on coordinates of end and next cell
    :param neighbor: cell towards the end
    :param end:  cell where we want to end up
    :return: int value for the distance
    """
    if not neighbor or not end:
        return None
    if isinstance(neighbor, tuple) or isinstance(end, tuple):
        return (end[0] - neighbor[0]) + (end[1] - neighbor[1])
    return abs(neighbor.x - end.x) + abs(neighbor.y - end.y)


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
        self.path_alternative = []
        self.current_cell = None
        

        self.l_index, self.old_l_index = 0 , 0
        # These lists are empty by default
        self.open_set, self.closed_set = list(), list()

    def found_check(self):
        """ Checking if we found our end point """
        return True if self.open_set[self.l_index].get_x_y() == self.end.get_x_y() else False

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

    def solve_alternative(self):
        """:returns list | bool  """
        if self.run_check():
            return self.run_alternative()
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

    def reconstruct_path(self, alternative_path = False):
        """
        Starting at the last index, looping backwards to finding the path and adding to a list.
        List is reversed in the end.
        :return: List: The Path
        """
        self.path = []       

        #output alternative path
        if alternative_path:
            for temp in self.path_alternative:
                self.path.append(temp.get_x_y())
            self.path.reverse()                  
            return self.path
        
        #output normal path
        temp = self.open_set[self.l_index]
        if isinstance(temp.previous, list):
            self.path = temp.previous
            self.path.reverse()
            self.path.append(temp.get_x_y())
        else:
            while hasattr(temp, 'previous'):
                self.path.append(temp.get_x_y())
                temp = temp.previous
            self.path.reverse()
        return self.path

    def is_accessible(self, cell):
        """
        Checking if our cell is a wall and if we've already checked if we couldn't access it.
        :param cell: Potential new cell
        :return: True if we can access it false if we can't
        """
        return True if not self.in_set(cell, self.closed_set) and cell.accessible else False




    def get_lowest_index_open_set(self):
        """
        Acquiring the lowest index by comparing all cell.f values in open set
        :return: None
        """
        self.l_index = 0
        for i in range(len(self.open_set)):
            if self.open_set[i].f < self.open_set[self.l_index].f:
                self.l_index = i

    def iteration_start(self):
        """
        Function that's being called whenever an iteration of the run loop start.
        This function is merely here for overriding by child.
        """
        pass

    def iteration_end(self):
        """
        Function that's being called whenever an iteration of the run loop ends.
        This function is merely here for overriding by child.
        """
        pass

    def iteration_neighbours(self, neighbours):
        """
        Function that's being called whenever a cells neighbours are known.
        This function is merely here for overriding by child.
        """
        pass

    def iteration_path_found(self):
        """
        Function that's being called when a path has been found.
        This function is merely here for overriding by child.
        """
        pass

    def iteration_no_path_found(self):
        """
        Function that's being called when a path has been found.
        This function is merely here for overriding by child.
        """
        pass

    def in_set(self, cell, type_set):
        in_set = False
        for cells in type_set:
            if cell.get_x_y() == cells.get_x_y():
                in_set = True
        return in_set

    def nearest_path(self, path):
        """
        This function is keeping the path that is closet to the end poin.

        :return: None
        """      
        nearest = []
        temp = path
        
        #first run of this function
        if not self.path_alternative:
            self.path_alternative = temp[:]
            return
        

        distance_old = self.path_alternative[-1].get_content()['f']
        distance = temp[-1].get_content()['f'] #Heuristic based distance to end
        

        if distance < distance_old and distance is not 0 or distance_old is 0:
            self.path_alternative = temp[:]

 
    def run_alternative(self):
        """
            This function start building the alternative path
            
            :return: list path
        """
        self.reconstruct_path(True)
        return self.path

    def run(self):
        """
        The main implementation of the A* algorithm. Recommend reading the Wikipedia pseudo-code to understand it.

        :return: False if no path is found or list when path is found
        """
        while self.continuation_check():  # checking if we still have something to read from
            # We need to use the lowest available index to continue our search
            self.iteration_start()
            self.get_lowest_index_open_set()
            if self.found_check():  # If we've found our goal, ready to finalize
                self.reconstruct_path()
                self.iteration_path_found()
                return self.path  # return with a path reconstruct function call

            self.current_cell = self.open_set[self.l_index]
            neighbours = self.grid.get_neighbours(self.current_cell)
            self.iteration_neighbours(neighbours)
            for cell in neighbours:
                if self.is_accessible(cell):
                    temp_g = cell.g + 1
                    new_path = False
                    if self.in_set(cell, self.open_set):
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
            self.nearest_path(self.open_set)
            # ensuring that we don't come across the same element again
            del self.open_set[self.l_index]
            self.iteration_end()
            

        self.iteration_no_path_found()
        return False


class AstarNumpy(AStar):
    """ The AstarNumpy works a little bit differently from the other AStar implementation.
    The reason for this change is because NumPy works best when we're NOT storing objects with arrays.
    It's best to store values and allow NumPy to deal with the math complexity.
    For the current implementation we're only allowing boolean logic for accessibility.
    This might seem similar to others, however implementing this to use integral or different stages of
    accessibility (i.e. different scales of complex it is to get somewhere) will require everything to be rewritten.
    Keep this in mind for future progress.
    Date of creation: 28 of May 2019.
    """

    def __init__(self, grid, start=None, end=None):
        """
        :param grid: A grid or node based structure that knows indexes
        :param start: The start cell
        :param end: The end cell
        """
        AStar.__init__(self, grid, start, end)

        self.grid = grid  # I've decided AGAINST creating a grid because this would mess with the numpy access operators
        # Simply put calling variables using [] would result in [()] and calling actual grid functions
        self.end = end
        self.start = start
        self.path = []
        self.current_cell = None

        """In here you will find one of the biggest changes made in the implementation
        NumPy is the master when it comes to data management, so we won't even bother creating unique instances
        for each and every cell, we will leave that to numpy. What we do need to do is keep track of the data
        we would ordinarily store in a cell, in this case we use two dicts

        """
        self.g = {self.start: 0}
        self.f = {self.start: calculate_heuristic(self.start, self.end)}
        # These lists are empty by default
        self.open_set, self.closed_set = list(), set()
        self.previous = {}



    def solve(self):
        """ :returns list | bool """
        if self.run_check():
            heappush(self.open_set, (self.f[self.start], self.start))
            return self.run()
        else:
            return None
        

    def found_check(self):
        """
        Answers the: have we found our end destination
        :returns bool """
        return True if self.current_cell == self.end else False

    def reconstruct_path(self):
        """After we've found our path we can rebuild it by asking our previous for the previous and so on.
        :returns void
        """
        self.path = []
        while self.current_cell in self.previous:
            self.path.append(self.current_cell)
            self.current_cell = self.previous[self.current_cell]
        self.path.append(self.start)
        self.path.reverse()

    def run(self):
        """The main loop that has the algorithm's run in it.
        :returns list | bool
        """
        while self.continuation_check():  # Are we allowed to continue or have we exploited all our possibilities?
            self.iteration_start()
            self.current_cell = heappop(self.open_set)[1]  # Popping also means we don't have to remove it later!

            if self.found_check():
                self.reconstruct_path()
                self.iteration_path_found()
                return self.path

            neighbours = self.grid.get_neighbours(self.current_cell)

            self.iteration_neighbours(neighbours)
            for neighbor in neighbours:
                temp_g = self.g[self.current_cell] + calculate_heuristic(self.current_cell, neighbor)
                if 0 <= neighbor[0] < self.grid.array.shape[0]:
                    if 0 <= neighbor[1] < self.grid.array.shape[1]:
                        if self.grid.array[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        continue
                else:
                    continue

                if neighbor in self.closed_set and temp_g >= self.g.get(neighbor, 0):
                    continue

                if temp_g < self.g.get(neighbor, 0) or neighbor not in [i[1] for i in self.open_set]:
                    self.previous[neighbor] = self.current_cell
                    self.g[neighbor] = temp_g
                    self.f[neighbor] = temp_g + calculate_heuristic(neighbor, self.end)
                    heappush(self.open_set, (self.f[neighbor], neighbor))  # pushing our new found element to be checked

                self.closed_set.add(self.current_cell)
                self.iteration_end()
        self.iteration_no_path_found()
        return False