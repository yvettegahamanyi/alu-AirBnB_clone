import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.engine.errors import ModelNotFoundError, InstanceNotFoundError
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class TestConsole(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        storage.reset()  # Assuming there is a method to reset the storage before each test

    def tearDown(self):
        """Tear down test environment"""
        storage.reset()

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))
    
    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("quit"))
    
    def test_create_missing_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")
    
    def test_create_invalid_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")
    
    def test_create_valid_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            output = f.getvalue().strip()
            self.assertTrue(len(output) > 0)
            self.assertTrue(output in storage.all(BaseModel).keys())
    
    def test_show_missing_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")
    
    def test_show_missing_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")
    
    def test_show_invalid_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show InvalidClass 1234")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")
    
    def test_show_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 1234")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")
    
    def test_show_valid_instance(self):
        with patch('sys.stdout', new=StringIO()) as f:
            instance = BaseModel()
            instance.save()
            HBNBCommand().onecmd(f"show BaseModel {instance.id}")
            self.assertIn(instance.id, f.getvalue().strip())
    
    def test_destroy_missing_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")
    
    def test_destroy_missing_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")
    
    def test_destroy_invalid_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy InvalidClass 1234")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")
    
    def test_destroy_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 1234")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")
    
    def test_destroy_valid_instance(self):
        instance = BaseModel()
        instance.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"destroy BaseModel {instance.id}")
            self.assertNotIn(instance.id, storage.all(BaseModel))
    
    def test_all_no_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            self.assertEqual(f.getvalue().strip(), "[]")
    
    def test_all_invalid_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")
    
    def test_all_valid_class(self):
        instance = BaseModel()
        instance.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel")
            self.assertIn(instance.id, f.getvalue().strip())
    
    def test_update_missing_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")
    
    def test_update_missing_id(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")
    
    def test_update_missing_attribute(self):
        instance = BaseModel()
        instance.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update BaseModel {instance.id}")
            self.assertEqual(f.getvalue().strip(), "** attribute name missing **")
    
    def test_update_missing_value(self):
        instance = BaseModel()
        instance.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update BaseModel {instance.id} name")
            self.assertEqual(f.getvalue().strip(), "** value missing **")
    
    def test_update_valid_instance(self):
        instance = BaseModel()
        instance.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update BaseModel {instance.id} name 'MyModel'")
            updated_instance = storage.find_by_id("BaseModel", instance.id)
            self.assertEqual(updated_instance.name, 'MyModel')
    
    def test_models(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("models")
            self.assertIn("BaseModel", f.getvalue().strip())
    
    def test_handle_class_methods_invalid_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("InvalidClass.all()")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")
    
    def test_handle_class_methods_valid_all(self):
        instance = BaseModel()
        instance.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.all()")
            self.assertIn(instance.id, f.getvalue().strip())
    
    def test_handle_class_methods_valid_show(self):
        instance = BaseModel()
        instance.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"BaseModel.show('{instance.id}')")
            self.assertIn(instance.id, f.getvalue().strip())
    
    def test_handle_class_methods_invalid_method(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.invalid_method()")
            self.assertEqual(f.getvalue().strip(), "** invalid method **")
    
    def test_emptyline(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual(f.getvalue().strip(), "")


if __name__ == "__main__":
    unittest.main()
