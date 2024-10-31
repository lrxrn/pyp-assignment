"""The main program file for the Restaurant Management System."""
# Import the required modules
import base64
import re

# Import the modules
from Modules.db import db_addKey, db_getKey, db_updateKey
from Modules.db import db_getAllKeys, db_getAllValues, db_savePassword
from Modules.utils import clear_console, inp, wait_for_enter, printD, display_rich_table
from Modules.utils import generate_password, decode_password, time_object, date_diff
from Modules.utils import log, encode_password, wait_for

# Import the roles
from Roles.admin import start as admin_menu
from Roles.manager import start as manager_menu
from Roles.chef import start as chef_menu
from Roles.customer import start as customer_menu

# Logout function
def logout(usr=None):
    """Function to logout the user and return to the main menu.

    Args:
        usr (str, optional): The username of the user who is logging out. Defaults to None.
    """
    print("\n")
    if usr:
        printD(f"Logging out... \nGoodbye {usr}.", "yellow")
    else:
        printD("Logging out..", "yellow")
    clear_console(1)
    main_start()

# Update profile function
def update_profile(username, admin_username=None, choice=None, return_func=None):
    """Function to update the profile of a user.

    Args:
        username (str): The username of the user that the profile is being updated.
        admin_username (str, optional): The governing admin user if any. Defaults to None.
        choice (int, optional): The pre-chosen choice option. Defaults to None.
        return_func (func, optional): The function to return to. Defaults to None.
    """
    clear_console()
    admin_privileges = False
    if admin_username:
        admin_user_data = db_getKey("users", admin_username)
        if admin_user_data:
            admin_privileges = admin_user_data['role'] == "administrator"
    else:
        admin_privileges = False
    
    printD("Update Profile", "cyan")
    print(f"Username: {username}")
    if choice is None:
        user_data = db_getKey("users", username)
        user_password_data = db_getKey("passwords", username)
        print(f"Name: {user_data['name']}")
        print(f"Email: {user_data['email']}")
        print(f"Phone Number: {user_data['PhoneNumber']}")
        print(f"Date of Birth: {user_data['DOB']} ({date_diff(user_data['DOB'], type='dob')} old)")
        print(f"Address: {user_data['address']}")
        print(f"Role: {user_data['role']}")
        if user_password_data is None or user_password_data.get('last_login') is None:
            printD("Last Login: unknown", "yellow")
        elif user_password_data['last_login'] == "never":
            printD("Last Login: never", "yellow")
        else:
            printD(f"Last Login: {user_password_data['last_login']} ({date_diff(user_password_data['last_login'])})", "white", True)
        if admin_privileges:
            if user_password_data is None or user_password_data.get('password') is None:
                printD("Password: Not set", "yellow")
            elif user_password_data['attempts'] >= 3:
                printD("Password: Locked", "yellow")
            
            display_rich_table(title="Update profile", data=[["1", "Update name"], ["2", "Update email"], ["3", "Update phone number"], ["4", "Update address"], ["5", "Update password"], ["6", "Update role"], ["M", "Go back to [M]ain menu"]], title_style="cyan on white")
            ch = inp("Enter your choice: ", "str", ["1", "2", "3", "4", "5", "6", "M"], stringUpperSensitive=True)
        else:
            display_rich_table(title="Update profile", data=[["1", "Update name"], ["2", "Update email"], ["3", "Update phone number"], ["4", "Update address"], ["5", "Update password"], ["M", "Go back to [M]ain menu"]], title_style="cyan on white")
            ch = inp("Enter your choice: ", "str", ["1", "2", "3", "4", "5", "M"], stringUpperSensitive=True)
    else:
        ch = choice
  

    match ch:
        case "1":
            new_name = input("Enter new name: ").strip()
            user_data['name'] = new_name
            db_updateKey("users", username, user_data)
            printD("Name updated successfully.", "green")
        case "2":
            new_email = inp("Enter new email: ", "email")
            user_data['email'] = new_email
            db_updateKey("users", username, user_data)
            printD("Email updated successfully.", "green")
        case "3":
            new_phone = inp("Enter new phone number: ", "phone")
            user_data['PhoneNumber'] = new_phone
            db_updateKey("users", username, user_data)
            printD("Phone number updated successfully.", "green")
        case "4":
            new_address = input("Enter new address: ").strip()
            user_data['address'] = new_address
            db_updateKey("users", username, user_data)
            printD("Address updated successfully.", "green")
        case "5":
            if user_password_data is None or user_password_data.get('password') is None: # If password is not set
                if admin_privileges:
                    printD("Password not set. Please set a password for this user.", "yellow")
                    print("1. Reset Password \n2. Go Back to Main Menu")
                    ch = inp("Enter your choice: ", "int", [1, 2])
                    match ch:
                        case 1:
                            reset_password(username)
                        case 2:
                            main_menu(username, user_data['role'])
                else:
                    printD("Password not set. Please contact an administrator to set your password.", "yellow")
                    wait_for_enter("Press Enter to go back to the main menu.", True)
                    main_menu(username, user_data['role'])
            else:
                current_password = base64.b64decode(db_getKey("passwords", username)['password']).decode()
                inp_password = inp("Enter current password: ", "pwd")
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
                    "password": encode_password(new_password),
                    "attempts": 0,
                    "last_login": user_password_data['last_login']
                }
                db_updateKey("passwords", username, password_data)
                printD("Password updated successfully.", "green")
        case "6":
            if admin_privileges:
                print("1. Customer \n2. Chef \n3. Manager \n4. Administrator")
                new_role = inp("Enter new role: ", "int", [1, 2, 3, 4])
                roles = ["customer", "chef", "manager", "administrator"]
                user_data['role'] = roles[new_role - 1]
                db_updateKey("users", username, user_data)
                printD("Role updated successfully.", "green")
            else:
                printD("Invalid choice. Please try again.", "yellow")
        case "M":
            wait_for_enter("Press Enter to go back to the main menu.", True)
            main_menu(username, user_data['role'])
        
    if return_func:
        if admin_username is not None:
            return_func(admin_username)
        else:
            return_func(username)
    else:
        wait_for_enter("Press Enter to go back to the main menu.", True)
        if admin_username is not None:
            main_menu(admin_username, user_data['role'])
        else:
            main_menu(username, user_data['role'])

