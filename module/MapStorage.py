import pickle as pickle


class map_storage:
    
    def __init__(self, directory_name, file_extention, grid_size):
        self.directory_name = directory_name
        self.file_extention = file_extention
        self.map = None
        self.grid_size = grid_size

    '''
    file_path
    set the file path
    :return: string of the file path
    '''
    def file_path(self, file_name):
        if not self.directory_name:
            self.directory_name = "./"
        if not self.file_extention:
            self.file_extention = ".map"
        return self.directory_name + file_name + '.' + self.file_extention
    '''
    save 
        This function will work only for the plotgame file
        it will save the file that was drawn in the plotgame
        input is 
            npblock: ? , (this are the blocks of the map)
            gird: list , (the size that the grid is in)
            name: string , (name of the file)
    :return: bool 
    '''
    def save_plotgame(self, npblocks ,grid ,file_name ):
        obstacle = {}
        gird_size = [grid.rows,grid.columns]
        
        
        for x in range(grid.rows):
            for y in range(grid.columns):
                #if npblocks[y, x].obstacle:     #check if there is a obstacle on y,x cordinat 
                if y in obstacle:           
                    obstacle[y].append(x)   #add an x codinat to the y cordinat
                else:
                    obstacle[y] = [x]       #make a new x codinats list for a y cordinat key        
        return self.save_file(file_name , {'grid':gird_size, 'obsticals':obstacle})

    '''
        save_file
            This function saves a map in a bitmap file
        input is
            name: string, (the name of the file)
    '''    
    def save_file(self, file_name, file_data):
        filepath = self.file_path(file_name)
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(file_data, f, pickle.HIGHEST_PROTOCOL)  
        except:
            return False
        
        return True
        
    '''
        load_map
            This function loads the map
        input is
            name: string, (the name of the file)
    '''
    def load(self, file_name):
        try: #try catch to load the map 
            with open(self.file_path(file_name), 'rb') as f: #load map
                self.map = pickle.load(f)
                return self.map
        except: #file not found
            return False        
    '''
        change_dir
            change the directory where the file is saved
        :return: bool
    '''
    def change_dir(self, directory):
        self.directory_name = directory
        return True
    '''
        draw_map
            This function draws a map
            :input:
            map is the map that is loaded
            npblocks is a refrence and used to send the data back
        :return: bool
    '''    
    def draw(self, npblocks, start_position):
        if not self.map:
            return False
        obsticals_map = self.map['obsticals']

        #select start draw position
        if not start_position or (start_position[0] is 0 and start_position[1] is 0): 
            start_position = [0, 0]
            end_map_position = [start_position[0] + self.grid_size, start_position[1] + self.grid_size]
        else:
            end_map_position = [start_position[0] + (self.grid_size-1), start_position[1] + (self.grid_size-1)]
            start_position = [start_position[0] -1 , start_position[1] - 1]

        for y in range(start_position[1], end_map_position[1]):
            for x in range(start_position[0], end_map_position[0]):
                if y in obsticals_map and x in obsticals_map[y]:
                    place_y = y - start_position[1]
                    place_x = x - start_position[0]
                    npblocks[place_y, place_x].mark_obstacle()      
        return True
