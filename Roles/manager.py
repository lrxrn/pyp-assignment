import re
import datetime
import json
from Modules.db import db_getKey, db_updateKey, db_addKey, db_deleteKey, db_getAllKeys, db_getAllValues


def loaddatabase(database, type, data="none"):
    if type == "read":
        try:
            with open(f"{database}.json", 'r') as file:
                file = json.load(file)
        except FileNotFoundError:
            if database == "users" or database == "passwords":
                file = {}
            else:
                file = []
        return file
    if type == "write":
        with open(f"{database}.json", 'w') as file:
            json.dump(data, file, indent=4)


def validate_and_input_customer(prompt, type="string"):
    while True:
        inp_value = input(prompt)
        if inp_value == "c":
            manage_customer()

        data = loaddatabase("users", "read")

        if type == "Password":
            if re.match(r"[A-Za-z0-9@#$%^&+=]{8,}", inp_value):
                return inp_value
            else:
                print("Password must be at least 8 characters long and contain at least one letter and one number")
                continue

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
    new_customer_username = validate_and_input_customer("Enter new customer username (type \"c\" to cancel)\n NOTE: Username cannot be changed once created: ", "Username")
    new_customer_email = validate_and_input_customer("Enter new customer email (type \"c\" to cancel): ", "Email")
    new_customer_name = input("Enter new customer name (type \"c\" to cancel): ")
    new_customer_phonenumber = input("Enter new customer phone number (type \"c\" to cancel): ")
    new_customer_dob = validate_and_input_customer("Enter new customer date of birth (type \"c\" to cancel): ", "dob")
    new_customer_address = input("Enter new customer address (type \"c\" to cancel): ")
    new_customer_password = validate_and_input_customer("Enter new customer password (type \"c\" to cancel): ", "Password")

    addusers = loaddatabase("users", "read")

    addusers[new_customer_username] = {
        "name": new_customer_name,
        "email": new_customer_email,
        "role": "customer",
        "PhoneNumber": new_customer_phonenumber,
        "DOB": new_customer_dob,
        "Address": new_customer_address
    }

    loaddatabase("users", "write", addusers)

    addpasswords = loaddatabase("passwords", "read")

    addpasswords[new_customer_username] = {
        "password": new_customer_password
    }

    loaddatabase("passwords", "write", addpasswords)

    print("Customer added successfully.")
    manage_customer()



def edit_customer_list(edit, new_value, type):
    if type == "password":
        editpasswords = loaddatabase("passwords", "read")

        editpasswords[edit][type] = {
            "password": new_value
        }

        loaddatabase("passwords", "write", editpasswords)

    editusers = loaddatabase("users", "read")

    editusers[edit][type] = new_value

    loaddatabase("users", "write", editusers)

    manage_customer()