# Main menu function
def main_menu(username, role:str):
    """The main menu function that redirects the user to their respective roles.

    Args:
        username (str): The username of the user.
        role (str): The role of the user.
    """
    role = role.strip().lower()
    match role:
        case "customer":
            # No need to ask whether to continue as a customer or not
            customer_menu(username)
        case "chef":
            display_rich_table(title="You are a Chef.", data=[["1", "Continue as a Chef"], ["2", "Continue as a Customer"], ["L", "[L]ogout"]], title_style="bright_magenta on white")
            ch = inp("Enter your choice: ", "str", ["1", "2", "L"], stringUpperSensitive=True)
            clear_console(0.5)
            match ch:
                case "1":
                    chef_menu(username)
                case "2":
                    customer_menu(username)
                case _:
                    logout(username)
        case "manager":
            display_rich_table(title="You are a Manager.", data=[["1", "Continue as a Manager"], ["2", "Continue as a Customer"], ["L", "[L]ogout"]], title_style="bright_magenta on white")
            ch = inp("Enter your choice: ", "str", ["1", "2", "L"], stringUpperSensitive=True)
            clear_console(0.5)
            match ch:
                case "1":
                    manager_menu(username)
                case "2":
                    customer_menu(username)
                case _:
                    logout(username)
        case "administrator":
            display_rich_table(title="You are an Admin.", data=[["1", "Continue as an Administrator"], ["2", "Continue as a Customer"], ["L", "[L]ogout"]], title_style="bright_magenta on white")
            ch = inp("Enter your choice: ", "str", ["1", "2", "L"], stringUpperSensitive=True)
            clear_console(0.5)
            match ch:
                case "1":
                    admin_menu(username)
                case "2":
                    customer_menu(username)
                case _:
                    logout(username)
        case _:
            printD("Your user role in our Database is invalid. Please contact an Administrator to reset your user role.", "yellow")
            logout(username)

# Reset password function
def reset_password(usr=None):
    """A function to reset the password of a user.

    Args:
        usr (str, optional): The username of the user to reset the password of. Defaults to None.
    """
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
        display_rich_table(title="Identity verification", data=[["1", "Email verification"], ["2", "Phone verification"], ["C", "[C]ancel and Go back to Main menu"]], title_style="green on white")
        ch = inp("Enter your choice: ", "str", ["1", "2", "C"], stringUpperSensitive=True)
        match ch:
            case "1":
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
            case "2":
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
            case "C":
                print("Cancelling...")
                main_start()

# Registration function     
def register(staff_username=None, return_func=None):
    """Function to register a new user.

    Args:
        staff_username (str, optional): The username of the staff that invokes the register function. Defaults to None.
        return_func (func, optional): The user menu function to return to. Defaults to None.
    """
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
        "address": inp_address
    }
    password_data = {
        "password": base64.b64encode(inp_password.encode()).decode(),
        "attempts": 0,
        "last_login": "never"
    }
    if db_getKey("users", inp_username):
        printD("Username already exists.", "yellow")
        wait_for_enter("Press Enter to go back.", True)
        if return_func:
            return_func(staff_username)
        else:
            main_start()
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
                if return_func:
                    return_func(staff_username)
                else:
                    main_start()
            case "n":
                printD("Registration cancelled.", "yellow")
                wait_for_enter("Press Enter to go back.", True)
                if return_func:
                    return_func(staff_username)
                else:
                    main_start()

