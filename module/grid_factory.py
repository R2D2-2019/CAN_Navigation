from module.Structure import GridInFile, GridInMemory


def grid_factory(columns=0, rows=0):
    try:
        g = GridInMemory(columns, rows)
    except MemoryError:
        g = GridInFile(columns, rows)

    return g
