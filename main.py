# Import the core modules
import os
import time
import base64
import re

# Import the modules
from Modules.db import db_addKey, db_getKey, db_updateKey, db_getAllKeys, db_getAllValues, db_deleteKey, db_savePassword
from Modules.functions import clear_console, inp, wait_for_enter, printD, generate_password

# Import the roles
from Roles.admin import start as admin_menu
from Roles.manager import start as manager_menu
from Roles.chef import start as chef_menu
from Roles.customer import start as customer_menu

# Logout function
def logout(usr=None):
    print("\n")
    if usr:
        printD(f"Logout. Goodbye {usr}.", "pink")
    else:
        printD("Logging out.", "pink")
    clear_console(2)
    main_start()

def update_profile(username, admin_username=None, choice=None, return_func=None):
    clear_console()
    global admin_privileges
    admin_privileges = False
    if admin_username:
        admin_user_data = db_getKey("users", admin_username)
        if admin_user_data:
            admin_privileges = admin_user_data['role'] == "administrator"
    else:
        admin_privileges = False
    
    printD("Update Profile", "cyan")
    print("-"*35)
    print(f"Username: {username}")
    if choice is None:
        user_data = db_getKey("users", username)
        print(f"Name: {user_data['name']}")
        print(f"Email: {user_data['email']}")
        print(f"Phone Number: {user_data['PhoneNumber']}")
        print(f"Date of Birth: {user_data['DOB']}")
        print(f"Address: {user_data['Address']}")
        if admin_privileges:
            print("1. Update Name \n2. Update Email \n3. Update Phone Number \n4. Update Address \n5. Update Password \n6. Update Role \n7. Go Back to Main Menu")
            ch = inp("Enter your choice: ", "int", [1, 2, 3, 4, 5, 6])
        else:
            print("1. Update Name \n2. Update Email \n3. Update Phone Number \n4. Update Address \n5. Update Password \n6. Go Back to Main Menu")
            ch = inp("Enter your choice: ", "int", [1, 2, 3, 4, 5])
    else:
        ch = choice
  

    match ch:
        case 1:
            new_name = input("Enter new name: ").strip()
            user_data['name'] = new_name
            db_updateKey("users", username, user_data)
            printD("Name updated successfully.", "green")
        case 2:
            new_email = inp("Enter new email: ", "email")
            user_data['email'] = new_email
            db_updateKey("users", username, user_data)
            printD("Email updated successfully.", "green")
        case 3:
            new_phone = inp("Enter new phone number: ", "phone")
            user_data['PhoneNumber'] = new_phone
            db_updateKey("users", username, user_data)
            printD("Phone number updated successfully.", "green")
        case 4:
            new_address = input("Enter new address: ").strip()
            user_data['Address'] = new_address
            db_updateKey("users", username, user_data)
            printD("Address updated successfully.", "green")
        case 5:
            current_password = base64.b64decode(db_getKey("passwords", username)['password']).decode()
            inp_password = inp("Enter current password: ", "str")
            if inp_password != current_password:
                printD("Invalid password.", "red")
                print("1. Try again  \n2. Forgot Password \n3. Go Back to Main Menu")
                ch = inp("Enter your choice: ", "int", [1, 2, 3])
                match ch:
                    case 1:
                        update_profile(username, None, 5)
                    case 2:
                        reset_password(username)
                    case 3:
                        main_menu(username, user_data['role'])
            new_password = inp("Enter new password: ", "password")
            new_password_confirm = inp("Confirm new password: ", "password")
            if new_password != new_password_confirm:
                printD("Passwords do not match. Please try again.", "yellow")
                wait_for_enter("Press Enter to go back to the main menu.", True)
                main_menu(username, user_data['role'])
            password_data = {
                "password": base64.b64encode(new_password.encode()),
                "attempts": 0
            }
            db_updateKey("passwords", username, password_data)
            printD("Password updated successfully.", "green")
        case 6:
            if admin_privileges:
                print("1. Customer \n2. Chef \n3. Manager \n4. Administrator")
                new_role = inp("Enter new role: ", "int", [1, 2, 3, 4])
                roles = ["customer", "chef", "manager", "administrator"]
                user_data['role'] = roles[new_role - 1]
                db_updateKey("users", username, user_data)
                printD("Role updated successfully.", "green")
            else:
                printD("Invalid choice. Please try again.", "yellow")
        case _:
            wait_for_enter("Press Enter to go back to the main menu.", True)
            main_menu(username, user_data['role'])
        
    if return_func:
        return_func()
    else:
        wait_for_enter("Press Enter to go back to the main menu.", True)
        main_menu(username, user_data['role'])
            
        
