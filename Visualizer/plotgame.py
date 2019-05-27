from pipper import install_packages
install_packages(['pygame', 'euclid3'])
from square import Square
from modules.CAN_Navigation.module.Algorithms import AStar
from modules.CAN_Navigation.module.Structure import grid_factory
import euclid3 as vmath
import pygame as pg


GRID_SIZE = 50


def main():
    # grid size is fixed , tried 200x200 but it's really slow
    grid = grid_factory(GRID_SIZE, GRID_SIZE)
    algo = AStar(grid)

    # init pygame and open a white window thats 1000x1000 res
    pg.init()
    width, height = 1000, 1000
    display = pg.display.set_mode((width, height), 0, 32)
    display.fill((240, 240, 240))

    # determine how big the blocks need to be
    block_w, block_h = width/grid.rows, height/grid.columns

    # fill blocks (2D list of lists)
    blocks = list()
    for x in range(0, width+1, int(block_w)):
        blocks.append(list())
        for y in range(0, height+1, int(block_h)):
            b = Square(vmath.Vector2(x, y), vmath.Vector2(block_w, block_h))
            blocks[-1].append(b)

    # poll events
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)

            # if we press m1 we check what block the cursor is on and mark it as an obstacle
            if pg.mouse.get_pressed()[0]:
                mouse_pos = pg.mouse.get_pos()
                for row in blocks:
                    for block in row:
                        if block.body.collidepoint(mouse_pos):
                            block.mark_obstacle()

            if event.type == pg.KEYDOWN:
                mouse_pos = pg.mouse.get_pos()
                # if we press s for the first time we check on which block the mouse is set it as start
                if event.key == pg.K_s and not algo.start:
                    for y, row in enumerate(blocks):
                        for x, block in enumerate(row):
                            if block.body.collidepoint(mouse_pos):
                                algo.start = grid[(x, y)]
                                block.mark_start()
                # if we press e for the first time we check on which block the mouse is and set is as end
                if event.key == pg.K_e and not algo.end:
                    for y, row in enumerate(blocks):
                        for x, block in enumerate(row):
                            if block.body.collidepoint(mouse_pos):
                                algo.end = grid[(x, y)]
                                block.mark_end()
                # if we press space for the first time we mark all obstacle blocks als inaccessible in our grid
                if event.key == pg.K_SPACE:
                    if not algo.path:
                        if not algo.start or not algo.end:
                            continue

                        for x in range(grid.rows):
                            for y in range(grid.columns):
                                if blocks[y][x].obstacle:
                                    grid[(x, y)].accessible = False

                        # calculate a path
                        algo.solve()

                        # remove start(twice) and end node from the path
                        algo.path.pop()
                        algo.path.pop(0)
                        algo.path.pop(0)

                        # color the path yellow
                        for v2 in algo.path:
                            blocks[v2[1]][v2[0]].set_color((0, 255, 255))

                # if we press c we clear all variables and reset the grid and blocks
                if event.key == pg.K_c:
                    grid = grid_factory(GRID_SIZE, GRID_SIZE)
                    algo = AStar(grid)
                    for row in blocks:
                        for block in row:
                            block.reset()

            # block draw calls and pygame updates
            for row in blocks:
                for block in row:
                    block.draw(display)
            pg.display.update()


main()
