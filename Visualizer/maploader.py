import pickle as pickle

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

def draw_map(map,npblocks, grid_size, start_position):
    if not map :
        return False
    
    if not start_position: #if there is no starting position just make it 0
        start_position = [0,0]

    obsticals_map = map['obsticals']
    end_map_position = [start_position[0] + grid_size, start_position[1] + grid_size]

    print(start_position, end_map_position)

    for y in range(start_position[0], end_map_position[0]):
        for x in range(start_position[1], end_map_position[1]):
            if x in obsticals_map[y]:
                place_y = y - start_position[0]
                place_x = x - start_position[1]
                npblocks[place_y, place_x].mark_obstacle()      #place mark the obstacle on the map
            #if obsticals_map[y][x]:
            #    
    return True
'''
    #loop true all the objects on the grid
    for y in obsticals_map:
        for x in obsticals_map[y]:
            npblocks[y, x].mark_obstacle()      #place mark the obstacle on the map
'''  
    