import re
import datetime
import json
from Modules.functions import display_table, inp, clear_console
from Modules.db import db_addKey, db_getKey, db_updateKey, db_getAllKeys, db_getAllValues, db_deleteKey


def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)


def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)


# 0 Function to load database
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


# 0 Function to validate and input customer information
def validate_and_input_customer(prompt, type="string"):
    while True:
        inp_value = input(prompt)
        if inp_value == "c":
            manage_customer()

        data = loaddatabase("users", "read")

        if type == "Password":
            if re.match(r"[A-Za-z0-9@#$%^&+=]{8,}", inp_value):
                confirm_password = input("Confirm password: ")
                if inp_value != confirm_password:
                    print("Passwords do not match")
                    continue
                else:
                    return inp_value
            else:
                print("Password must be at least 8 characters long and contain at least one letter and one number")
                continue

        if type == "Username":
            if inp_value in data:
                print("Username already exists. Please choose a different username.")
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
                print("Incorrect date format, should be DD/MM/YYYY")

        if type == "string":
            return inp_value


# 0 Function to get next ID
def get_next_id(filename, prefix):
    if not filename:
        return f"{prefix}01"
    ids = [int(item["MenuItmID"].split('-')[1]) for item in filename]
    next_id_num = max(ids) + 1
    return f"{prefix}{next_id_num:02d}"


# 1 Function to manage customer
def manage_customer(cur_usr):
    clear_console()
    print("Manage Customer\n1: Add Customer\n2: Edit Customer\n3: Delete Customer\n4: View Customer List\n5: Go Back")

    option = inp("Choose an option from 1 to 5: ", "int", [1, 2, 3, 4, 5])
    match option:
        case 1:
            add_customer(cur_usr)
        case 2:
            edit_customer(cur_usr)
        case 3:
            delete_customer(cur_usr)
        case 4:
            view_customer_list(cur_usr)
        case 5:
            start(cur_usr)


# 1.1 Function to add customer
def add_customer(cur_usr):
    new_customer_username = validate_and_input_customer(
        "Enter new customer username (type \"c\" to cancel). NOTE: Username cannot be changed once created: ",
        "Username")
    new_customer_email = validate_and_input_customer("Enter new customer email (type \"c\" to cancel): ", "Email")
    new_customer_name = validate_and_input_customer("Enter new customer name (type \"c\" to cancel): ", "Name")
    new_customer_phonenumber = validate_and_input_customer("Enter new customer phone number (type \"c\" to cancel): ")
    new_customer_dob = validate_and_input_customer("Enter new customer date of birth (type \"c\" to cancel): ", "dob")
    new_customer_address = validate_and_input_customer("Enter new customer address (type \"c\" to cancel): ")
    new_customer_password = validate_and_input_customer("Enter new customer password (type \"c\" to cancel): ",
                                                        "Password")

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
    manage_customer(cur_usr)


# 1.2 Function to edit customer
def edit_customer(cur_usr, username=""):
    editusers = loaddatabase("users", "read")

    if username:
        user_nm = username
    else:
        listofcustimers = []
        for key, value in editusers.items():
            if value["role"] == "customer":
                listofcustimers.append(f"{key}")
        n = len(listofcustimers)

        if n == 0:
            print("No customers found")
            manage_customer(cur_usr)

        print("Edit Customer")
        display_table(["No.", "Username"], [(i + 1, listofcustimers[i]) for i in range(n)])

    while True:
        if not username:
            edit_customer_option = input("Choose a customer to edit (type \"c\" to cancel): ")
            if edit_customer_option == "c":
                manage_customer(cur_usr)
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
        else:
            break

    print(f"Edit Customer: {user_nm}")
    print(
        "1: Edit Name\n2: Edit Email\n3: Edit Phone Number\n4: Edit Date of Birth\n5: Edit Address\n6: Edit Password\n7: Go Back")

    while True:
        option = inp("Choose an option from 1 to 7: ", "int", [1, 2, 3, 4, 5, 6, 7])
        match option:
            case 1:
                print(f"Edit Name\nCurrent name: {editusers[user_nm]["name"]}")
                edit_customer_list(cur_usr, "Enter new name: ", user_nm, "name")
            case 2:
                print(f"Edit Email\nCurrent email: {editusers[user_nm]["email"]}")
                edit_customer_list(cur_usr, "Enter new email: ", user_nm, "email")
            case 3:
                print(f"Edit Phone Number\nCurrent phone number: {editusers[user_nm]["PhoneNumber"]}")
                edit_customer_list(cur_usr, "Enter new phone number: ", user_nm, "PhoneNumber")
            case 4:
                print(f"Edit Date of Birth\nCurrent date of birth: {editusers[user_nm]["DOB"]}")
                edit_customer_list(cur_usr, "Enter new date of birth: ", user_nm, "DOB")
            case 5:
                print(f"Edit Address\nCurrent address: {editusers[user_nm]["Address"]}")
                edit_customer_list(cur_usr, "Enter new address: ", user_nm, "Address")
            case 6:
                edit_customer_list(cur_usr, "Enter new password: ", user_nm, "password")
            case 7:
                if username:
                    view_customer_list(cur_usr)
                else:
                    manage_customer(cur_usr)


