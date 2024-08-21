# to doimport os
import time
import base64
import re

# Enable logging of debug messages. Set to False to disable
DEBUG_MODE = True

# pre determine valid user roles
valid_roles = ["administrator", "manager", "chef", "customer"]
valid_inputTypes = ["str", "int", "email", "role", "password"]

# db directories
usersDB_path = "./db/users.txt"
credentialsDB_path = "./db/credentials.txt"
DBfolder_path = "./db"

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

# Database class
class Database:
    def __init__(self, usersDB_path, credentialsDB_path):
        self.usersDB_path = usersDB_path
        self.credentialsDB_path = credentialsDB_path

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

# Debug print function
def debug_print(*args):
    if DEBUG_MODE:
        print("[DEBUG]:", *args)

# Function to wait for user to press Enter (does not do anything except wait for user input)
def wait_for_enter(msg="Press Enter to proceed...", clear=False):
    input(msg)
    if clear:
        clear_console()

def validate_input(input, type="str"):
    if type == "int":
        try:
            input = int(input)
            return input
        except ValueError:
            return False
    elif type == "email":
        if re.match(r"[^@]+@[^@]+\.[^@]+", input):
            return input
        else:
            return False
    elif type == "role":
        if input.lower() in valid_roles:
            return input.lower()
        else:
            return False
    elif type == "password":
        if re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", input):
            return input
        else:
            return False
    else:
        return input

# function to accept user input and validate it
def get_user_input(prompt, type="str", valid_values=None):
    while True:
        # check if the type is a valid type
        type = type.lower()
        if type not in valid_inputTypes:
            debug_print("Invalid input type. Defaulting to string.")
            type = "str"
        
        # get the user input
        user_input = input(prompt)
        # check if there is a valid value to check against
        if valid_values:
            if user_input in valid_values:
                validated_input = validate_input(user_input, type)
                if validated_input:
                    return validated_input
                else:
                    print(f"Invalid input. Please enter a valid {type}.")
                    continue
            else:
                print(f"Invalid input. Please enter a valid value. \n Value should be one of {valid_values}")
                continue
        else:
            validated_input = validate_input(user_input, type)
            if validated_input:
                return validated_input
            else:
                print(f"Invalid input. Please enter a valid {type}.")
                continue

# check if the db directory exists
if not os.path.exists(DBfolder_path):
    os.mkdir(DBfolder_path)

# check if the users file exists
if not os.path.exists(usersDB_path):
    with open(usersDB_path, "w") as f:
        f.write("")

# check if the credentials file exists
if not os.path.exists(credentialsDB_path):
    with open(credentialsDB_path, "w") as f:
        f.write("")

# read the user list from db/users.txt
usersDB = open(usersDB_path, "r")
usersDB = usersDB.readlines()
usersDB = [user.strip() for user in usersDB]
# map the user to email and email to user
emailsDB = dict([[user.split(",")[1],user.split(",")[0]] for user in usersDB])
usrEmailDB = dict([[user.split(",")[0],user.split(",")[1]] for user in usersDB])
rolesDB = dict([[user.split(",")[0],user.split(",")[3]] for user in usersDB])
usersDB = dict([[user.split(",")[0],user.split(",")[2]] for user in usersDB])

# read the user password from db/credentials.txt and map it to the user (user,password)
passwordsDB = open(credentialsDB_path, "r")
passwordsDB = passwordsDB.readlines()
# Decrypt the password
passwordsDB = [password.strip() for password in passwordsDB]
passwordsDB = dict([[password.split(",")[0],decrypt(password.split(",")[2])] for password in passwordsDB])
# passwordAttemptsDB = dict([[password.split(",")[0],int(password.split(",")[1])] for password in passwordsDB])
passwordAttemptsDB = dict([[user,1] for user in usersDB])

# database save functions
def save_new_user(user, email, name, role, password):
    with open(usersDB_path, "a") as f:
        # Append the privided user details to the file
        f.write(f"\n{user.lower()},{email.lower()},{name},{role.lower()}\n")

    with open(credentialsDB_path, "a") as f:
        # Append the user and password to the file
        f.write(f"\n{user.lower()},{password}")

def save_users():
    # Save the users to the file and overwrite the existing content
    with open(usersDB_path, "w") as f:
        for user in usersDB:
            f.write(f"{user},{usrEmailDB[user]},{usersDB[user]},{rolesDB[user]}\n")


def save_passwords():
    with open(credentialsDB_path, "w") as f:
        for user in passwordsDB:
            # check if the password is encrypted
            if is_encrypted(passwordsDB[user]):
                #f.write(f"{user},{passwordAttemptsDB[user]},{encrypt(passwordsDB[user])}\n")
                f.write(f"{user},{encrypt(passwordsDB[user])}\n")
            else:
                #f.write(f"{user},{passwordAttemptsDB[user]},{passwordsDB[user]}\n")
                f.write(f"{user},{passwordsDB[user]}\n")

def update_user(user, email, name, role):
    debug_print(f"Updating user: {user} with email: {email}, name: {name}, role: {role}")
    usersDB[user] = name
    emailsDB[email] = user
    rolesDB[user] = role
    save_users()

# Clear console function to de-clutter the console
def clear_console(wait_time=None):
    # Wait for specifc time before clearing the console
    if wait_time:
        time.sleep(wait_time)
    os.system('clear' if os.name == 'posix' else 'cls')

