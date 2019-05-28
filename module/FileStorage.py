import json
import random
import string
import os


class FileStorage:
    def __init__(self, directory_name=None, forbidden_instances=()):
        self.directory_name = directory_name
        if directory_name is None:
            self.generate_directory_name()

            while os.path.exists(self.directory_name):
                self.generate_directory_name()
        os.mkdir(self.directory_name)

        self.pre_defined_forbidden = FileStorage,  # comma is not a mistake.
        self.forbidden_instances = self.pre_defined_forbidden + forbidden_instances

    def generate_directory_name(self, length=15):
        """Generating a random directory name """
        letters = string.ascii_letters
        directory_name = ""

        for x in range(length):
            directory_name += random.choice(letters)
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

    def clean_instance(self, instance):
        entry = instance.__dict__
        cleaned_entry = dict()

        for k, v in entry.items():
            if not isinstance(v, self.forbidden_instances):
                cleaned_entry[k] = v
        return cleaned_entry

    def set_file_content(self, instance):
        """ Setting the content from a grid file in file object.
        Using the native json.dump function to store it in a JSON string.
        Uses the __dict__ call to store ALL object attributes
        """
        with open(self.path(instance), 'w') as f:
            json.dump(self.clean_instance(instance), f)

    def delete_folder(self):
        """ Clears the directory that's been created to store the files """
        import shutil
        shutil.rmtree(self.directory_name)