# 1.2.1 Function to edit customer list
def edit_customer_list(cur_usr, prompt, edit, type):
    if type == "password":
        while True:
            new_password = validate_and_input_customer("Enter new password: ", "Password")
            confirm_password = input("Confirm new password: ")
            if new_password != confirm_password:
                print("Passwords do not match")
                continue
            else:
                break

        editpasswords = loaddatabase("passwords", "read")

        editpasswords[edit]["password"] = new_password

        loaddatabase("passwords", "write", editpasswords)

        manage_customer(cur_usr)
    else:
        new_value = input(prompt)
        editusers = loaddatabase("users", "read")

        editusers[edit][type] = new_value

        loaddatabase("users", "write", editusers)

        manage_customer(cur_usr)


# 1.3 Function to delete customer
def delete_customer(cur_usr, username=""):
    print("Delete Customer")

    customers = []
    users = loaddatabase("users", "read")
    for key, value in users.items():
        if value["role"] == "customer":
            customers.append(key)

    if len(customers) == 0:
        print("No customers found")
        manage_customer(cur_usr)

    if not username:
        display_table(["No.", "Username"], [(i + 1, customers[i]) for i in range(len(customers))])

    while True:
        if not username:
            user = input("Enter username to delete (type \"c\" to cancel): ").lower()
            if user == "c":
                manage_customer(cur_usr)
            if user not in customers:
                print("User not found. Please enter a valid username.")
                continue

        user = username if username else user
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
            if username:
                view_customer_list(cur_usr)
            else:
                manage_customer(cur_usr)


# 1.4 Function to view customer list
def view_customer_list(cur_usr):
    print("View Customer List")
    users = loaddatabase("users", "read")
    customers = []
    for key, value in users.items():
        if value["role"] == "customer":
            value["username"] = key
            customers.append(value)

    if len(customers) == 0:
        print("No customers found")
        manage_customer(cur_usr)

    display_table(["No.", "Username", "Name", "Email", "Phone Number", "Date of Birth", "Address"], [(i + 1,
                                                                                                      customers[i][
                                                                                                          "username"],
                                                                                                      customers[i][
                                                                                                          "name"],
                                                                                                      customers[i][
                                                                                                          "email"],
                                                                                                      customers[i][
                                                                                                          "PhoneNumber"],
                                                                                                      customers[i][
                                                                                                          "DOB"],
                                                                                                      customers[i][
                                                                                                          "Address"])
                                                                                                     for i in range(
            len(customers))])

    while True:
        option = input("Enter the customer number to edit or delete (type \"c\" to cancel): ")

        if option.isnumeric():
            if 0 < int(option) <= len(customers):
                option2 = input(
                    "Do you want to edit or delete the customer? (type \"e\" to edit, \"d\" to delete, \"c\" to cancel): ").lower()

                if option2 == "e":
                    option = int(option)
                    if 0 < option <= len(customers):
                        edit_customer(cur_usr, customers[option - 1]["username"])
                        break
                    else:
                        print(f"Invalid input. Please type a number from 1 to {len(customers)}")
                        continue
                elif option2 == "d":
                    if option.isnumeric():
                        option = int(option)
                        if 0 < option <= len(customers):
                            delete_customer(cur_usr, customers[option - 1]["username"])
                            break
                        else:
                            print(f"Invalid input. Please type a number from 1 to {len(customers)}")
                            continue
                    else:
                        manage_customer(cur_usr)
                        break
        else:
            manage_customer(cur_usr)
            break


