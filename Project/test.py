import os
import tabulate
from Modules.db import Database
from Modules.functions import wait_for_enter, inp

#print(os.path.dirname(os.path.abspath(__file__)))

# Create a new test database
userDB = Database("users", { "debug": True })


while True:
  print("\n")
  print("Users Menu: \n1. Add User \n 2. Edit User\n3. Delete User \n4. Show Users \n5. Exit")
  ch = input("Enter your choice: ")
  match ch:
    case "1":
      print("ADD NEW USER")
      username = input("Enter username: ")
      if(userDB.get(username)):
        print("User already exists")
        wait_for_enter()
        continue
        
      email = input("Enter email: ")
      userDB.set(username, {"email": email})
      if(userDB.get(username)):
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
          userList = userDB.Allkeys()
          tableHeaders = ["No.", "Username"]
          tableData = []
          for i in range(len(userList)):
            tableData.append([i+1, userDB.Allkeys()[i]])
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
          if(userDB.get(usernametoEdit)):
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
      if(userDB.get(username)):
        userDB.delete(username)
        print("User deleted successfully!")
      else:
        print("User does not exist!")
    case "4":
      print("SHOW USERS")
      # Make table using tabulate
      tableHeaders = ["No.", "Username"]
      tableData = []
      for i in range(len(userDB.Allkeys())):
        tableData.append([i+1, userDB.Allkeys()[i]])
      table = tabulate.tabulate(tableData, headers=tableHeaders, tablefmt="grid")
      print(table)
      wait_for_enter()
    case "5":
      print("Exiting...")
      exit()
    case _:
      print("Invalid choice")
      wait_for_enter()