import json


class FileStorage:
    def __init__(self, directory_name):
        self.directory_name = directory_name

    def path(self, instance):
        """ Getting the path based on the directory and instance names"""
        return self.directory_name + "/" + instance.file_name

    def get_file_content(self, instance):
        """ Getting the content from a file and storing it in the object.
        """
        with open(self.path(instance), 'r') as f:
            for key, values in json.load(f).items():
                setattr(instance, key, values)

    def set_file_content(self, instance):
        """ Setting the content from a grid file in file object.
        Using the native json.dump function to store it in a JSON string.
        Uses the __dict__ call to store ALL object attributes
        """
        with open(self.path(instance), 'w') as f:
            json.dump(self.__dict__, f)
