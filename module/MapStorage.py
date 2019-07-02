import pickle as pickle

'''
 save_map 
    This function saves a map in a bitmap file 
    input is 
        npblock: ? , (this are the blocks of the map)
        gird: list , (the size that the grid is in)
        name: string , (name of the file)
 :return: bool 
'''
def save_map(npblocks, grid, name = 'data'):
    
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
    with open(name+'.map', 'wb') as f:
        pickle.dump({'grid':gird_size, 'obsticals':obstacle}, f, pickle.HIGHEST_PROTOCOL)  

    return True

'''
    load_map
        This function loads the map
    input is
        name: string, (the name of the file)
'''
def load_map(name='data'):
    try: #try catch to load the map 
        with open(name+'.map', 'rb') as f: #load map
            return pickle.load(f)
    except: #file not found
        return False
'''
    draw_map
        This function draws a map
        :input:
        map is the map that is loaded
        npblocks is a refrence and used to send the data back
    :return: bool
'''
def draw_map(map, npblocks):
    if not map:
        return False
    obsticals_map = map['obsticals']
    #loop true all the objects on the grid
    for y in obsticals_map:
        for x in obsticals_map[y]:
            npblocks[y, x].mark_obstacle()      #place mark the obstacle on the map
    return True