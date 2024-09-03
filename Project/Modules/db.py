import json
import base64
import os

dataDir = "Data"


class Database:
    # Constructor
    def __init__(self, name, options={}):
        if name is None:
            raise SyntaxError("Database name cannot be empty")
        self.name = name
        self.options = options
        self.dataDir = options.get("dataDir", dataDir)
        self.debug = options.get("debug", False)
        self.dir = os.path.join(f"{os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]}", f"{self.dataDir}")
        self.path = os.path.join(self.dir, f"{self.name}.json")
        self.data = {}

        # Load data from file
        self.load()

    # Function to print debug messages
    def printd(self, msg):
        if self.debug:
            print(f"[DB] {msg}")

    # Load data from file
    def load(self):
        self.printd(f"Initializing database {self.name}")

        # Check if db directory exists
        self.printd("Checking if Data directory exists")
        if not os.path.exists(self.dir):
            # Create db directory
            os.mkdir(self.dir)
        
        # Check if file exists
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
                pass
        except FileNotFoundError:
            self.printd(f"Database {self.name} not found. Creating new database file.")
            with open(self.path, "w") as f:
                f.write("{}")
        finally:
            self.printd(f"Database {self.name} loaded successfully")


    # Save data to file
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    # Get data
    def get(self, key):
        return self.data.get(key)

    # Add/ edit data
    def set(self, key, value):
        self.data[key] = value
        self.save()

    # Delete data
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save()

    # Permanently Erase Database
    def clear(self):
        self.data = {}
        self.save()

    # Return all keys
    def Allkeys(self):
        return list(self.data.keys())

    # Return all values
    def values(self):
        return self.data.values()



"""
class Database:
    def __init__(self, DBName, options):
        if DBName is None:
            raise ValueError("Database Name cannot be empty")
        
        self.debug = options["debug"] | False
        self.DBName = DBName.lower()
        self.path = f"{dataPath}/{self.DBName}.json"

        self.initDB()

    # Function to print debug messages
    def printd(self, msg):
        if self.debug:
            print(msg)

    # Function to see if the database file exists and create it if it doesn't
    def initDB(self):
        self.printd(f"Initializing database {self.DBName}")
        try:
            with open(self.path, "r") as f:
                pass
        except FileNotFoundError:
            self.printd(f"Database {self.DBName} not found. Creating new database file.")
            with open(self.path, "w") as f:
                f.write("{}")

    # password encrypt function
    def encrypt(unencrypted_password): 
        # base64 encode the password
        # Encode the password string to bytes
        byte_data = unencrypted_password.encode('utf-8')
        # Encode the bytes to base64 and convert the bytes back to a string
        password = base64.b64encode(byte_data).decode('utf-8')
        return password

    # password decrypt function
    def decrypt(encrypted_password):
        # base64 decode the password
        # Encode the base64 password string to bytes
        byte_data = encrypted_password.encode('utf-8')
        # Decode the bytes to base64 and convert the bytes back to a string
        password = base64.b64decode(byte_data).decode('utf-8')
        return password

    # function to read the users from the file and return a list of users
    def read_users(self):
        usersDB = []
        with open(self.usersDB_path, "r") as f:
            usersDB = f.readlines()
        usersDB = [user.strip() for user in usersDB]
        return usersDB

    # function to read the credentials from the file and return a dictionary of users and passwords
    def read_credentials(self):
        passwordsDB = {}
        with open(self.credentialsDB_path, "r") as f:
            passwordsDB = f.readlines()
        passwordsDB = [password.strip() for password in passwordsDB]
        passwordsDB = dict([[password.split(",")[0], self.decrypt(password.split(",")[2])] for password in passwordsDB])
        return passwordsDB

    # function to append a new user to the database
    def save_new_user(self, user, email, name, role, password):
        with open(self.usersDB_path, "a") as f:
            f.write(f"\n{user.lower()},{email.lower()},{name},{role.lower()}\n")

        with open(self.credentialsDB_path, "a") as f:
            f.write(f"\n{user.lower()},{password}")

    # def save_users(self):
    #     usersDB = self.read_users()
    #     with open(self.usersDB_path, "w") as f:
    #         for user in usersDB:
    #             f.write(f"{user},{usrEmailDB[user]},{usersDB[user]},{rolesDB[user]}\n")

    # def save_passwords(self):
    #     passwordsDB = self.read_credentials()
    #     with open(self.credentialsDB_path, "w") as f:
    #         for user in passwordsDB:
    #             if is_encrypted(passwordsDB[user]):
    #                 f.write(f"{user},{encrypt(passwordsDB[user])}\n")
    #             else:
    #                 f.write(f"{user},{passwordsDB[user]}\n")

    # function to save the updated user details and save it to the file
    def save_updated_user(self, usersDB):
        with open(self.usersDB_path, "w") as f:
            for rec in usersDB:
                f.write(f"{rec}")

    # function to save the updated password and save it to the file
    def save_password(self, passwordsDB):
        with open(self.credentialsDB_path, "w") as f:
            for rec in passwordsDB:
                f.write(f"{rec}")

    # function to update the user details
    def update_user(self, user, email=None, name=None, role=None):
        usersDB = self.read_users()
        if user in usersDB:
            index = usersDB.index(user)
            user_details = usersDB[index].split(",")
            if email:
                user_details[1] = email.lower()
            if name:
                user_details[2] = name
            if role:
                user_details[3] = role.lower()
            usersDB[index] = ",".join(user_details)
            self.save_updated_user(usersDB)
            return True
        else:
            return False
        
    # function to update the password
    def update_password(self, user, new_password):
        passwordsDB = self.read_credentials()
        if user in passwordsDB:
            passwordsDB[user] = new_password
            self.save_password(passwordsDB)
            return True
        else:
            return False
"""

'''
if __name__ == "__main__":
    db = Database("/path/to/json/files", "MyDatabase")
    data = db.get_data("example")
    print(data)
    print(db.get_name())
'''