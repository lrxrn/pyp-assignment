import json
import os

dataDir = "data"

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
    data[key] = value
    _db_saveDB(DBName, data)
    
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