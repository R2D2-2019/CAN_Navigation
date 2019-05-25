from module.Structure import GridInMemory
from module.Structure import GridInFile
from module.Structure import GridInNumpy


def calculate_potential_size(columns, rows):
    # TODO: Instantiate cells for a better idea of size
    """ ROUGH ESTIMATION, UNRELIABLE IN NATURE"""

    overhead = 100000  # meant as a SOFT indication on what we need for the actual algorithm operation

    var_size = 64  # max amount of bits that are expected to be used to store
    # 5 is the amount of variables stored (x,y,f,g,h)
    return overhead + ((5 * (columns * rows)) * var_size)


def grid_factory(columns=0, rows=0):
    # Trying if we can actually do it memory wise:
    import os
    import psutil
    import importlib

    process = psutil.Process(os.getpid())
    available_bits = process.memory_info().rss * 8  # the amount of "free" memory we have for our process

    # Numpy ISN'T a hard requirement, though it's nice to mention it DOES help.
    numpy_loader = importlib.util.find_spec('numpy')

    if available_bits < calculate_potential_size(rows, columns):
        if numpy_loader is not None:
            return GridInNumpy(columns, rows)
        return GridInFile(columns, rows)
    return GridInMemory(columns, rows)