def wait(wait_time):
    time.sleep(wait_time)

def logout():
    debug_print("Logout function called.")
    print("Logout. Redirecting to login page.")
    clear_console(2)
    start()

def update_profile(username):
    debug_print("Update profile function called.")
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

def admin_menu(username):
    while True:
        print("-"*35)
        print("Administrator Menu")
        print("-"*35)
        print("1. Manage staff")
        print("2. View sales report")
        print("3. View feedback")
        print("4. Update profile")
        print("5. Logout")
        print("-"*35)
        try:
            main_choice = int(input("Enter your choice: "))
            if main_choice == 1:
                admin_manageStaff()
            elif main_choice == 2:
                admin_view_sales_report()
            elif main_choice == 3:
                admin_view_feedback()
            elif main_choice == 4:
                update_profile(username)
            elif main_choice == 5:
                logout()
            else:
                print("Invalid choice. Please try again.")
                clear_console(5)
                continue
        except ValueError:
            print("Invalid choice. Please try again.")
            clear_console(5)
            continue


def admin_manageStaff():
    while True:
        print("-"*35)
        print("Admin: Manage Staff")
        print("-"*35)
        print("1. Add staff")
        print("2. Remove staff")
        print("3. Update staff")
        print("4. View staff")
        print("5. Back")
        print("-"*35)
        try:
            manage_staff_choice = int(input("Enter your choice: "))
            if manage_staff_choice == 1:
                admin_manageStaff_addStaff()
            elif manage_staff_choice == 2:
                admin_manageStaff_removeStaff()
            elif manage_staff_choice == 3:
                admin_manageStaff_updateStaff()
            elif manage_staff_choice == 4:
                clear_console()
                admin_manageStaff_viewStaff()
            elif manage_staff_choice == 5:
                admin_menu()
                break
            else:
                print("Invalid choice. Please try again.")
                clear_console(5)
                continue
        except ValueError:
            print("Invalid choice. Please try again.")
            clear_console(5)
            continue

def admin_manageStaff_addStaff():
    print("Enter the details of the staff.")
    name = input("Enter the name: ")
    email = input("Enter the email: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    role = input("Enter the role: ")
    save_new_user(username, email, name, role, password)

def admin_manageStaff_removeStaff():
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

def admin_manageStaff_viewStaff():
    print("Staff list:")
    print("-"*50)
    print("Name [Username] - Email - Role")
    print("-"*50)
    for user in usersDB:
        print(f"{usersDB[user]} [{user}] - {usrEmailDB[user]} - {rolesDB[user]}")
    print("-"*50)
    wait(10)


def manager_menu():
    # to be implemented
    return

def chef_menu():
    # to be implemented
    return

def customer_menu():
    # to be implemented
    return

def main_menu(role, username):
    debug_print("Main menu function called.")
    while True:
        if role == "administrator":
            admin_menu(username)
        elif role == "manager":
            print("You are a manager.")
            manager_menu()
        elif role == "chef":
            print("You are a chef.")
            chef_menu()
        elif role == "customer":
            print("You are a customer.")
            customer_menu()
        else:
            print("Invalid role.")
            clear_console(3)
            logout()
            break

def login():
    debug_print("Login function called.")
    while True:
        print("Welcome to the restaurant \nLogin to continue.")
        inp_username = input("Enter username/ email: ").strip().lower()

        if inp_username in usersDB:
            print(f"Hi, {inp_username}.")
            # check if the attempts is greater than or equal to 3, dont let user login if so
            if passwordAttemptsDB[inp_username] >= 3:
                    print("You have exceeded the maximum number of login attempts. Please try again later.")
                    wait_for_enter("Press Enter to go back to the login screen.", True)
                    start()
                    break
            else:
                passwordAttemptsDB[inp_username] += 1

                inp_password = input("Enter password: ").strip()
                if inp_password == passwordsDB[inp_username]:
                    print("\n\n")
                    print(f"Welcome Back, {usersDB[inp_username]} [{inp_username}]!")
                    wait(2)
                    main_menu(rolesDB[inp_username], inp_username)
                    break
                else:
                    print("Invalid password.")
                    wait_for_enter("Press Enter to try again.", True)
                
        elif inp_username in emailsDB:
            print(f"Hi, {inp_username}.")
            # check if the attempts is greater than or equal to 3, dont let user login if so
            if passwordAttemptsDB[emailsDB[inp_username]] >= 3:
                    print("You have exceeded the maximum number of login attempts. Please try again later.")
                    wait_for_enter("Press Enter to go back to the login screen.", True)
                    start()
                    break
            else:
                passwordAttemptsDB[emailsDB[inp_username]] += 1

            inp_password = input("Enter password: ").strip()
            if inp_password == passwordsDB[emailsDB[inp_username]]:
                print("\n\n")
                print(f"Welcome Back {usersDB[emailsDB[inp_username]]} [{emailsDB[inp_username]}]!")
                wait(2)
                main_menu(rolesDB[emailsDB[inp_username]], emailsDB[inp_username])
                break
            else:
                print("Invalid password.")
                wait_for_enter("Press Enter to try again.", True)
        else:
            debug_print(f"Invalid username or email. \nInput: {inp_username}")
            print("Invalid username or email.")
            wait_for_enter("Press Enter to try again.", True)

def start():
    clear_console()
    login()

if __name__ == "__main__":
    try:
        debug_print("Starting the program.")
        start()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")