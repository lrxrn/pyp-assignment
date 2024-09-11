import os
import tabulate
from Modules.db import db_getKey, db_setKey, db_deleteKey, db_getAllKeys
from Modules.functions import wait_for_enter, inp

#print(os.path.dirname(os.path.abspath(__file__)))

# Create a new database

while True:
  print("\n")
  print("Users Menu: \n1. Add User \n 2. Edit User\n3. Delete User \n4. Show Users \n5. Exit")
  ch = input("Enter your choice: ")
  match ch:
    case "1":
      print("ADD NEW USER")
      username = input("Enter username: ")
      if(db_getKey("users", username)):
        print("User already exists")
        wait_for_enter()
        continue
        
      email = input("Enter email: ")
      db_setKey("users", username, {"email": email})
      if(db_getKey("users", username)):
        print("User added successfully!")
      else:
        print("Error adding user!")
    case "2":
      print("EDIT USER")
      chTyp = input("Enter C to choose user from list or U to enter username: ")
      chTyp = chTyp.upper()
      match chTyp:
        case "C":
          print("Choose user from list")
          userList = db_getAllKeys("users")
          tableHeaders = ["No.", "Username"]
          tableData = []
          for i in range(len(userList)):
            tableData.append([i+1, userList[i]])
          table = tabulate.tabulate(tableData, headers=tableHeaders, tablefmt="grid")
          print(table)
          chUser = inp("Enter user number: ", "int")
          if(chUser > 0 and chUser <= len(userList)):
            usernametoEdit = userList[chUser-1]
            print(f"Editing user: {usernametoEdit}")
            wait_for_enter()
          else:
            print("Invalid user number!")
            
        case "U":
          usernametoEdit = input("Enter username: ")
          if(db_getKey("users", usernametoEdit)):
            print(f"Editing user: {usernametoEdit}")
          else:
            print("User not found!")
            wait_for_enter()
            continue
        case _:
          print("Invalid choice!")
          wait_for_enter()
          continue
          
    case "3":
      print("DELETE USER")
      username = input("Enter username: ")
      if(db_getKey("users", username)):
        db_deleteKey("users", username)
        print("User deleted successfully!")
      else:
        print("User does not exist!")
    case "4":
      print("SHOW USERS")
      userList = db_getAllKeys("users")
      # Make table using tabulate
      tableHeaders = ["No.", "Username"]
      tableData = []
      for i in range(len(userList)):
        tableData.append([i+1, userList[i]])
      table = tabulate.tabulate(tableData, headers=tableHeaders, tablefmt="grid")
      print(table)
      wait_for_enter()
    case "5":
      print("Exiting...")
      exit()
    case _:
      print("Invalid choice")
      wait_for_enter()