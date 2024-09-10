#!/usr/bin/python3
"""Project File Storage"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """storage engine for AirBnB clone project
    Class Methods:
        all: Returns the object
        new: updates the dictionary id
        save: Serializes, or converts Python objects into JSON strings
        reload: Deserializes, or converts JSON strings into Python objects.
    Class Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
        class_dict (dict): A dictionary of all the classes.
    """

    __objects = {}
    __file_path = 'file.json'
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "State": State, "City": City, "Amenity": Amenity,
                  "Review": Review}

    def all(self):
        """Return dictionary of <class>.<id> : object instance"""
        return type(self).__objects

    def new(self, obj):
        """set new __objects to existing dictionary of instances"""
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            type(self).__objects[key] = obj

    def save(self):
        """serialize/save obj dictionaries to json file"""
        obj_dict = {}

        for key, obj in type(self).__objects.items():
            obj_dict[key] = obj.to_dict()
        with open(type(self).__file_path, 'w', encoding="UTF-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """convert obj dicts back to instances, if it exists"""
        try:
            with open(type(self).__file_path, 'r', encoding="UTF-8") as f:
                new_obj_dict = json.load(f)
                for key, value in new_obj_dict.items():
                    obj = self.class_dict[value['__class__']](**value)
                    type(self).__objects[key] = obj
        except FileNotFoundError:
            pass
