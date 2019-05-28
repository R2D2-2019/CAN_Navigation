from modules.CAN_Navigation.module.Grid import grid_factory
from modules.CAN_Navigation.module.Algorithms import AStar
import matplotlib.animation as animation
import matplotlib.pyplot as plt


def input_to_list_of_ints(string: str, delimiter: chr):
    """
    Converts input to a list of strings
    :param string: String of characters to print to the user
    :param delimiter: Character that determines when to slice
    """
    input_string = input(string)
    return list(map(int, input_string.split(delimiter)))


def update_graph(c, ax, x_points, y_points):
    """ 
    This updates the graph every frame
    :param c: matplotlib uses this as frame counter
    :param ax: axis we draw to
    :param x_points: x values of every vector2 in a path
    :param y_points: y values of every vector2 in a path
    """
    x, y = list(), list()
    for i in range(c):
        x.append(x_points[i])
        y.append(y_points[i])
    ax.plot(x, y, 'r--')


def main():
    """
    Main fuction that gets all the needed variables to setup the grid and Astar class from input.
    Asks the user if it needs to be animated or not.
    Uses matplotlib animation function to visually represent the path as a line(s) in xy space.
    """
    grid_size = input_to_list_of_ints("grid size: ", ',')
    start = input_to_list_of_ints("start vector: ", ',')
    end = input_to_list_of_ints("end vector: ", ',')
    animated = input("animated? y/n : ")
    animated = True if animated == 'y' else False

    figure = plt.figure()
    axes = figure.add_subplot()
    plt.axis([0, grid_size[0], 0, grid_size[1]])

    grid = grid_factory(grid_size[0], grid_size[1])
    start_point = grid[(start[0], start[1])]
    end_point = grid[(end[0], end[1])]
    algo = AStar(grid, start_point, end_point)
    path = algo.solve()

    # seperate the path into a list of x and y values
    x_points, y_points = list(), list()
    for vector2 in path:
        x_points.append(vector2[0])
        y_points.append(vector2[1])

    # if the user wants animations we call FuncAnimation (matplotlib) else we just plot all at once
    if animated:
        ani = animation.FuncAnimation(figure, update_graph, interval=50, fargs=[
                                      axes, x_points, y_points], frames=len(x_points), repeat=False)
    else:
        axes.plot(x_points, y_points, 'r--')

    axes.grid()
    plt.show()


main()
