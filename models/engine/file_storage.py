#!/usr/bin/python3
"""
Contains the FileStorage class
"""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """
    Represents a file storage engine using JSON file
    """
    __file_path = "file.json"
    __objects = {}


    def all(self, cls=None):
        """
        Returns a dictionary of objects of a specific class or all classes
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects


    def new(self, obj):
        """
        Adds the object to the objects dictionary
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj


    def save(self):
        """
        Serializes objects to the JSON file
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)


    def reload(self):
        """
        Deserializes the JSON file to objects
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass


    def delete(self, obj=None):
        """
        Deletes obj from the objects dictionary if it exists
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]


    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects
        """
        self.reload()


    def get(self, cls, id):
        """
        Retrieves one object based on class and ID
        """
        objs = self.all(cls)
        for obj_id, obj in objs.items():
            if obj.id == id:
                return obj
        return None


    def count(self, cls=None):
        """
        Counts the number of objects in storage matching the given class
        """
        objs = self.all(cls)
        return len(objs)
