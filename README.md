# PYP-assignment
This project includes the Python code for the assignment in the PYP module.

## Table of contents
* [Introduction](#pyp-assignment)
* [Technologies](#technologies)
* [File structure](#file-structure)
* [Database](#database)
    * [Overview of Database functions](#overview-of-database-functions)
* [Common functions](#common-functions)
    * [Overview of Common functions](#overview-of-common-functions)
* [Setup](#setup)

## Technologies
Project is created with:
* Python version: 3.12.x

## File structure
```ascii
Project/
├─ Modules/
│  ├─ db.py
│  ├─ functions.py
├─ Roles/
│  ├─ admin.py
│  ├─ manager.py
│  ├─ chef.py
│  ├─ customer.py
main.py
```

## Database
All database functions are in the `Modules/db.py` file.

#### Overview of Database functions
* **db_getKey(DBName, key)** - Get a value from a key in the database.
```
Parameters:
DBName (str): The Database name.
key (str): The key to get the value from.

Returns:
str: The value of the key.
```

* **db_setKey(DBName, key, value)** - Set a key with a value in the database.
```
Parameters:
DBName (str): The Database name.
key (str): The key to set the value to.
value (str): The value to set the key to.

Returns:
None -> The key is set in the database.
```

* **db_deleteKey(DBName, key)** - Delete a key from the database.
```
Parameters:
DBName (str): The Database name.
key (str): The key to delete.

Returns:
None -> The key is deleted from the database.
```

* **db_getAllKeys(DBName)** - Get all keys in the database.
```
Parameters:
DBName (str): The Database name.

Returns:
list: A list of all keys in the database.
```

* **db_getAllValues(DBName)** - Get all values in the database.
```
Parameters:
DBName (str): The Database name.

Returns:
list: A list of all values in the database.
```

## Common functions
All common functions are in the `Modules/functions.py` file.

#### Overview of Common functions
* **clear_console(wait_time=None)** - Clear the console to de-clutter it.
```
Parameters:
wait_time (float, optional): Time to wait before clearing the console.

Returns:
None -> The console is cleared.
```

* **wait_for_enter(msg="Press Enter to proceed...", clear=False)** - Wait for the user to press Enter.
```
Parameters:
msg (str, optional): Message to display to the user.
clear (bool, optional): Whether to clear the console after pressing Enter.

Returns:
None -> Waits for user input.
```

* **generate_id(name, category)** - Generate a unique ID based on the item name and category.
```
Parameters:
name (str): The name of the menu item.
category (str): The category of the menu item.

Returns:
str: A unique ID generated from the name and category.
```

* **display_table(headers, data)** - Display a table with headers and data.
```
Parameters:
headers (list): List of column headers.
data (list): List of rows, where each row is a list of values.

Returns:
None -> Displays the table.
```

* **inp(msg="Input your value: ", type="str")** - Input function with type validation.
```
Parameters:
msg (str, optional): Message to display to the user.
type (str, optional): Type of input to validate ('int', 'float', 'email', 'str').

Returns:
various: The validated input value.
```

## Setup
To run this project, clone the repository and run the `main.py` file.
```sh
$ git clone
```
```sh
$ cd PYP-assignment
```
```sh
$ python main.py
```