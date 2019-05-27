from pipper import install_packages
install_packages(['pygame', 'euclid3'])

import pygame as pg
import euclid3 as vmath

from modules.CAN_Navigation.module.Structure import grid_factory
from modules.CAN_Navigation.module.Algorithms import AStar
from square import Square

def input_to_list_of_ints(string: str, delimiter: chr):
    """
    Converts input to a list of strings
    :param string: String of characters to print to the user
    :param delimiter: Character that determines when to slice
    """
    input_string = input(string)
    return list(map(int, input_string.split(delimiter)))

def main():
    grid_size = (50, 50)
    grid = grid_factory(grid_size[0], grid_size[1])
    path = None
    start = None
    end = None

    pg.init()

    width, height = 1000, 1000
    display = pg.display.set_mode((width, height), 0, 32)
    display.fill((240, 240, 240))

    block_w, block_h = width/grid_size[0], height/grid_size[1]

    blocks = list()
    start_index = None
    end_index = None
    for x in range(0, width, int(block_w)):
        for y in range(0, height, int(block_h)):
            b = Square(vmath.Vector2(x, y), vmath.Vector2(block_w, block_h))
            blocks.append(b)

    # poll events
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)

            # if we press m1 we check what block the cursor is on and mark it as an obstacle
            if pg.mouse.get_pressed()[0]:
                mouse_pos = pg.mouse.get_pos()
                for block in blocks:
                    if block.body.collidepoint(mouse_pos):
                        block.mark_obstacle()
             
            if event.type == pg.KEYDOWN:
                mouse_pos = pg.mouse.get_pos()
                if event.key == pg.K_s and start_index == None:
                    for index, block in enumerate(blocks):
                        if block.body.collidepoint(mouse_pos):
                            start_index = index
                            block.mark_start()

                if event.key == pg.K_e and end_index == None:
                    for index, block in enumerate(blocks):
                        if block.body.collidepoint(mouse_pos):
                            end_index = index
                            block.mark_end()

                if event.key == pg.K_SPACE:
                    if path == None:
                        for x in range(grid.rows):
                            for y in range(grid.columns):
                                if blocks[x + (grid.columns*y)].obstacle:
                                    grid[(x, y)].accessible = False
                                    
                        start = grid[(int(start_index / grid.rows), int(start_index % grid.columns))]
                        end = grid[(int(end_index / grid.rows), int(end_index % grid.columns))]
                        algo = AStar(grid, start, end)
                        path = algo.solve()
                        print(path)
                        path.pop()
                        for v2 in path:
                            blocks[v2[0] + (grid.rows * v2[1])].set_color((0, 255, 255))

                if event.key == pg.K_c:
                    path, start, end, end_index, start_index = None, None, None, None, None
                    grid = grid_factory(grid_size[0], grid_size[1])
                    for block in blocks:
                        block.reset()


            for block in blocks:
                block.draw(display)
            pg.display.update()

main()