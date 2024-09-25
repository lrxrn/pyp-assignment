import re
import base64

from Modules.db import db_addKey, db_deleteKey, db_updateKey, db_getKey, db_getAllKeys, db_getAllValues
from Modules.functions import clear_console, inp, printD, wait_for_enter, generate_password

def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)
    
def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)
    
def start(cur_usr):
    print("-"*35)
    print("Administrator Menu")
    print("-"*35)
    print("1. Manage staff")
    print("2. View sales report")
    print("3. View feedback")
    print("4. Update profile")
    print("5. Logout")
    print("-"*35)
    ch = inp("Enter your choice: ", "int", [1, 2, 3, 4, 5])
    match ch:
        case 1:
            manageStaff(cur_usr)
        case 2:
            viewSalesReport()
        case 3:
            viewFeedback()
        case 4:
            update_profile(cur_usr, start)
        case 5:
            logout(cur_usr)


def manageStaff(cur_usr):
    print("-"*35)
    print("Admin: Manage Staff")
    print("-"*35)
    print("1. Add staff")
    print("2. Remove staff")
    print("3. Update staff")
    print("4. View staff")
    print("5. Back")
    print("-"*35)
    ch = inp("Enter your choice: ", "int", [1, 2, 3, 4, 5])
    match ch:
        case 1:
            manageStaff_addStaff(cur_usr)
        case 2:
            manageStaff_removeStaff(cur_usr)
        case 3:
            manageStaff_updateStaff(cur_usr)
        case 4:
            manageStaff_viewStaff(cur_usr)
        case 5:
            start(cur_usr)

def manageStaff_addStaff(cur_usr):
    clear_console()
    from main import register as register_main
    register_main(cur_usr, manageStaff)

def manageStaff_removeStaff():
    print("Enter the username of the staff to be removed.")
    username = input("Enter the username: ")
    if username in usersDB:
        del usersDB[username]
        del emailsDB[emailsDB[username]]
        del rolesDB[username]
        save_users()
    else:
        print("User not found. Please try again.")
        clear_console(2)

def manageStaff_viewStaff():
    print("Staff list:")
    print("-"*50)
    print("Name [Username] - Email - Role")
    print("-"*50)
    for user in usersDB:
        print(f"{usersDB[user]} [{user}] - {usrEmailDB[user]} - {rolesDB[user]}")
    print("-"*50)
    wait(10)
