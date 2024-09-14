# AirBnB clone
Airbnb is a platform, where travellers can find and book short-term rentals all over the world

## The console
- After cloning run the console file `$ ./console.py` to se the magic
- create your data model `User, State, Place, Review, Amenity`
- manage (create, update, destroy, etc) objects via a console / command interpreter
- store and persist objects to a file (JSON file)

## Supported commands:
- **Create object** :

    `create <ClassName> <key1>=<value1> <key2>=<value2>...`
    Example: `create User name="John" age=30`


- **Show an Object**:

    `show <ClassName> <uuid>`

    Example: `show User abi8..`


- **Update an Object**:

    `update <ClassName> <id> <attribute_name>="<new_value>"`

    Example: `update User 123 name="Jane"`


- **List All Objects**:

    `all <ClassName>`

    Example: `all State`


- **Delete an Object**:

    `destroy <ClassName> <id>`

    Example: `destroy User adb9..`


- **Exit the Console**:

    Use `quit` or `EOD` to exit the console
