#!/usr/bin/python3
"""
This file defines the console class which will
serve as the entry point of the entire project
"""

from cmd import Cmd
from models import storage
from models.engine.errors import *
import shlex
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


# Global variable of registered models
# classes = storage.models
classes = {
    "State": State,
    "City": City,
    "Place": Place,
    "User": User,
    "Review": Review,
    "Amenity": Amenity,
}


class HBNBCommand(Cmd):
    """
    The Console based driver of the AirBnb Clone
    All interactions with the system is done via
    this class"""

    prompt = "(hbnb) "

    """Commands"""
    def do_EOF(self, args):
        """Exit the programme in non-interactive mode"""
        return True

    def do_quit(self, args):
        """Quit command exit the program"""
        return True

    def do_create(self, args):
        """Create an instance of Model and optionally pass attributes in key=value format.
        Example:
        $ create State name="California"
        """
        args, n = parse(args)  # Assuming parse splits the command arguments

        if not n:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return

        # Create a new instance of the given class
        obj_class = classes[args[0]]
        new_instance = obj_class()

        # If there are additional arguments (key=value pairs), set the attributes
        if n > 1:
            for arg in args[1:]:
                if "=" in arg:
                    key, value = arg.split("=", 1)

                    # Strip quotes from the value if provided (e.g., name="California")
                    value = value.strip('"').strip("'")

                    # Only set the attribute if it exists on the class
                    if hasattr(new_instance, key):
                        setattr(new_instance, key, value)
                    else:
                        print(f"** attribute '{key}' is not valid for {args[0]} **")
                        return

        # Save the instance and show its id
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show an Instance of Model base on its ModelName and id
        Example:
        $ show MyModel instance_id"""
        args, n = parse(arg)

        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                inst = storage.find_by_id(*args)
                print(inst)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for show **")
            pass

    def do_destroy(self, arg):
        """Deletes an Instance of Model base on its ModelName and id."""
        args, n = parse(arg)

        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                storage.delete_by_id(*args)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for destroy **")
            pass

    def do_all(self, args):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        args, n = parse(args)

        if n < 2:
            try:
                print(storage.find_all(*args))
            except ModelNotFoundError:
                print("** class doesn't exist **")
        else:
            print("** Too many argument for all **")
            pass

    def do_update(self, arg):
        """Updates an instance base on its id eg
        $ update Model id field value
        Throws errors for missing arguments"""
        args, n = parse(arg)
        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            print("** attribute name missing **")
        elif n == 3:
            print("** value missing **")
        else:
            try:
                storage.update_one(*args[0:4])
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")

    def do_models(self, arg):
        """Print all registered Models"""
        print(*classes)

    def handle_class_methods(self, arg):
        """Handle Class Methods
        <cls>.all(), <cls>.show() etc
        """

        printable = ("all(", "show(", "count(", "create(")
        try:
            val = eval(arg)
            for x in printable:
                if x in arg:
                    print(val)
                    break
            return
        except AttributeError:
            print("** invalid method **")
        except InstanceNotFoundError:
            print("** no instance found **")
        except TypeError as te:
            field = te.args[0].split()[-1].replace("_", " ")
            field = field.strip("'")
            print(f"** {field} missing **")
        except Exception as e:
            print("** invalid syntax **")
            pass

    def default(self, arg):
        """Override default method to handle class methods"""
        if '.' in arg and arg[-1] == ')':
            if arg.split('.')[0] not in classes:
                print("** class doesn't exist **")
                return
            return self.handle_class_methods(arg)
        return Cmd.default(self, arg)

    def emptyline(self):
        """Override empty line to do nothing"""
        return


def parse(line: str):
    """splits a line by spaces"""
    args = shlex.split(line)
    return args, len(args)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
