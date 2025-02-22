#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        obj_dict = FileStorage.__objects
        if cls is not None:
            cls_dic = {key: obj for key, obj in obj_dict.items() if isinstance(obj, cls)}
            return cls_dic
        return obj_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    class_name = value['__class__']
                    self.__objects[key] = eval(class_name)(**value)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # If the file doesn't exist or is empty, do nothing

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()