def edit_customer():
    print("-" * 50)
    editusers = loaddatabase("users", "read")

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
            break
        elif editcustomerinfo == "2":
            print(f"Edit Email\nCurrent email: {editusers[user_nm]["email"]}")
            new_email = input("Enter new email: ")
            edit_customer_list(user_nm, new_email, "email")
            break
        elif editcustomerinfo == "3":
            print(f"Edit Phone Number\nCurrent phone number: {editusers[user_nm]["PhoneNumber"]}")
            new_phonenumber = input("Enter new phone number: ")
            edit_customer_list(user_nm, new_phonenumber, "PhoneNumber")
            break
        elif editcustomerinfo == "4":
            print(f"Edit Date of Birth\nCurrent date of birth: {editusers[user_nm]["DOB"]}")
            new_dob = input("Enter new date of birth: ")
            edit_customer_list(user_nm, new_dob, "DOB")
            break
        elif editcustomerinfo == "5":
            print(f"Edit Address\nCurrent address: {editusers[user_nm]["Address"]}")
            new_address = input("Enter new address: ")
            edit_customer_list(user_nm, new_address, "Address")
            break
        elif editcustomerinfo == "6":
            new_password = validate_and_input_customer("Enter new password: ", "Password")
            confirm_password = input("Confirm new password: ")
            if new_password != confirm_password:
                print("Passwords do not match")
                continue
            edit_customer_list(user_nm, new_password, "password")
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

        deleteusers = loaddatabase("users", "read")

        if user in deleteusers:
            del deleteusers[user]
            loaddatabase("users", "write", deleteusers)
        else:
            print("User not found")
            continue

        deletepasswords = loaddatabase("passwords", "read")

        if user in deletepasswords:
            del deletepasswords[user]
            loaddatabase("passwords", "write", deletepasswords)
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
    file = loaddatabase("menuItems", "read")

    new_menu_name = input("Enter the name of the new menu item: ")
    new_cuisine_type = input("Enter the cuisine type of the new menu item: ")
    while True:
        try:
            new_price = int(input("Enter the price of the new menu item: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number")
            continue
    new_category = input("Enter the category of the new menu item: ")

    new_item = {
        "MenuItmID": get_next_id(file, "BG-"),
        "Name": new_menu_name,
        "CuisineType": new_cuisine_type,
        "Price": new_price,
        "Category": new_category
    }
    file.append(new_item)

    loaddatabase("menuItems", "write", file)

    print("Menu item added successfully")
    manage_menuandpricing()


def edit_menu_list(type):
    print(f"Edit {type}\nCurrent {type.lower()}: {updated_menu[0][type]}")
    new_value = input(f"Enter new {type.lower()}: ")
    updated_menu[0][type] = new_value
    loaddatabase("menuItems", "write", updated_menu)
    print(f"{type} updated successfully.")
    manage_menuandpricing()


def edit_menu_item():
    print("-" * 50)
    print("Edit Menu Item")
    editmenu = loaddatabase("menuItems", "read")

    for i in range(len(editmenu)):
        print(f"{editmenu[i]['MenuItmID']} - {editmenu[i]['Name']}")

    while True:
        edit_menu_option = input("Enter menu item ID to edit: ").upper()
        global updated_menu
        updated_menu = [item for item in editmenu if item['MenuItmID'] == edit_menu_option]

        if len(updated_menu) == 0:
            print(f"Item with MenuItmID '{edit_menu_option}' not found.")
            continue
        else:
            print(f"Editing Menu Item: {edit_menu_option}")
            print(f"1: Edit Name\n2: Edit Cuisine Type\n3: Edit Price\n4: Edit Category\n5: Go Back")
            while True:
                editmenuitem = input("Choose an option from 1 to 5: ")
                if editmenuitem == "1":
                    edit_menu_list("Name")
                    break
                elif editmenuitem == "2":
                    edit_menu_list("CuisineType")
                    break
                elif editmenuitem == "3":
                    edit_menu_list("Price")
                    break
                elif editmenuitem == "4":
                    edit_menu_list("Category")
                    break


def delete_menu_item():
    print("-" * 50)
    print("Delete Menu Item")
    deletemenu = loaddatabase("menuItems", "read")

    for i in range(len(deletemenu)):
        print(f"{deletemenu[i]['MenuItmID']} - {deletemenu[i]['Name']}")

    while True:
        menu = input("Enter menu item ID to delete: ").upper()
        updated_menu = [item for item in deletemenu if item['MenuItmID'] != menu]

        if len(updated_menu) == len(deletemenu):
            print(f"Item with MenuItmID '{menu}' not found.")
            continue
        else:
            loaddatabase("menuItems", "write", updated_menu)
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
    ingredients = loaddatabase("ingredients", "read")
    print("Ingredients list requested by chef")
    pendingrequest = []
    for item in ingredients:
        if item['RequestStatus'] == "Pending":
            print(f"{item['RequestID']} - {item['Ingredient']['name']} - {item['Ingredient']['quantity']}{item['Ingredient']['unit']} - {item['RequestStatus']}")
            pendingrequest.append(item['RequestID'])
    while True:
        option = input("Enter the request ID to change the status of the request (type \"c\" to cancel): ").upper()
        if option == "C":
            start()
            break
        else:
            if option not in pendingrequest:
                print(f"Request ID '{option}' not found.")
                continue
            ingredient = next((item for item in ingredients if item['RequestID'] == option), None)
            if ingredient:
                print(f"Request ID: {ingredient['RequestID']}\nIngredient: {ingredient['Ingredient']['name']}\nQuantity: {ingredient['Ingredient']['quantity']}{ingredient['Ingredient']['unit']}\nRequest Status: {ingredient['RequestStatus']}")
                status = input("Enter the status of the request (Approved/Rejected): ").capitalize()
                if status == "Approved" or status == "Rejected":
                    ingredient['RequestStatus'] = status
                    loaddatabase("ingredients", "write", ingredients)
                    print(f"Request ID: {ingredient['RequestID']} - {ingredient['RequestStatus']}")
                    start()
                    break
                else:
                    print("Invalid input. Please type either 'Approved' or 'Rejected'")
                    continue
            else:
                print(f"Request ID '{option}' not found.")
                continue




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
            exit()
        else:
            print("Invalid input. Please type a number from 1 to 5")
            continue


start()
