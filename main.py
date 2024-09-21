# Import the core modules
import os
import time
import base64
import re

# Import the modules
from Modules.db import db_addKey, db_getKey, db_updateKey, db_getAllKeys, db_getAllValues, db_deleteKey
from Modules.functions import clear_console, inp, wait_for_enter

# Import the roles
from Roles.admin import start as admin_menu
from Roles.manager import start as manager_menu
from Roles.chef import start as chef_menu
from Roles.customer import start as customer_menu

# Logout function
def logout():
    print("Logout. Redirecting to login page.")
    clear_console(2)
    main_start()

def update_profile(username, return_func):
    while True:
        print("-"*35)
        print("Update Profile")
        print("-"*35)
        print("1. Update Name")
        print("2. Update Email")
        print("3. Update Role")
        print("4. Update Password")
        print("5. Back")
        print("-"*35)
        try:
            update_choice = int(input("Enter your choice: "))
            if update_choice == 1:
                new_name = get_user_input("Enter your new name: ")
                update_user(user=username, email=usrEmailDB[username], name=new_name, role=rolesDB[username])
            elif update_choice == 2:
                new_email = get_user_input("Enter your new email: ", "email")
                update_user(email=new_email)
            elif update_choice == 3:
                new_role = get_user_input("Enter your new role: ", "role", valid_roles)
                update_user(role=new_role)
            elif update_choice == 4:
                new_password = get_user_input("Enter your new password: ", "password")
                update_user(password=new_password)
            elif update_choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")
                clear_console(5)
                continue
        except ValueError:
            print("Invalid choice. Please try again.")
            clear_console(5)
            continue
        return_func(username)
        
def main_menu(username, role):
    match role:
        case "customer":
            print("Customer Menu")
            customer_menu(username)
        case "chef":
            print("You are a Chef. Choose an option:")
            print("1. Continue as Chef")
            print("2. Continue as a Customer")
            ch = inp("Enter your choice: ", "int", [1, 2])
            match ch:
                case 1:
                    print("Chef Menu")
                    chef_menu(username)
                case 2:
                    print("Customer Menu")
                    customer_menu(username)
        case "manager":
            print("You are a Manager. Choose an option:")
            print("1. Continue as Manager")
            print("2. Continue as a Customer")
            ch = inp("Enter your choice: ", "int", [1, 2])
            match ch:
                case 1:
                    print("Manager Menu")
                    manager_menu(username)
                case 2:
                    print("Customer Menu")
                    customer_menu(username)
        case "administrator":
            print("You are an Adminstrator. Choose an option:")
            print("1. Continue as Admin")
            print("2. Continue as a Customer")
            ch = inp("Enter your choice: ", "int", [1, 2])
            match ch:
                case 1:
                    print("Administrator Menu")
                    admin_menu(username)
                case 2:
                    print("Customer Menu")
                    customer_menu(username)
        case _:
            print("Invalid role. Please contact the administrator.")
            logout()
            
def reset_password():
    clear_console()
    print("Reset Password")
    username = inp("Enter username: ").strip().lower()
    if not db_getKey("users", username):
        print("Username not found.")
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
                    print("Identity verified.")
                    new_password = inp("Enter new password: ", "password")
                    new_password_confirm = inp("Confirm new password: ", "password")
                    if new_password != new_password_confirm:
                        print("Passwords do not match. Please try again.")
                        wait_for_enter("Press Enter to go back to the main screen.", True)
                        main_start()
                        return
                    password_data = {
                        "password": new_password,
                        "attempts": 0
                    }
                    db_updateKey("passwords", username, password_data)
                    print("Password reset successful.")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_start()
                else:
                    print("Email is not the valid email on file.")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_menu()
            case 2:
                phone = db_getKey("users", username)["PhoneNumber"]
                print("Please enter your phone number to verify your identity.")
                user_input = inp("Enter your phone number: ", "int")
                if user_input == phone:
                    print("Identity verified.")
                    new_password = inp("Enter new password: ", "password")
                    new_password_confirm = inp("Confirm new password: ", "password")
                    if new_password != new_password_confirm:
                        print("Passwords do not match. Please try again.")
                        wait_for_enter("Press Enter to go back to the main screen.", True)
                        main_start()
                        return
                    password_data = {
                        "password": new_password,
                        "attempts": 0
                    }
                    db_updateKey("passwords", username, password_data)
                    print("Password reset successful.")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_start()
                else:
                    print("Phone number is not the valid number on file.")
                    wait_for_enter("Press Enter to go back to the main screen.", True)
                    main_menu()
            case 3:
                print("Cancelling...")
                main_start()
            
