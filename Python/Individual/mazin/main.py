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
                return inp_value
            else:
                print("Password must be at least 8 characters long and contain at least one letter and one number")

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
                datetime.datetime.strptime(inp_value, "%d/%m/%Y")
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



def edit_customer_list(edit, new_value, type):
    if type == "password":
        try:
            with open('passwords.json', 'r') as editpasswords:
                editpasswords = json.load(editpasswords)
        except FileNotFoundError:
            editpasswords = {}

        editpasswords[edit][type] = {
            "password": new_value
        }

        with open('passwords.json', 'w') as editpasswordsfile:
            json.dump(editpasswords, editpasswordsfile, indent=4)
    try:
        with open('users.json', 'r') as editusers:
            editusers = json.load(editusers)
    except FileNotFoundError:
        editusers = {}

    editusers[edit][type] = new_value

    with open('users.json', 'w') as editusersfile:
        json.dump(editusers, editusersfile, indent=4)


def edit_customer():
    print("-" * 50)
    try:
        with open('users.json', 'r') as editusers:
            editusers = json.load(editusers)
    except FileNotFoundError:
        editusers = {}

    listofcustimers = []
    for key, value in editusers.items():
        listofcustimers.append(f"{key}")
    n = len(listofcustimers)

    if n == 0:
        print("No customers found")
        manage_customer()

    print("Edit Customer")
    for i in range(n):
        print(f"{i + 1}: {listofcustimers[i]}")

    while True:
        edit_customer_option = input("Choose a customer to edit (type \"c\" to cancel): ")
        if edit_customer_option == "c":
            manage_customer()
            break
        if edit_customer_option.isnumeric():
            edit_customer_option = int(edit_customer_option)
            if 0 < edit_customer_option <= n:
                user_nm = listofcustimers[edit_customer_option - 1]
                break
            else:
                print(f"Invalid input. Please type a number from 1 to {n}")
                continue
        else:
            print(f"Invalid input. Please type a number from 1 to {n}")
            continue

    print(f"Edit Customer: {user_nm}")
    print("1: Edit Name\n2: Edit Email\n3: Edit Phone Number\n4: Edit Date of Birth\n5: Edit Address\n6: Edit Password\n7: Go Back")

    while True:
        editcustomerinfo = input("Choose an option from 1 to 7: ")
        if editcustomerinfo == "1":
            print(f"Edit Name\nCurrent name: {editusers[user_nm]["name"]}")
            new_name = input("Enter new name: ")
            edit_customer_list(user_nm, new_name, "name")
            manage_customer()
            break
        elif editcustomerinfo == "2":
            print(f"Edit Email\nCurrent email: {editusers[user_nm]["email"]}")
            new_email = input("Enter new email: ")
            edit_customer_list(user_nm, new_email, "email")
            manage_customer()
            break
        elif editcustomerinfo == "3":
            print(f"Edit Phone Number\nCurrent phone number: {editusers[user_nm]["PhoneNumber"]}")
            new_phonenumber = input("Enter new phone number: ")
            edit_customer_list(user_nm, new_phonenumber, "PhoneNumber")
            manage_customer()
            break
        elif editcustomerinfo == "4":
            print(f"Edit Date of Birth\nCurrent date of birth: {editusers[user_nm]["DOB"]}")
            new_dob = input("Enter new date of birth: ")
            edit_customer_list(user_nm, new_dob, "DOB")
            manage_customer()
            break
        elif editcustomerinfo == "5":
            print(f"Edit Address\nCurrent address: {editusers[user_nm]["Address"]}")
            new_address = input("Enter new address: ")
            edit_customer_list(user_nm, new_address, "Address")
            manage_customer()
            break
        elif editcustomerinfo == "6":
            new_password = validate_and_input_customer("Enter new password: ", "Password")
            confirm_password = input("Confirm new password: ")
            if new_password != confirm_password:
                print("Passwords do not match")
                continue
            edit_customer_list(user_nm, new_password, "password")
            manage_customer()
            break
        elif editcustomerinfo == "7":
            manage_customer()
            break
        else:
            print("Invalid input. Please type a number from 1 to 7")
            continue


def delete_customer():
    print("-" * 50)
    while True:
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


def get_next_id(filename, prefix):
    if not filename:
        return f"{prefix}01"
    ids = [int(item["MenuItmID"].split('-')[1]) for item in filename]
    next_id_num = max(ids) + 1
    return f"{prefix}{next_id_num:02d}"


def add_menu():
    try:
        with open("menuItems.json", 'r') as file:
            file = json.load(file)
    except FileNotFoundError:
        file = []

    new_menu_name = input("Enter the name of the new menu item: ")
    new_cuisine_type = input("Enter the cuisine type of the new menu item: ")
    new_price = input("Enter the price of the new menu item: ")
    new_category = input("Enter the category of the new menu item: ")

    new_item = {
        "MenuItmID": get_next_id(file, "BG-"),
        "Name": new_menu_name,
        "CuisineType": new_cuisine_type,
        "Price": new_price,
        "Category": new_category
    }
    file.append(new_item)

    with open("menuItems.json", 'w') as file2:
        json.dump(file, file2, indent=4)

    print("Menu item added successfully")
    manage_menuandpricing()


def edit_menu_item():
    print("-" * 50)
    print("Edit Menu Item")


def delete_menu_item():
    print("-" * 50)
    print("Delete Menu Item")
    try:
        with open('menuItems.json', 'r') as deletemenu:
            deletemenu = json.load(deletemenu)
    except FileNotFoundError:
        deletemenu = []

    for i in range(len(deletemenu)):
        print(f"{deletemenu[i]['MenuItmID']} - {deletemenu[i]['Name']}")

    while True:
        menu = input("Enter menu item ID to delete: ").upper()
        updated_menu = [item for item in deletemenu if item['MenuItmID'] != menu]

        if len(updated_menu) == len(deletemenu):
            print(f"Item with MenuItmID '{menu}' not found.")
            continue
        else:
            with open('menuItems.json', 'w') as file:
                json.dump(updated_menu, file, indent=4)
            item_to_delete = next((item for item in deletemenu if item['MenuItmID'] == menu), None)
            print(f"Menu item \"{menu} - {item_to_delete['Name']}\" deleted.")
            manage_menuandpricing()


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
