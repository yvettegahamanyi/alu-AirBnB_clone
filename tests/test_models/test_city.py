#!/usr/bin/python3
# Tests for class city
import unittest
from models.city import City


class TestCity(unittest.TestCase):
    def test_attributes(self):
        city = City()
        self.assertTrue(hasattr(city, 'id'))
        self.assertTrue(hasattr(city, 'created_at'))
        self.assertTrue(hasattr(city, 'updated_at'))
        self.assertTrue(hasattr(city, 'name'))

    def test_name_default_value(self):
        city = City()
        self.assertEqual(city.name, "")
        self.assertEqual(city.state_id, "")

    def test_name_assignment(self):
        city = City()
        city.name = "Kigali"
        city.state_id = "75643"
        self.assertEqual(city.name, "Kigali")
        self.assertEqual(city.state_id, "75643")


if __name__ == '__main__':
    unittest.main()