# 2 Function to manage menu and pricing
def manage_menuandpricing(cur_usr):
    print(
        "Manage menu categories and pricing\n1: Add Menu Item\n2: Edit Menu Item\n3: Delete Menu Item\n4: View Menu\n5: Go Back")

    option = inp("Choose an option from 1 to 5: ", "int", [1, 2, 3, 4, 5])
    match option:
        case 1:
            add_menu(cur_usr)
        case 2:
            edit_menu_item(cur_usr)
        case 3:
            delete_menu_item(cur_usr)
        case 4:
            view_menu(cur_usr)
        case 5:
            start(cur_usr)


# 2.1 Function to add menu item
def add_menu(cur_usr):
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
    manage_menuandpricing(cur_usr)


# 2.2.1 Function to edit menu list
def edit_menu_list(cur_usr, type, goback="", menuitem=""):
    editmenu = loaddatabase("menuItems", "read")
    currentvalue = next((item[type] for item in editmenu if item['MenuItmID'] == menuitem), None)
    print(f"Edit {type}\nCurrent {type.lower()}: {currentvalue}")

    new_value = input(f"Enter new {type.lower()}: ")

    for item in editmenu:
        if item['MenuItmID'] == menuitem:
            item[type] = new_value
            loaddatabase("menuItems", "write", editmenu)
            print(f"{type} updated successfully.")
            break

    if goback == "view":
        view_menu(cur_usr)
    else:
        manage_menuandpricing(cur_usr)


# 2.2 Function to edit menu item
def edit_menu_item(cur_usr, menuitem=""):
    print("Edit Menu Item")
    editmenu = loaddatabase("menuItems", "read")

    if menuitem:
        edit_menu_option = menuitem
        goback = "view"
    else:
        for i in range(len(editmenu)):
            print(f"{editmenu[i]['MenuItmID']} - {editmenu[i]['Name']}")

    while True:
        if not menuitem:
            edit_menu_option = input("Enter menu item ID to edit: ").upper()

        if len(editmenu) == 0:
            print(f"Item with MenuItmID '{edit_menu_option}' not found.")
            continue
        else:
            print(f"Editing Menu Item: {edit_menu_option}")
            print(f"1: Edit Name\n2: Edit Cuisine Type\n3: Edit Price\n4: Edit Category\n5: Go Back")
            option = inp("Choose an option from 1 to 5: ", "int", [1, 2, 3, 4, 5])
            menuitem = edit_menu_option
            match option:
                case 1:
                    edit_menu_list(cur_usr, "Name", goback, menuitem)
                case 2:
                    edit_menu_list(cur_usr, "CuisineType", goback, menuitem)
                case 3:
                    edit_menu_list(cur_usr, "Price", goback, menuitem)
                case 4:
                    edit_menu_list(cur_usr, "Category", goback, menuitem)
                case 5:
                    manage_menuandpricing(cur_usr)


# 2.3 Function to delete menu item
def delete_menu_item(cur_usr, menu=""):
    print("Delete Menu Item")
    deletemenu = loaddatabase("menuItems", "read")

    if not menu:
        for i in range(len(deletemenu)):
            print(f"{deletemenu[i]['MenuItmID']} - {deletemenu[i]['Name']}")

    while True:
        if not menu:
            menu = input("Enter menu item ID to delete: ").upper()

        updated_menu = [item for item in deletemenu if item['MenuItmID'] != menu]

        if len(updated_menu) == len(deletemenu):
            print(f"Item with MenuItmID '{menu}' not found.")
            continue
        else:
            loaddatabase("menuItems", "write", updated_menu)
            item_to_delete = next((item for item in deletemenu if item['MenuItmID'] == menu), None)
            print(f"Menu item \"{menu} - {item_to_delete['Name']}\" deleted.")
            if not menu:
                manage_menuandpricing(cur_usr)
            else:
                view_menu(cur_usr)