def main_menu(username, role:str):
    role = role.strip().lower()
    match role:
        case "customer":
            print("You are a Customer. Choose an option:")
            print("1. Continue as Customer")
            print("2. Logout")
            ch = inp("Enter your choice: ", "int", [1, 2])
            match ch:
                case 1:
                    clear_console(2)
                    customer_menu(username)
                case _:
                    logout(username)
        case "chef":
            print("You are a Chef. Choose an option:")
            print("1. Continue as Chef")
            print("2. Continue as a Customer")
            print("3. Logout")
            ch = inp("Enter your choice: ", "int", [1, 2, 3])
            match ch:
                case 1:
                    clear_console(2)
                    chef_menu(username)
                case 2:
                    clear_console(2)
                    customer_menu(username)
                case _:
                    logout(username)
        case "manager":
            print("You are a Manager. Choose an option:")
            print("1. Continue as Manager")
            print("2. Continue as a Customer")
            print("3. Logout")
            ch = inp("Enter your choice: ", "int", [1, 2, 3])
            match ch:
                case 1:
                    clear_console(2)
                    manager_menu(username)
                case 2:
                    clear_console(2)
                    customer_menu(username)
                case _:
                    logout(username)
        case "administrator":
            print("You are an Adminstrator. Choose an option:")
            print("1. Continue as Admin")
            print("2. Continue as a Customer")
            print("3. Logout")
            ch = inp("Enter your choice: ", "int", [1, 2, 3])
            match ch:
                case 1:
                    clear_console(2)
                    admin_menu(username)
                case 2:
                    clear_console(2)
                    customer_menu(username)
                case _:
                    logout(username)
        case _:
            printD("Invalid role. Please contact the administrator.", "red")
            logout()
            
def reset_password(usr=None):
    clear_console()
    printD("Reset Password", "cyan")
    print("-"*35)
    if usr:
        username = usr
    else:
        username = input("Enter your username: ").strip().lower()
    if not db_getKey("users", username):
        printD("Username not found.", "yellow")
        wait_for_enter("Press Enter to go back to the main screen.", True)
        main_start()
        return
    else:
        print(f"Hi, {username}. \nBefore resetting your password, we need to verify your identity.")
        print("1. Email Verification \n2. Phone Verification \n3. Cancel")
        ch = inp("Enter your choice: ", "int", [1, 2, 3])
        match ch:
            case 1:
                email = db_getKey("users", username)["email"]
                print("Please enter your email address to verify your identity.")
                user_input = inp("Enter your email: ", "email")
                if user_input == email:
                    printD("Identity verified.", "green")
                    new_password = inp("Enter new password: ", "password")
                    new_password_confirm = inp("Confirm new password: ", "password")
                    if new_password != new_password_confirm:
                        printD("Passwords do not match. Please try again.", "yellow")
                        wait_for_enter("Press Enter to go back to the main screen.", True)
                        main_start()
                        return
                    db_savePassword(username, new_password)
                    printD("Password reset successful.", "green")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_start()
                else:
                    printD("Email is not the valid email on file.", "yellow")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_start()
            case 2:
                phone = db_getKey("users", username)["PhoneNumber"]
                print("Please enter your phone number to verify your identity.")
                user_input = inp("Enter your phone number: ", "int")
                if user_input == phone:
                    printD("Identity verified.", "green")
                    new_password = inp("Enter new password: ", "password")
                    new_password_confirm = inp("Confirm new password: ", "password")
                    if new_password != new_password_confirm:
                        printD("Passwords do not match. Please try again.", "yellow")
                        wait_for_enter("Press Enter to go back to the main screen.", True)
                        main_start()
                        return
                    db_savePassword(username, new_password)
                    printD("Password reset successful.", "green")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_start()
                else:
                    printD("Phone number is not the valid number on file.", "yellow")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_start()
            case 3:
                print("Cancelling...")
                main_start()
            
