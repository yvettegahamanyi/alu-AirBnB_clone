#!/usr/bin/python3
"""
Definititon of state class
"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    Definition of  data describing state, it inherits from BaseModel class


    Variables:
        name (string): Users last name.
    """

    name = ""