def register():
    print("Register as a new user.")
    inp_username = inp("Enter username: ").strip().lower()
    inp_password = inp("Enter password: ", "password")
    inp_name = input("Enter your name: ").strip()
    inp_email = inp("Enter email: ", "email")
    inp_phone = inp("Enter phone number: ", "int")
    inp_dob = inp("Enter date of birth (YYYY-MM-DD): ")
    inp_address = input("Enter address: ").strip()
    inp_confirm_password = inp("Confirm password: ", "password")
    if inp_password != inp_confirm_password:
        print("Passwords do not match. Please try again.")
        wait_for_enter("Press Enter to go back to the main screen.", True)
        main_start()
        return
    user_data = {
        "name": inp_name,
        "email": inp_email,
        "role": "customer",
        "PhoneNumber": inp_phone,
        "DOB": inp_dob,
        "Address": inp_address
    }
    password_data = {
        "password": inp_password,
        "attempts": 0
    }
    if db_getKey("users", inp_username):
        print("Username already exists.")
        wait_for_enter("Press Enter to go back to the main screen.", True)
        main_start()
        return
    else:
        db_addKey("users", inp_username, user_data)
        db_addKey("passwords", inp_username, password_data)
        print("Registration successful.")
        wait_for_enter("Press Enter to go back to the main screen.", True)
        main_start()

def login():
    while True:
        print("Login to continue.")
        inp_username = input("Enter username: ").strip().lower()

        # Check if the username is in the database
        usersList = db_getAllKeys("users")
        if inp_username in usersList:
            print(f"Hi, {inp_username}.")
            user_data = dict(db_getKey("users", inp_username))
            user_password_data = dict(db_getKey("passwords", inp_username))
            # check if the attempts is greater than or equal to 3, dont let user login if so
            if user_password_data['attempts'] >= 3:
                print("You have exceeded the maximum number of login attempts. Please reset your password to reset the attempts.")
                print("1. Reset Password \n2. Go Back to Main Menu")
                ch = inp("Enter your choice: ", "int", [1, 2])
                match ch:
                    case 1:
                        reset_password()
                    case 2:
                        main_start()
                break
            else:
                inp_password = input("Enter password: ").strip()
                if inp_password == user_password_data['password']:
                    user_password_data['attempts'] = 0
                    db_updateKey("passwords", inp_username, user_password_data)
                    print("\n\n")
                    print(f"Welcome Back, {user_data['name']} [{inp_username}]!")
                    main_menu(inp_username, user_data['role'])
                    break
                else:
                    print("Invalid password.")
                    user_password_data['attempts'] += 1
                    db_updateKey("passwords", inp_username, user_password_data)
                    print(f"Login attempts remaining: {3 - user_password_data['attempts']}")
                    print("Forgot password? \n 1. Reset Password \n 2. Try Again \n 3. Go Back to Main Menu")
                    ch = inp("Enter your choice: ", "int", [1, 2, 3])
                    match ch:
                        case 1:
                            reset_password()
                        case 2:
                            login()
                        case 3:
                            main_start()
        else:
            print("Username not found.")
            wait_for_enter("Press Enter to try again.", True)

def main_start():
    clear_console()
    print("Welcome to the Restaurant Management System.")
    print("1. Login \n2. Register \n3. Exit")
    ch = inp("Enter your choice: ", "int", [1, 2, 3])
    match ch:
        case 1:
            login()
        case 2:
            register()
        case 3:
            print("Exiting...")
            exit()
        case _:
            print("Invalid choice. Please try again.")
            clear_console(5)
            main_start()

try:
    main_start()
except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting...")