#!/usr/bin/python3
# test module for class user
import unittest
from models.base_model import BaseModel
from models.user import User
from datetime import datetime, timedelta


class TestUser(unittest.TestCase):
    # Test for the User class

    def test_inheritance(self):
        user = User()
        self.assertIsInstance(user, BaseModel)

    def test_attributes(self):
        # tests instantiation of attributes
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_attribute_assignment(self):
        # tests if attributes as required
        user = User()
        user.email = "johndoe@alx.com"
        user.password = "password"
        user.first_name = "John"
        user.last_name = "Doe"
        self.assertEqual(user.email, "johndoe@alx.com")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_to_dict(self):
        # tests the to_dict method specified in BaseModel
        user = User()
        user.email = "johndoe@alx.com"
        user.password = "password"
        user.first_name = "John"
        user.last_name = "Doe"
        user_dict = user.to_dict()
        self.assertEqual(user_dict["email"], "johndoe@alx.com")
        self.assertEqual(user_dict["password"], "password")
        self.assertEqual(user_dict["first_name"], "John")
        self.assertEqual(user_dict["last_name"], "Doe")
        self.assertEqual(user_dict["__class__"], "User")

    def setUp(self):
        # test the __str__ method specified in BaseModel
        self.user = User()
        self.user.id = "1995"
        self.user.email = "johndoe@alx.com"
        self.user.password = "password"
        self.user.first_name = "John"
        self.user.last_name = "Doe"

    def test_save_method_updates_updated_at(self):
        # Get the initial updated_at value
        initial_updated_at = self.user.updated_at

        # Wait for a short period to ensure there is a time difference
        # between the initial_updated_at and the updated_at after save
        # (simulate a delay)
        time_difference = timedelta(seconds=1)
        new_updated_at = datetime.now() + time_difference
        self.user.updated_at = new_updated_at

        # Call the save method
        self.user.save()

        # Check if the updated_at attribute has been updated
        self.assertNotEqual(self.user.updated_at, new_updated_at)
        self.assertNotEqual(self.user.updated_at, initial_updated_at)


if __name__ == '__main__':
    unittest.main()