def register(staff_username=None, return_func=None):
    clear_console()
    printD("Registration", "cyan")
    print("-"*35)
    global staff_privileges
    staff_privileges = "customer"
    if staff_username:
        staff_privileges = db_getKey("users", staff_username)['role']
        print(f"Hi, {staff_username} [{staff_privileges}].")
        print("Please enter the details of the new user.")
    inp_name = input("Name?: ").strip()
    inp_email = inp("Email address?: ", "email")
    inp_phone = inp("Phone number? (International format): ", "phone")
    inp_dob = inp("Date of Birth (DD-MMM-YYYY): ", "date")
    inp_address = input("Address: ").strip()
    while True:
        inp_username = input("Enter a username (Note: Username is not changeable): ").strip().lower()
        if re.search(r"\W", inp_username):
            printD("Username should not contain any special characters.", "yellow")
            continue
        if len(inp_username) < 4:
            printD("Username should be at least 4 characters long.", "yellow")
            continue
        if db_getKey("users", inp_username):
            printD("Username already exists.", "yellow")
            continue
        break
    
    global inp_role, inp_password
    inp_role = "customer"
    if staff_privileges == "customer": 
        while True:
            inp_password = inp("Enter password: ", "password")
            inp_password_confirm = inp("Confirm password: ", "password")
            if inp_password != inp_password_confirm:
                printD("Passwords do not match. Please try again.", "yellow")
                continue
            break
    else:
        inp_password = generate_password()
        
    if staff_privileges == "administrator":
        inp_role = inp("Role? (manager, chef, customer): ", "str", ["manager", "chef", "customer"])
        
    
    global user_data, password_data
    user_data = {
        "name": inp_name,
        "email": inp_email,
        "role": inp_role,
        "PhoneNumber": inp_phone,
        "DOB": inp_dob,
        "Address": inp_address
    }
    password_data = {
        "password": base64.b64encode(inp_password.encode()).decode(),
        "attempts": 0
    }
    if db_getKey("users", inp_username):
        printD("Username already exists.", "yellow")
        wait_for_enter("Press Enter to go back.", True)
        return_func(staff_username)
        return
    else:
        printD(f"Username: {inp_username}\nPassword: {inp_password} \nRole: {inp_role}", "green")
        printD("Please note down the username and password for future reference.", "green")
        ch = inp("Do you want to continue registering? (y/n): ", "str", ["y", "n"])
        match ch:
            case "y":    
                db_addKey("users", inp_username, user_data)
                db_addKey("passwords", inp_username, password_data)
                printD("Registration successful.", "green")
                wait_for_enter("Press Enter to go back.", True)
                return_func(staff_username)
            case "n":
                printD("Registration cancelled.", "yellow")
                wait_for_enter("Press Enter to go back.", True)
                return_func(staff_username)

def login(usr=None):
    clear_console()
    printD("Login to continue.", "cyan")
    if usr:
        inp_username = usr
    else:
        inp_username = input("Enter username: ").strip().lower()

    # Check if the username is in the database
    usersList = db_getAllKeys("users")
    if inp_username in usersList:
        printD(f"Hi, {inp_username}.", "white", True)
        user_data = dict(db_getKey("users", inp_username))
        # check if the user has a password
        user_password_data = db_getKey("passwords", inp_username)
        if not user_password_data:
            printD("Password not set. Please contact an administrator to reset your password.", "red")
            wait_for_enter("Press Enter to go back to the main screen.", True)
            main_start()
            
        # check if the attempts is greater than or equal to 3, dont let user login if so
        if user_password_data['attempts'] >= 3:
            printD("You have exceeded the maximum number of login attempts. Please reset your password to unlock your account.", "red")
            print("1. Reset Password \n2. Go Back to Main Menu")
            ch = inp("Enter your choice: ", "int", [1, 2])
            match ch:
                case 1:
                    reset_password(inp_username)
                case 2:
                    main_start()
        else:
            user_password = base64.b64decode(user_password_data['password']).decode()
            inp_password = input("Enter password: ").strip()
            if inp_password == user_password:
                user_password_data['attempts'] = 0
                db_updateKey("passwords", inp_username, user_password_data)
                clear_console(1)
                printD(f"Welcome Back, {user_data['name']} [{inp_username}]!", "white", True)
                main_menu(inp_username, user_data['role'])
            elif inp_password == "":
                printD("Please enter a password.", "red")
                printD(f"Login attempts remaining: {3 - user_password_data['attempts']}", "red", True)
                print("Forgot password? \n 1. Reset Password \n 2. Try Again \n 3. Go Back to Main Menu")
                ch = inp("Enter your choice: ", "int", [1, 2, 3])
                match ch:
                    case 1:
                        reset_password(inp_username)
                    case 2:
                        login(inp_username)
                    case 3:
                        main_start()
            else:
                clear_console()
                printD("Invalid password.", "red")
                user_password_data['attempts'] += 1
                db_updateKey("passwords", inp_username, user_password_data)
                printD(f"Login attempts remaining: {3 - user_password_data['attempts']}", "red", True)
                print("Forgot password? \n 1. Reset Password \n 2. Try Again \n 3. Go Back to Main Menu")
                ch = inp("Enter your choice: ", "int", [1, 2, 3])
                match ch:
                    case 1:
                        reset_password(inp_username)
                    case 2:
                        login(inp_username)
                    case 3:
                        main_start()
    else:
        printD("Username not found.", "red")
        wait_for_enter("Press Enter to go back to the main screen.", True)
        main_start()

def main_start():
    clear_console()
    # Load the users database to run the pre-check and add the default admin user if not present
    usersList = db_getAllKeys("users")
    printD("Welcome to the Restaurant Management System.", "cyan", True)
    print("1. Login \n2. Register \n3. Reset Password \n4. Exit")
    ch = inp("Enter your choice: ", "int", [1, 2, 3, 4])
    match ch:
        case 1:
            login()
        case 2:
            register(None, main_start)
        case 3:
            reset_password()
        case 4:
            print("Exiting...")
            exit()
        case _:
            print("Invalid choice. Please try again.")
            clear_console(5)
            main_start()

if __name__ == "__main__":
    try:
        main_start()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")