# 2.4 Function to view menu
def view_menu(cur_usr):
    print("View Menu")
    menu = loaddatabase("menuItems", "read")
    display_table(["No.", "Menu Item ID", "Name", "Cuisine Type", "Price", "Category"], [
        (i + 1, menu[i]["MenuItmID"], menu[i]["Name"], menu[i]["CuisineType"], menu[i]["Price"], menu[i]["Category"])
        for i in range(len(menu))])

    while True:
        option = input("Enter the menu number to edit or delete (type \"c\" to cancel): ")

        if option.isnumeric():
            if 0 < int(option) <= len(menu):
                option2 = input(
                    "Do you want to edit or delete the menu item? (type \"e\" to edit, \"d\" to delete, \"c\" to cancel): ").lower()

                if option2 == "e":
                    edit_menu_item(cur_usr, menu[int(option) - 1]["MenuItmID"])
                    break
                elif option2 == "d":
                    delete_menu_item(cur_usr, menu[int(option) - 1]["MenuItmID"])
                    break
                else:
                    manage_menuandpricing(cur_usr)
                    break
            else:
                print(f"Invalid input. Please type a number from 1 to {len(menu)}")
                continue


# 3 Function to view ingredients list requested by chef
def view_ingredientlist(cur_usr):
    print("View ingredients list requested by chef")
    ingredients = loaddatabase("ingredients", "read")
    print("Ingredients list requested by chef")
    pendingrequest = []
    for item in ingredients:
        if item['RequestStatus'] == "Pending":
            pendingrequest.append(item['RequestID'])

    display_table(["Request ID", "Ingredient", "Quantity", "Request Status"], [(item['RequestID'],
                                                                                item['Ingredient']['name'],
                                                                                f"{item['Ingredient']['quantity']}{item['Ingredient']['unit']}",
                                                                                item['RequestStatus']) for item in
                                                                               ingredients if
                                                                               item['RequestStatus'] == "Pending"])

    while True:
        option = input("Enter the request ID to change the status of the request (type \"c\" to cancel): ").upper()
        if option == "C":
            start(cur_usr)
            break
        else:
            if option not in pendingrequest:
                print(f"Request ID '{option}' not found.")
                continue
            ingredient = next((item for item in ingredients if item['RequestID'] == option), None)
            if ingredient:
                print(
                    f"Request ID: {ingredient['RequestID']}\nIngredient: {ingredient['Ingredient']['name']}\nQuantity: {ingredient['Ingredient']['quantity']}{ingredient['Ingredient']['unit']}\nRequest Status: {ingredient['RequestStatus']}")
                status = input("Enter the status of the request (Approved/Rejected): ").capitalize()
                if status == "Approved" or status == "Rejected":
                    ingredient['RequestStatus'] = "Completed"
                    loaddatabase("ingredients", "write", ingredients)
                    ingredient['ReviewedBy'] = {
                        "User": cur_usr,
                        "Status": status,
                        "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "Time": datetime.datetime.now().strftime("%H:%M")
                    }

                    loaddatabase("ingredients", "write", ingredients)
                    print(
                        f"Request ID: {ingredient['RequestID']} - {ingredient['RequestStatus']} - Reviewed by {ingredient['ReviewedBy']['User']} on {ingredient['ReviewedBy']['Date']} at {ingredient['ReviewedBy']['Time']}")
                    start(cur_usr)
                    break
                else:
                    print("Invalid input. Please type either 'Approved' or 'Rejected'")
                    continue
            else:
                print(f"Request ID '{option}' not found.")
                continue


# 0 Start function
def start(cur_usr):
    print(
        "Manager Menu\n1: Manage Customer\n2: Manage menu categories and pricing\n3: View ingredients list requested by chef\n4: Update own profile\n5: Logout")

    option = inp("Choose an option from 1 to 5: ", "int", [1, 2, 3, 4, 5])
    match option:
        case 1:
            manage_customer(cur_usr)
        case 2:
            manage_menuandpricing(cur_usr)
        case 3:
            view_ingredientlist(cur_usr)
        case 4:
            update_profile(cur_usr, start)
        case 5:
            logout(cur_usr)