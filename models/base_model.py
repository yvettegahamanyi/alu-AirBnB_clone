#!/usr/bin/python3
# module that Defines the BaseModel Class
from uuid import uuid4
from datetime import datetime
import models

"""Parent class for all other classes in AirBnB Project"""


class BaseModel():
    """Parent class for all other classes in AirBnB Project
    Methods:
        __init__(self)
        __str__(self)
        __save(self)
        __repr__(self)
        to_dict(self)
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization method, called each time an instance is created.
        Initialization attributes: uuid4, dates when class was updated/created
        """
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for key, value in kwargs.items():
                if "created_at" == key:
                    self.created_at = datetime.strptime(kwargs["created_at"],
                                                        date_format)
                elif "updated_at" == key:
                    self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                        date_format)
                elif "__class__" == key:
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Method to set the string representation of BaseModel object.
        Return the class name, id and the dictionary
        """
        return ('[{}] ({}) {}'.
                format(self.__class__.__name__, self.id, self.__dict__))

    def __repr__(self):
        """returns string repr"""
        return (self.__str__())

    def save(self):
        """
        - Updates the public attribute `updated_at` with the current time
        -
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns the dictionary of the BaseModel with string formats of time,
        A dictionary containing all the keys/value of __dict__ method of
        the instance. A key __class__ is added to this dictionary with the
        class name of the object
        """
        result = self.__dict__.copy()
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["__class__"] = self.__class__.__name__
        return result
