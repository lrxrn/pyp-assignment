import json
import os
import base64
import configparser
from Modules.functions import encode_password

projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(f"{projectRoot}/config.ini")

dataDir = config['Database']['data_directory']
adminUsername = config['Default']['admin_username']
adminPassword = config['Default']['admin_password']


# Internal load and save functions
def _db_loadDB(DBName):
    try:
        with open(f"{dataDir}/{DBName}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        _db_createDB(DBName)
        return {}
    
def _db_saveDB(DBName, data):
    with open(f"{dataDir}/{DBName}.json", 'w') as f:
        json.dump(data, f, indent=4)
        
def _db_createDB(DBName):
    if not os.path.exists(dataDir):
        os.mkdir(dataDir)
    with open(f"{dataDir}/{DBName}.json", 'w') as f:
        f.write("{}")
    if DBName == "users":
        if _db_loadDB("users") == {}: # If the users database is empty, add an admin user
            print("No users found. Adding default admin user.")
            db_addKey("users", adminUsername, {
                "name": "Admin User",
                "email": "admin@restaurant.com",
                "role": "administrator",
                "PhoneNumber": "+1234567890",
                "DOB": "10-May-1990",
                "Address": "Restaurant Address, City"
            })
            db_addKey("passwords", adminUsername, {"password": encode_password(adminPassword), "attempts": 0})
        
        
        
# Functions to interact with the database
## Get a value from a key within the database
def db_getKey(DBName, key):
    data = _db_loadDB(DBName)
    return data.get(key)

## Update a value in a key within the database
def db_updateKey(DBName, key, value):
    data = _db_loadDB(DBName)
    if key in data:
        data[key] = value
        _db_saveDB(DBName, data)
    else:
        db_addKey(DBName, key, value)
        
# Deprecated function; included for backwards compatibility
def db_setKey(DBName, key, value):
    db_updateKey(DBName, key, value)
    
## Add a value to a key within the database
def db_addKey(DBName, key, value):
    data = _db_loadDB(DBName)
    if key not in data:
        data[key] = value
        _db_saveDB(DBName, data)
    else:
        db_updateKey(DBName, key, value)
    
## Delete a key from the database
def db_deleteKey(DBName, key):
    data = _db_loadDB(DBName)
    if key in data:
        del data[key]
        _db_saveDB(DBName, data)
        
## Get all keys from the database
def db_getAllKeys(DBName):
    data = _db_loadDB(DBName)
    return list(data.keys())

## Get all values from the database
def db_getAllValues(DBName):
    data = _db_loadDB(DBName)
    return list(data.values())

## !! Clear the database
def db_clearDB(DBName):
    data = {}
    _db_saveDB(DBName, data)
    
    
# Save password after encrypting it
def db_savePassword(username, password, attempts=0):
    password = base64.b64encode(password.encode()).decode()
    db_updateKey("passwords", username, {"password": password, "attempts": attempts})