# Login function
def login(usr=None):
    """Function to login to the system.

    Args:
        usr (str, optional): The username of the user that is logging in. Defaults to None.
    """
    clear_console()
    printD("Login to continue.", "cyan")
    if usr:
        inp_username = usr
    else:
        inp_username = input("Enter username / email: ").strip().lower()

    # Check if the username is in the database
    usersList = db_getAllKeys("users")
    userData = db_getAllValues("users")
    userDataMap = [{**data, 'username': usersList[userData.index(data)]} for data in userData]
    userEmails = [i['email'] for i in userData]
    if inp_username in usersList or inp_username in userEmails:
        if inp_username in usersList:
            user_data = dict(db_getKey("users", inp_username))
            login_usr = inp_username
        elif inp_username in userEmails:
            user_data = userDataMap[userEmails.index(inp_username)]
            login_usr = user_data['username']
        else:
            printD("Username / Email not found.", "red")
            wait_for_enter("Press Enter to go back to the main screen.", True)
            return main_start()
            
        printD(f"Hi, {login_usr}.", "white", True)
        # check if the user has a password
        user_password_data = db_getKey("passwords", login_usr)
        if not user_password_data:
            printD("User has no password set. Please contact an administrator to reset your password.", "yellow")
            wait_for_enter("Press Enter to go back to the main screen.", True)
            main_start()
            
        # check if the attempts is greater than or equal to 3, dont let user login if so
        if user_password_data['attempts'] >= 3:
            printD("Your account has been locked due to multiple failed login attempts.", "red")
            printD("Please reset your password to unlock your account.", "yellow")
            display_rich_table(title="Forgot password?", data=[["1", "Reset Password"], ["M", "Go back to [M]ain menu"]], title_style="yellow on white")
            ch = inp("Enter your choice: ", "str", ["1", "M"], stringUpperSensitive=True)
            match ch:
                case "1":
                    reset_password(login_usr)
                case "M":
                    main_start()
        else:
            user_password = decode_password(user_password_data['password'])
            inp_password = inp("Enter your password: ", "pwd")
            wait_for(0.5)
            clear_console()
            printD("Logging in...", "cyan")
            wait_for(2)
            clear_console()
            if inp_password == user_password:
                user_password_data['attempts'] = 0
                user_last_login = user_password_data['last_login']
                user_password_data['last_login'] = f"{time_object()[0]} {time_object()[1]}"
                db_updateKey("passwords", login_usr, user_password_data)
                clear_console(1)
                if user_last_login == "never":
                    printD(f"Welcome, {user_data['name']} [{login_usr}]!\n", "white", True)
                else:
                    printD(f"Welcome Back, {user_data['name']} [{login_usr}]!", "white", True)
                    print(f"Last Successful Login: {user_last_login} ({date_diff(user_last_login)})\n")
                main_menu(login_usr, user_data['role'])
            elif inp_password == "":
                printD("Please enter your password to login.", "yellow")
            else:
                clear_console()
                printD("Invalid password.", "red")
                user_password_data['attempts'] += 1
                db_updateKey("passwords", login_usr, user_password_data)
            printD(f"Login attempts remaining: {3 - user_password_data['attempts']}", "yellow", True)
            display_rich_table(title="Forgot password?", data=[["1", "Reset Password"], ["2", "Try again"], ["M", "Go back to [M]ain menu"]], title_style="yellow on white")
            ch = inp("Enter your choice: ", "str", ["1", "2", "M"], stringUpperSensitive=True)
            match ch:
                case "1":
                    reset_password(login_usr)
                case "2":
                    login(login_usr)
                case "M":
                    main_start()
    else:
        printD("Username / Email not found.", "red")
        wait_for_enter("Press Enter to go back to the main screen.", True)
        main_start()

def main_start():
    """A function to start the main program. This function is the entry point of the program.
    """
    clear_console(2)
    # Load the users database to run the pre-check and add the default admin user if not present
    db_getAllKeys("users")
    printD("Welcome to the Restaurant Management System.", "blue", True)
    display_rich_table(title="Main Menu", data=[["1", "Login"], ["2", "Register"], ["3", "Reset Password"], ["E", "[E]xit"]])
    ch = inp("Enter your choice: ", "str", ["1", "2", "3", "E"], stringUpperSensitive=True)
    match ch:
        case "1":
            login()
        case "2":
            register(None, main_start)
        case "3":
            reset_password()
        case "E":
            printD("Exiting...", "red", True)
            exit()

if __name__ == "__main__":
    try:
        main_start()
    except KeyboardInterrupt:
        clear_console()
        printD("\nProgram interrupted. \nExiting...", "red", True)
    except Exception as e:
        log(e, "error", "main.py")
        printD(f"\nAn error occurred. Error has been logged. \nLogging out...", "red", True)
        logout()
        raise e
    # except:
    #     printD("\nAn error occurred. \nExiting...", "red", True)