import re
import datetime
import json


def validate_and_input_customer(prompt, type="string"):
    while True:
        inp_value = input(prompt)
        if inp_value == "c":
            manage_customer()

        try:
            with open('users.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if type == "Password":
            if re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", inp_value):
                print("Password must be at least 8 characters long and contain at least one letter and one number")
            else:
                return inp_value

        if type == "Username":
            if inp_value in data:
                print("Username already exists")
                continue
            if re.match(r"[^@]+@[^@]+\.[^@]+", inp_value):
                print("Invalid username. Username should not be in email format")
                continue
            else:
                return inp_value

        if type == "Email":
            email_exists = False
            for entry in data.values():
                if entry.get("email") == inp_value:
                    email_exists = True
                    break
            if email_exists:
                print("Email already exists.")
                continue
            if re.match(r"[^@]+@[^@]+\.[^@]+", inp_value):
                return inp_value
            else:
                print("Invalid email")
                continue

        if type == "Name":
            return inp_value
        if type == "dob":
            try:
                datetime.datetime.strptime(inp_value, "%d-%m-%Y")
                return inp_value
            except ValueError:
                print("Incorrect date format, should be DD-MM-YYYY")


def add_customer():
    print("-" * 50)
    new_customer_username = validate_and_input_customer("Enter new customer username (type \"c\" to cancel): ", "Username")
    new_customer_email = validate_and_input_customer("Enter new customer email (type \"c\" to cancel): ", "Email")
    new_customer_name = input("Enter new customer name (type \"c\" to cancel): ")
    new_customer_phonenumber = input("Enter new customer phone number (type \"c\" to cancel): ")
    new_customer_dob = validate_and_input_customer("Enter new customer date of birth (type \"c\" to cancel): ", "dob")
    new_customer_address = input("Enter new customer address (type \"c\" to cancel): ")
    new_customer_password = validate_and_input_customer("Enter new customer password (type \"c\" to cancel): ", "Password")

    try:
        with open('users.json', 'r') as addusers:
            addusers = json.load(addusers)
    except FileNotFoundError:
        addusers = {}

    addusers[new_customer_username] = {
        "name": new_customer_name,
        "email": new_customer_email,
        "role": "customer",
        "PhoneNumber": new_customer_phonenumber,
        "DOB": new_customer_dob,
        "Address": new_customer_address
    }

    with open('users.json', 'w') as addusersfile:
        json.dump(addusers, addusersfile, indent=4)

    try:
        with open('passwords.json', 'r') as addpasswords:
            addpasswords = json.load(addpasswords)
    except FileNotFoundError:
        addpasswords = {}

    addpasswords[new_customer_username] = {
        "password": new_customer_password
    }

    with open('passwords.json', 'w') as addpasswordsfile:
        json.dump(addpasswords, addpasswordsfile, indent=4)

    print("Customer added successfully.")
    manage_customer()



def edit_customer_list(edit, index, new_value):
    file = open("customer_list", "r")
    lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith(edit):
            customer_info = line.split(", ")
            customer_info[index] = new_value
            lines[i] = ", ".join(customer_info)

    file = open("customer_list", "w")
    file.writelines(lines)


def edit_customer():
    listofcustimers = []
    customer_file = open("customer_list", "r")
    n = 0
    for users in customer_file:
        usersn = users.replace("\n", "")
        listofcustimers.append(usersn)
        if "customer" in users:
            users = users.rstrip()
            n = n + 1
            print(f"{n}: {users}")
    while True:
        edit_customer_check = input(f"Choose a customer to edit from 1 to {n} (type \"c\" to cancel): ")
        if edit_customer_check.isnumeric():
            if int(edit_customer_check) > n:
                print(f"Invalid input. Please enter a number from 1 to {n} or \"c\" to cancel")
                continue
            else:
                edit_customer_num = int(edit_customer_check) - 1
                break
        if edit_customer_check == "c":
            manage_customer()
        else:
            print(f"Invalid input. Please enter a number from 1 to {n} or \"c\" to cancel")
            continue

    print(f"Edit user: {listofcustimers[edit_customer_num]}")
    splitcustomerinfo = listofcustimers[edit_customer_num].split(", ")

    print("-" * 50)
    print("1: Edit username\n2: Edit email\n3: Edit name\n4: Edit password\n5: Go Back")
    edit_customer_detail = input("Choose an option from 1 to 4: ")

    if edit_customer_detail == "1":
        print("-" * 50)
        print("Edit username")
        new_username = validate_and_input_customer("Enter new username (type \"c\" to cancel): ", 0, "Username")

        edit_customer_list(splitcustomerinfo[0], 0, new_username)

        print("Username has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "2":
        print("-" * 50)
        print("Edit email")
        new_email = validate_and_input_customer("Enter new email (type \"c\" to cancel): ", 1, "Email")

        edit_customer_list(splitcustomerinfo[0], 1, new_email)

        print("Email has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "3":
        print("-" * 50)
        print("Edit name")
        new_name = input("Enter new name (type \"c\" to cancel): ")

        if new_name == "c":
            edit_customer()

        edit_customer_list(splitcustomerinfo[0], 2, new_name)

        print("Name has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "4":
        print("-" * 50)
        print("Edit password")
        new_password = validate_and_input_customer("Enter new password (type \"c\" to cancel): ", 3, "Password")

        edit_customer_list(splitcustomerinfo[0], 3, new_password)

        print("Password has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "5":
        manage_customer()
    else:
        print("Invalid input. Please type a number from 1 to 4")
        manage_customer()


def delete_customer():
    print("-" * 50)
    while True:
        global user_nm
        user = input("Enter username to delete (type \"c\" to cancel): ").lower()
        if user == "c":
            manage_customer()

        try:
            with open('users.json', 'r') as deleteusers:
                deleteusers = json.load(deleteusers)
        except FileNotFoundError:
            deleteusers = {}

        if user in deleteusers:
            del deleteusers[user]
            with open('users.json', 'w') as deleteusersfile:
                json.dump(deleteusers, deleteusersfile, indent=4)
        else:
            print("User not found")
            continue

        try:
            with open('passwords.json', 'r') as deletepasswords:
                deletepasswords = json.load(deletepasswords)
        except FileNotFoundError:
            deletepasswords = {}

        if user in deletepasswords:
            del deletepasswords[user]
            with open('passwords.json', 'w') as deletepaswordsfile:
                json.dump(deletepasswords, deletepaswordsfile, indent=4)
            print(f"Deleted user: {user}")
            manage_customer()



def manage_customer():
    print("-" * 50)
    print("Manage Customer\n1: Add Customer\n2: Edit Customer\n3: Delete Customer\n4: Go Back")

    while True:
        manage_customer_option = input("Choose an option from 1 to 4: ")
        if manage_customer_option == "1":
            add_customer()
            break
        elif manage_customer_option == "2":
            edit_customer()
            break
        elif manage_customer_option == "3":
            delete_customer()
            break
        elif manage_customer_option == "4":
            start()
            break
        else:
            print("Invalid input. Please type a number from 1 to 4")
            continue


def validate_and_input_menu(prompt, type="string"):
    while True:
        inp_value = input(prompt)
        if inp_value == "c":
            manage_menuandpricing()

        if type == "price":
            if inp_value.isnumeric():
                return int(inp_value)
            else:
                print("Price should be a number")
        else:
            return inp_value


def add_menu_item(menu_type):
    print("-" * 50)
    print(f"Add {menu_type}")
    menu_item_name = validate_and_input_menu(f"Enter {menu_type} name (type \"c\" to cancel): ", "name")
    menu_item_price = validate_and_input_menu(f"Enter {menu_type} price (type \"c\" to cancel): ", "price")
    menu_item_ingredients = validate_and_input_menu(f"Enter {menu_type} ingredients (type \"c\" to cancel): ", "ingredients")
    menu_file = open("menu_list", "a")
    menu_file.write(f"\n{menu_type}, {menu_item_name}, {menu_item_price}, {menu_item_ingredients}")
    print(f"{menu_type} added successfully")
    manage_menuandpricing()


def add_menu():
    print("-" * 50)
    print("Add Menu Item\n1: Add Main Course\n2: Add Appetizer\n3: Add Dessert\n4: Add Beverage\n5: Go Back")

    while True:
        add_menu_item_option = input("Choose an option from 1 to 5 (type \"c\" to cancel): ")
        if add_menu_item_option == "1":
            add_menu_item("Main Course")
            break
        elif add_menu_item_option == "2":
            add_menu_item("Appetizer")
            break
        elif add_menu_item_option == "3":
            add_menu_item("Dessert")
            break
        elif add_menu_item_option == "4":
            add_menu_item("Beverage")
            break
        elif add_menu_item_option == "5":
            manage_menuandpricing()
            break
        elif add_menu_item_option == "c":
            manage_menuandpricing()
            break
        else:
            print("Invalid input. Please type a number from 1 to 4")
            continue


def edit_menu_item():
    print("-" * 50)
    print("Edit Menu Item\n1: Edit Main Course\n2: Edit Appetizer\n3: Edit Dessert\n4: Go Back")

    while True:
        edit_menu_item_option = input("Choose an option from 1 to 4: ")
        if edit_menu_item_option == "1":
            print("Edit Main Course")
            break
        elif edit_menu_item_option == "2":
            print("Edit Appetizer")
            break
        elif edit_menu_item_option == "3":
            print("Edit Dessert")
            break
        elif edit_menu_item_option == "4":
            manage_menuandpricing()
            break
        else:
            print("Invalid input. Please type a number from 1 to 4")
            continue


def delete_menu_item():
    print("-" * 50)
    print("Delete Menu Item\n1: Delete Main Course\n2: Delete Appetizer\n3: Delete Dessert\n4: Go Back")

    while True:
        delete_menu_item_option = input("Choose an option from 1 to 4: ")
        if delete_menu_item_option == "1":
            print("Delete Main Course")
            break
        elif delete_menu_item_option == "2":
            print("Delete Appetizer")
            break
        elif delete_menu_item_option == "3":
            print("Delete Dessert")
            break
        elif delete_menu_item_option == "4":
            manage_menuandpricing()
            break
        else:
            print("Invalid input. Please type a number from 1 to 4")
            continue


def manage_menuandpricing():
    print("-" * 50)
    print("Manage menu categories and pricing\n1: Add Menu Item\n2: Edit Menu Item\n3: Delete Menu Item\n4: Go Back")

    while True:
        manage_menuandpricing_option = input("Choose an option from 1 to 4: ")
        if manage_menuandpricing_option == "1":
            add_menu()
            break
        elif manage_menuandpricing_option == "2":
            edit_menu_item()
            break
        elif manage_menuandpricing_option == "3":
            delete_menu_item()
            break
        elif manage_menuandpricing_option == "4":
            start()
            break
        else:
            print("Invalid input. Please type a number from 1 to 4")
            continue


def view_ingredientlist():
    print("-" * 50)
    print("View ingredients list requested by chef")


def updateprofile():
    print("-" * 50)
    print("Update own profile")


def logout():
    print("-" * 50)
    print("Logout")


def start():
    print("-" * 50)
    print("Manager Menu\n1: Manage Customer\n2: Manage menu categories and pricing\n3: View ingredients list requested by chef\n4: Update own profile\n5: Logout")

    while True:
        option = input("Choose an option from 1 to 5: ")
        if option == "1":
            manage_customer()
            break
        elif option == "2":
            manage_menuandpricing()
            break
        elif option == "3":
            view_ingredientlist()
            break
        elif option == "4":
            updateprofile()
            break
        elif option == "5":
            logout()
            break
        else:
            print("Invalid input. Please type a number from 1 to 5")
            continue


start()
