# #!/usr/bin/python3

# """
# This file defines the storage system for
# the project.
# It will use JSON format to either serialize and deserialize objects
# """

# import json
# from json.decoder import JSONDecodeError
# from .errors import *
# from models.base_model import BaseModel
# from models.user import User
# from models.state import State
# from models.city import City
# from models.amenity import Amenity
# from models.place import Place
# from models.review import Review
# from datetime import datetime


# class FileStorage:
#     """
#     This is  will serve as an Object relation mappingto interface or database
#     """

#     """class private varaibles"""
#     __objects: dict = {}
#     __file_path: str = 'file.json'
#     models = (
#             "BaseModel",
#             "User", "City", "State", "Place",
#             "Amenity", "Review"
#             )

#     def __init__(self):
#         """constructor"""
#         pass

#     def all(self):
#         """Return all instances stored"""
#         return FileStorage.__objects

#     def new(self, obj):
#         """Stores a new Object"""
#         key = "{}.{}".format(type(obj).__name__, obj.id)
#         FileStorage.__objects[key] = obj

#     def save(self):
#         """serializes objects stored and persist in file"""
#         serialized = {
#             key: val.to_dict()
#             for key, val in self.__objects.items()
#         }
#         with open(FileStorage.__file_path, "w") as f:
#             f.write(json.dumps(serialized))

#     def reload(self):
#         """de-serialize persisted objects"""
#         try:
#             deserialized = {}
#             with open(FileStorage.__file_path, "r") as f:
#                 deserialized = json.loads(f.read())
#             FileStorage.__objects = {
#                 key:
#                     eval(obj["__class__"])(**obj)
#                     for key, obj in deserialized.items()}
#         except (FileNotFoundError, JSONDecodeError):
#             # No need for error
#             pass

#     def find_by_id(self, model, obj_id):
#         """Find and return an elemt of model by its id"""
#         F = FileStorage
#         if model not in F.models:
#             # Invalid Model Name
#             # Not yet Implemented
#             raise ModelNotFoundError(model)

#         key = model + "." + obj_id
#         if key not in F.__objects:
#             # invalid id
#             # Not yet Implemented
#             raise InstanceNotFoundError(obj_id, model)

#         return F.__objects[key]

#     def delete_by_id(self, model, obj_id):
#         """Find and return an elemt of model by its id"""
#         F = FileStorage
#         if model not in F.models:
#             raise ModelNotFoundError(model)

#         key = model + "." + obj_id
#         if key not in F.__objects:
#             raise InstanceNotFoundError(obj_id, model)

#         del F.__objects[key]
#         self.save()

#     def find_all(self, model=""):
#         """Find all instances or instances of model"""
#         if model and model not in FileStorage.models:
#             raise ModelNotFoundError(model)
#         results = []
#         for key, val in FileStorage.__objects.items():
#             if key.startswith(model):
#                 results.append(str(val))
#         return results

#     def update_one(self, model, iid, field, value):
#         """Updates an instance"""
#         F = FileStorage
#         if model not in F.models:
#             raise ModelNotFoundError(model)

#         key = model + "." + iid
#         if key not in F.__objects:
#             raise InstanceNotFoundError(iid, model)
#         if field in ("id", "updated_at", "created_at"):
#             # not allowed to be updated
#             return
#         inst = F.__objects[key]
#         try:
#             # if instance has that value
#             # cast it to its type
#             vtype = type(inst.__dict__[field])
#             inst.__dict__[field] = vtype(value)
#         except KeyError:
#             # instance doesn't has the field
#             # assign the value with its type
#             inst.__dict__[field] = value
#         finally:
#             inst.updated_at = datetime.utcnow()
#             self.save()


#!/usr/bin/python3
'''AirBnB clone project File Storage'''
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ This is a storage engine for AirBnB clone project
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

    __file_path = 'file.json'
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}

    def all(self):
        '''Return dictionary of <class>.<id> : object instance'''
        return self.__objects

    def new(self, obj):
        '''Set new __objects to existing dictionary of instances'''
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Save/serialize obj dictionaries to json file"""
        obj_dict = {}

        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserialize/convert obj dicts back to instances, if it exists"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                new_obj_dict = json.load(f)
            for key, value in new_obj_dict.items():
                obj = self.class_dict[value['__class__']](**value)
                self.__objects[key] = obj
        except FileNotFoundError:
            pass