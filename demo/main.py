
import os
import pickle as pickle
import time
from modules.CAN_Navigation.module.Algorithms import AStar
from modules.CAN_Navigation.Visualizer.maploader import *





def map_terminal(map):
    os.system('cls' if os.name == 'nt' else 'clear') #clearing terminal   

    #change 
    obsticals_map = map['obsticals']
    grid_size     = map['grid']

    #icons for displaying ground and the walls
    ground = '░'
    wall = '█'

    for x in range(0,grid_size[0]):
        for y in range(0,grid_size[1]):

            if y in obsticals_map and x in obsticals_map[y]:
                print(wall, end='')
            else:
                print(ground, end='')
        print('')







while True:
    map_data = load_map()
    map_terminal(map_data)
    time.sleep(2)

        
