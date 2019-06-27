import pygame as pg
import numpy as np
import pickle as pickle
from rectangle import Rectangle
from modules.CAN_Navigation.module.Algorithms import AStar
from modules.CAN_Navigation.module.Grid import grid_factory

# square shaped grids' fixed width/height
GRID_SIZE = 60


def main():
    """
    Main function that's basically the entire application.
    Sets up pygame then fills a numpy array with rectangles to draw every draw call.
    Checks for mouse and keyboard input, marks rectangles as obstacles on mouse click.
    Uses keyboard input; S, E, Space, C to mark start and end, space to find a path and
    C to clear the screen/start over.

    TODO: Big GRID_SIZE numbers may cause slow down (marking obstacles too fast skips rectangles),
    not sure if it's the application or something inherent to pygame.

    """

    print("click to mark obstacles.")
    print("S: mark start. \nE: mark end. \nSpace: plot path. \nC: clear all.")

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
                    if not algo.path:
                        # ignore key press when either start or end isn't marked
                        if not algo.start or not algo.end:
                            continue

                        for x in range(grid.rows):
                            for y in range(grid.columns):
                                if npblocks[y, x].obstacle:

                                    grid[(x, y)].accessible = False

                        # calculate a path
                        algo.solve()

                        # remove start(twice) and end node from the path
                        algo.path.pop()
                        algo.path.pop(0)

                        # color the path yellow
                        for v2 in algo.path:
                            npblocks[v2[1], v2[0]].set_color((0, 255, 255))

                # if we press c we clear all variables and reset the grid and blocks
                if event.key == pg.K_c:
                    grid = grid_factory(GRID_SIZE, GRID_SIZE)
                    algo = AStar(grid)
                    for row in npblocks:
                        for block in row:
                            block.reset()

                if event.key == pg.K_o:
                    print("Saving map")
                    grid = grid_factory(GRID_SIZE, GRID_SIZE)
                    if save_map(npblocks,grid):
                       print("Save compleet")
                    else:
                       print("Save faild")

                if event.key == pg.K_l:
                    print("load map")
                    map_file = load_map()
                    draw_map(map_file, npblocks)

                        
                                

            # rectangle draw calls and pygame updates
            display.fill((240, 240, 240))
            rects.draw(display)
            pg.display.flip()


#save the created map
def save_map(npblocks,grid):
    
    obstacle = {}
    gird_size = [grid.rows,grid.columns]


    for x in range(grid.rows):
        for y in range(grid.columns):
            if npblocks[y, x].obstacle:     #check if there is a obstacle on y,x cordinat 
                if y in obstacle:           
                    obstacle[y].append(x)   #add an x codinat to the y cordinat
                else:
                    obstacle[y] = [x]       #make a new x codinats list for a y cordinat key

    
    #save list to a bitmap file
    with open('data.map', 'wb') as f:
        pickle.dump({'grid':gird_size, 'obsticals':obstacle}, f, pickle.HIGHEST_PROTOCOL)  

    return True

#save old created map
def load_map():
    try: #try catch to load the map 
        with open('data.map', 'rb') as f: #load map
            return pickle.load(f)
    except: #file not found
        return False

def draw_map(map,npblocks):
    if not map:
        return False

    obsticals_map = map['obsticals']
    
    #loop true all the objects on the grid
    for y in obsticals_map:
        for x in obsticals_map[y]:
            npblocks[y, x].mark_obstacle()      #place mark the obstacle on the map
    
    return True

main()



