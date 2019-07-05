import numpy as np
import os 
import unittest
from modules.CAN_Navigation.module.MapStorage import map_storage 


class TestMapLoadSave(unittest.TestCase):
        """
        Basic test class for the map loader function
        containts:
                - check if the file load correct
        """
        def test_file_save(self):
                file_location = './modules/CAN_Navigation/test/maploader/'
                file_name     = 'test_file'
                file_extention= 'data'
                file_data = {'grid': [5, 5], 'obsticals': {0: [0, 1, 2, 3, 4], 1: [0, 1, 2, 3, 4], 2: [0, 1, 2, 3, 4], 3: [0, 1, 2, 3, 4], 4: [0, 1, 2, 3, 4]}}
                
                storage_file  = map_storage(file_location,file_extention,file_data['grid'][0])

                load_data = storage_file.load(file_name)
                
                self.assertEqual(file_data['grid'][0], load_data['grid'][0])
                self.assertEqual(file_data['grid'][1], load_data['grid'][1])
                self.assertEqual(file_data['obsticals'], load_data['obsticals'])

        def test_file_save(self):
                file_location = './modules/CAN_Navigation/test/maploader/'
                file_name     = 'test_file'
                file_extention= 'data'
                file_full_path= file_location+ file_name+ "."+ file_extention
                file_data = {'grid': [5, 5], 'obsticals': {0: [0, 1, 2, 3, 4], 1: [0, 1, 2, 3, 4], 2: [0, 1, 2, 3, 4], 3: [0, 1, 2, 3, 4], 4: [0, 1, 2, 3, 4]}}               
                

                storage_file  = map_storage(file_location,file_extention,file_data['grid'][0])

                save_file = storage_file.save_file(file_name,file_data) 
                file_found = os.path.isfile(file_full_path)

                self.assertEqual(True, save_file)
                self.assertEqual(True, file_found)

if __name__ == '__main__':
    unittest.main()