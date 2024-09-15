import json
import os
import configparser
projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(f"{projectRoot}/config.ini")

dataDir = config['Database']['data_directory']

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
        json.dump(data, f)
        
def _db_createDB(DBName):
    if not os.path.exists(dataDir):
        os.mkdir(dataDir)
    with open(f"{dataDir}/{DBName}.json", 'w') as f:
        f.write("{}")
        
        
        
# Functions to interact with the database
## Get a value from a key within the database
def db_getKey(DBName, key):
    data = _db_loadDB(DBName)
    return data.get(key)

## Set a value to a key within the database
def db_setKey(DBName, key, value):
    data = _db_loadDB(DBName)
    if key in data:
        data[key] = value
        _db_saveDB(DBName, data)
    else:
        print("Key does not exist in the database. Use db_addKey() to add a new key.")
    
## Add a value to a key within the database
def db_addKey(DBName, key, value):
    data = _db_loadDB(DBName)
    if key not in data:
        data[key] = value
        _db_saveDB(DBName, data)
    else:
        print("Key already exists in the database. Use db_setKey() to update the value.")
    
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