import datetime
from Modules.utils import display_table, inp, clear_console, get_next_id, printD, wait_for_enter
from Modules.db import db_addKey, db_getKey, db_getAllKeys, db_deleteKey, _db_loadDB, _db_saveDB

         
# 0.1 Function to load and save database
def loaddatabase(database, type="read", data="none"):
    match type:
        case "read":
            return _db_loadDB(database)
        case "write":
            if data != "none":
                _db_saveDB(database, data)

                
# 0.2 Function to validate and input customer details
def validate_and_input_customer(prompt, type="string"):
    type = type.lower()
    match type:
        case "password":
            inp_value = inp(prompt, "password", cancelAllowed=True)
            return inp_value
        case "username":
            inp_value = inp(prompt, "string", cancelAllowed=True)
            data = loaddatabase("users", "read")
            if inp_value in data:
                print("Username already exists. Please choose a different username.")
                return validate_and_input_customer(prompt, type)
            else: 
                return inp_value
        case "email":
            inp_value = inp(prompt, "email", cancelAllowed=True)
            data = loaddatabase("users", "read")
            email_exists = False
            for entry in data.values():
                if entry.get("email") == inp_value:
                    email_exists = True
                    break
            if email_exists:
                print("Email already exists.")
                return validate_and_input_customer(prompt, type)
            else:
                return inp_value
        case "dob":
            inp_value = inp(prompt, "date", cancelAllowed=True)
            return inp_value
        case _:
            inp_value = inp(prompt, "string", cancelAllowed=True)
            return inp_value


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
    from main import register as register_main
    register_main(cur_usr, manage_customer)


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
                print(f"Edit Address\nCurrent address: {editusers[user_nm]["address"]}")
                edit_customer_list(cur_usr, "Enter new address: ", user_nm, "address")
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

    display_table(["No.", "Username", "Name", "Email", "Phone Number", "Date of Birth", "Address"], [(i + 1, customers[i]["username"], customers[i]["name"], customers[i]["email"], customers[i]["PhoneNumber"], customers[i]["DOB"], customers[i]["address"]) for i in range(len(customers))])

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
    file = loaddatabase("menu", "read")

    new_menu_name = input("Enter the name of the new menu item: ")
    new_cuisine_type = input("Enter the cuisine type of the new menu item: ")
    while True:
        try:
            new_price = float(input("Enter the price of the new menu item: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number")
            continue
    new_category = inp("Enter the category of the new menu item: ", "str", ["Main Course", "Appetizer", "Dessert", "Beverage", "Others"], stringUpperSensitive=True)

    new_item = {
        "name": new_menu_name,
        "cuisineType": new_cuisine_type,
        "price": new_price,
        "category": new_category.lower(),
        "available": True
    }
    
    new_item_id = get_next_id("menu", "MNI-")

    db_addKey("menu", new_item_id, new_item)

    print(f"Menu item {new_item_id} added successfully")
    manage_menuandpricing(cur_usr)


# 2.2 Function to edit menu item
def edit_menu_item(cur_usr, menuitem=""):
    print("Edit Menu Item")
    menu = loaddatabase("menu", "read")
    
    menuitems = []
    for key, value in menu.items():
        value["ID"] = key
        menuitems.append(value)

    goback = ""
    if menuitem:
        edit_menu_option = menuitem
        goback = "view"
    else:
        display_table(["Menu Item ID", "Name", "Cuisine Type", "Price", "Category", "Available"], [(menuitems[i]["ID"], menuitems[i]["name"], menuitems[i]["cuisineType"], menuitems[i]["price"], menuitems[i]["category"], "Yes" if menuitems[i]["available"] else "No") for i in range(len(menu))])

    while True:
        if not menuitem:
            edit_menu_option = input("Enter menu item ID to edit: ").upper()

        if len(menu) == 0:
            print(f"Item with MenuItmID '{edit_menu_option}' not found.")
            continue
        else:
            print(f"Editing Menu Item: {edit_menu_option}")
            print(f"1: Edit Name\n2: Edit Cuisine Type\n3: Edit Price\n4: Edit Category\n5: Go Back")
            option = inp("Choose an option from 1 to 5: ", "int", [1, 2, 3, 4, 5])
            menuitem = edit_menu_option
            match option:
                case 1:
                    edit_menu_list(cur_usr, "name", goback, menuitem)
                case 2:
                    edit_menu_list(cur_usr, "cuisineType", goback, menuitem)
                case 3:
                    edit_menu_list(cur_usr, "price", goback, menuitem)
                case 4:
                    edit_menu_list(cur_usr, "category", goback, menuitem)
                case 5:
                    manage_menuandpricing(cur_usr)


# 2.2.1 Function to edit menu list
def edit_menu_list(cur_usr, type: str, goback="", menuitem=""):
    menu = loaddatabase("menu", "read")

    currentvalue = menu[menuitem][type]
    print(f"Edit {type}\nCurrent {type.capitalize()}: {currentvalue}")

    new_value = input(f"Enter new {type.capitalize()}: ")

    if menu[menuitem]:
        if type.lower() == "price":
            menu[menuitem][type] = int(new_value)
        else:
            menu[menuitem][type] = new_value
        loaddatabase("menu", "write", menu)
        print(f"{type} updated successfully.")

    if goback == "view":
        view_menu(cur_usr)
    else:
        manage_menuandpricing(cur_usr)


# 2.3 Function to delete menu item
def delete_menu_item(cur_usr, goback="", menu=""):
    print("Delete Menu Item")
    deletemenu = loaddatabase("menu", "read")

    menuitems = db_getAllKeys("menu")
    menu_objs = []
    for item in menuitems:
        menuitem = db_getKey("menu", item)
        if menuitem is {}:
            continue
        else:
            menu_name = menuitem["name"]
            menu_cuisine = menuitem["cuisineType"]
            menu_price = menuitem["price"]
            menu_category = menuitem["category"]
            menu_available = menuitem["available"]
            menu_objs.append({"menuitem_id": item, "name": menu_name, "cuisineType": menu_cuisine,
                                  "price": menu_price, "category": menu_category, "available": menu_available})

    if not menu:
        if menu_objs is []:
            printD("No feedback available.", "red")
            manage_menuandpricing(cur_usr)
            return

        table_headers = ["Menu Item ID", "Name", "Cuisine Type", "Price", "Category", "Available"]
        table_data = []
        for menu_obj in menu_objs:
            available = "Yes" if menu_obj["available"] else "No"
            table_data.append([menu_obj["menuitem_id"], menu_obj["name"], menu_obj["cuisineType"], menu_obj["price"], menu_obj["category"], available])
        display_table(table_headers, table_data)

    while True:
        if not menu:
            menu = input("Enter menu item ID to delete: ").upper()

        if db_getKey("menu", menu) is None:
            print(f"Item with menu item ID '{menu}' not found.")
            menu = ""
            continue
        else:
            menu_delete_item = db_getKey("menu", menu)
            db_deleteKey("menu", menu)
            print(f"Menu item \"{menu} - {menu_delete_item["name"]}\" deleted.")
            if goback == "view":
                view_menu(cur_usr)
            else:
                manage_menuandpricing(cur_usr)


# 2.4 Function to view menu
def view_menu(cur_usr):
    print("View Menu")
    menu = loaddatabase("menu", "read")
    menuitems = []
    for key, value in menu.items():
        value["MenuItmID"] = key
        menuitems.append(value)

    display_table(["No.", "Menu Item ID", "Name", "Cuisine Type", "Price", "Category", "Available"], [(i + 1, menuitems[i]["MenuItmID"], menuitems[i]["name"], menuitems[i]["cuisineType"], menuitems[i]["price"], menuitems[i]["category"], "Yes" if menuitems[i]["available"] else "No") for i in range(len(menu))])
    while True:
        option = input("Enter the menu number to edit or delete (type \"c\" to cancel): ")

        if option.isnumeric():
            if 0 < int(option) <= len(menu):
                option2 = input("Do you want to edit or delete the menu item? (type \"e\" to edit, \"d\" to delete, \"c\" to cancel): ").lower()

                if option2 == "e":
                    edit_menu_item(cur_usr, menuitem=menuitems[int(option) - 1]["MenuItmID"])
                    break
                elif option2 == "d":
                    delete_menu_item(cur_usr, "view", menuitems[int(option) - 1]["MenuItmID"])
                    break
                else:
                    manage_menuandpricing(cur_usr)
                    break
            else:
                print(f"Invalid input. Please type a number from 1 to {len(menu)}")
                continue
        elif option.lower() == "c":
            manage_menuandpricing(cur_usr)
            break


# 3 Function to view ingredients list requested by chefs
def view_ingredientlist(cur_usr):
    ingredients_from_db = loaddatabase("ingredients", "read")
    ingredients = loaddatabase("ingredients", "read")
    pendingrequest = []
    pendingrequest_ids = []
    pendingrequest_ingr = {}
    for req in ingredients:
        if ingredients[req]['status'] == "pending":
            pendingrequest_ids.append(req)
            ingredients[req]["RequestID"] = req
            pendingrequest.append(ingredients[req])
            ingredients[req]["fmt_ingr"] = []
            for ingr in ingredients[req]['items']:
                ingredients[req]["fmt_ingr"].append(f"{ingr['name']} - {ingr['quantity']} {ingr['unit']}")
            pendingrequest_ingr = {item['RequestID']: ", ".join(item['fmt_ingr']) for item in pendingrequest}
    
    if len(pendingrequest) == 0:
        print("No pending ingredient requests found.")
        wait_for_enter()
        start(cur_usr)
    else:
        while True:
            clear_console()
            print("Pending Ingredient requests")
            table_headers = ["Request ID", "Ingredient-Quantity(Unit)","Request Status", "Requsted By", "Reviewed By"]
            table_data = [
                (
                    item['RequestID'],
                    pendingrequest_ingr.get(item['RequestID'], "N/A"), 
                    item.get('status', "N/A"),
                    item.get("request_chef", {}).get("user", "-"),
                    item.get("review_user", {}).get("user", "-")
                ) 
                for item in pendingrequest
            ]
            display_table(table_headers, table_data)
            option = input("Enter the request ID to change the status of the request (type \"c\" to cancel): ").upper()
            if option == "C":
                print("Cancelled.")
                wait_for_enter()
                start(cur_usr)
                break
            else:
                if option not in pendingrequest_ids:
                    print(f"Request ID '{option}' not found.")
                    continue
                
                selected_ing = ingredients[option]
                selected_ingredient = ingredients_from_db[option]
                if selected_ingredient:
                    print(f"Request ID: {selected_ing['RequestID']}\nRequested Items: {', '.join(selected_ing['fmt_ingr'])}\nRequest Status: {selected_ing.get('status', 'N/A')}\nRequested By: {selected_ing.get('request_chef', {}).get('user', '-')}\nReviewed By: {selected_ing.get('review_user', {}).get('user', '-')}")
                    status = input("Enter the status of the request (Approve/Reject): ").lower()
                    if status == "approve" or status == "reject":
                        selected_ingredient['status'] = "completed" if status == "approve" else "rejected"
                        selected_ingredient['review_user'] = {
                            "user": cur_usr,
                            "date": datetime.datetime.now().strftime('%d-%b-%Y'),
                            "time": datetime.datetime.now().strftime('%I:%M %p')
                        }
                        loaddatabase("ingredients", "write", ingredients_from_db)
                        print(f"Request ID: {selected_ing['RequestID']} - {selected_ingredient["status"].capitalize()} successfully.")
                        wait_for_enter()
                        start(cur_usr)
                        break
                    else:
                        print("Invalid input. Please type either 'Approved' or 'Rejected'")
                        wait_for_enter()
                        continue
                else:
                    print(f"Request ID '{option}' not found.")
                    wait_for_enter()
                    continue


# 4 Function to update own profile
def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)


# 5 Logout function
def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)


# 0 Start function
def start(cur_usr):
    clear_console()
    printD("Manager Menu", "magenta")
    print("1: Manage Customer\n2: Manage menu categories and pricing\n3: View ingredients list requested by chef\n4: Update own profile\n5: Logout")

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