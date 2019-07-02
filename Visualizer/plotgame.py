import pygame as pg
import numpy as np

from rectangle import Rectangle
from modules.CAN_Navigation.module.Algorithms import AStar
from modules.CAN_Navigation.module.Grid import grid_factory
from modules.CAN_Navigation.Visualizer.maploader import *
# square shaped grids' fixed width/height
GRID_SIZE = 30


#this is al demo code 
start_position = [0,0]  
end_found      = False

def main():
    """
    Main function that's basically the entire application.
    Sets up pygame then fills a numpy array with rectangles to draw every draw call.
    Checks for mouse and keyboard input, marks rectangles as obstacles on mouse click.
    Uses keyboard input; S, E, Space, C to mark start and end, space to find a path and
    C to clear the screen/start over.
    O is to save the map.
    L is to load the map

    TODO: Big GRID_SIZE numbers may cause slow down (marking obstacles too fast skips rectangles),
    not sure if it's the application or something inherent to pygame.

    """

    print("click to mark obstacles.")
    print("S: mark start. \nE: mark end. \nSpace: plot path. \nC: clear all. \nO is to save the map.\nL is to load the map")
    print("Right arrow is next step")

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
            b = Rectangle((x, y), (block_w, block_h))
            blocks[-1].append(b)

    # create a numpy array based on the (slow) python list of lists
    npblocks = np.array(blocks)
    del blocks

    # create a sprite group to reduce draw calls
    rects = pg.sprite.Group()
    for row in npblocks:
        for rect in row:
            rects.add(rect)

    # poll events
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)
        
        #if we press m1 we check what block the cursor is on and mark it as an obstacle
            if pg.mouse.get_pressed()[0]:
                mouse_pos = pg.mouse.get_pos()
                
                for row in npblocks:
                    for block in row:
                        if block.rect.collidepoint(mouse_pos):
                            block.mark_obstacle()


            if event.type == pg.KEYDOWN:
                mouse_pos = pg.mouse.get_pos()
                # if we press s for the first time we check on which block the mouse is set it as start
                if event.key == pg.K_s and not algo.start:
                    for y, row in enumerate(npblocks):
                        for x, block in enumerate(row):
                            if block.rect.collidepoint(mouse_pos):
                                algo.start = grid[(x, y)]
                                block.mark_start()
                # if we press e for the first time we check on which block the mouse is and set is as end
                if event.key == pg.K_e and not algo.end:
                    for y, row in enumerate(npblocks):
                        for x, block in enumerate(row):
                            if block.rect.collidepoint(mouse_pos):
                                algo.end = grid[(x, y)]
                                block.mark_end()

                # if we press space for the first time we map obstacles to the grid and get a path
                if event.key == pg.K_SPACE:
                    for x in range(grid.rows):
                        for y in range(grid.columns):
                            if npblocks[y, x].obstacle:
                                grid[(x, y)].accessible = False
                    algo = calculate_rout(algo, grid, 0)
                    color_path(algo, npblocks)
                    if end_found:
                        print("found the end of the route")
                    else:
                        print("did not find the end")
                        change_end(algo.path[-1])


                # if we press c we clear all variables and reset the grid and blocks
                if event.key == pg.K_c:
                    grid = grid_factory(GRID_SIZE, GRID_SIZE)
                    algo = AStar(grid)
                    for row in npblocks:
                        for block in row:
                            block.reset()
                
                #save the created map
                if event.key == pg.K_o:
                    print("Saving map")
                    grid = grid_factory(GRID_SIZE, GRID_SIZE)
                    if save_map(npblocks,grid):
                       print("Save compleet")
                    else:
                       print("Save faild")

                #load a saved map
                if event.key == pg.K_l:
                    print("load map")
                    map_file = load_map()
                    #grid = grid_factory(GRID_SIZE, GRID_SIZE)
                    #algo = AStar(grid)
                        

                    #clean up the screen
                    for row in npblocks:
                        for block in row:
                            block.reset()  

                    draw_map(map_file, npblocks, GRID_SIZE, start_position)


                        
                                

            # rectangle draw calls and pygame updates
            display.fill((240, 240, 240))
            rects.draw(display)
            pg.display.flip()

def change_end(new_path):
    global start_position
    start_position = [new_path[1]-2,new_path[0]-2]
    #start_position = new_path
    

def calculate_rout(algo, grid, loop):
    global end_found

    if not algo.path:
        # ignore key press when either start or end isn't marked
        if not algo.start or not algo.end:
            return False
        
        #print(algo.end.get_x_y(), algo.start.get_x_y(), end=' nr 1 \n')


        # calculate a path
        compleet_algo = algo.solve()

        if compleet_algo:
            if loop is 0:
                end_found = True
                algo.path.pop()
                algo.path.pop(0)

            return algo
        
        compleet_algo = algo.solve_alternative()
        new_end = algo.path[0]
        tmp_start = algo.start

        algo = AStar(grid)
        algo.end = grid[(new_end[0],new_end[1])]
        algo.start = tmp_start

        


        return calculate_rout(algo, grid, 1 )
    return False


def color_path(algo, npblocks):
        # color the path 
        if  algo:
            i = 0
            for value in algo.path:
                if i is 0:
                    npblocks[value[1], value[0]].set_color((0, 255, 0))
                elif i is len(algo.path)-1:
                    npblocks[value[1], value[0]].set_color((255, 0, 0))
                else:
                    npblocks[value[1], value[0]].set_color((0, 255, 255))

                i += 1

main()



