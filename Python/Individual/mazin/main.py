import re


def validate_and_input(prompt, index, type="string"):
    while True:
        inp_value = input(prompt)
        if inp_value == "c":
            manage_customer()
        if "," in inp_value:
            if index == 0:
                print("Username should not contain commas")
                continue
            elif index == 1:
                print("Email should not contain commas")
                continue
            elif index == 2:
                print("Name should not contain commas")
                continue
            elif index == 3:
                print("Password should not contain commas")
                continue

        customer_file_r = open("customer_list", "r")
        customer_file_r = list(customer_file_r)
        records = []
        if type == "pwd":
            if re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", inp_value):
                return inp_value
            else:
                print(
                    "Password must be at least 8 characters long and contain at least one letter and one number and "
                    "should not contain any commas")
        else:
            if type == "username" or type == "email":
                for line in customer_file_r:
                    records.append(line.split(", ")[index])
                if inp_value in records:
                    print("Record already exists")
                else:
                    if type == "email":
                        if re.match(r"[^@]+@[^@]+\.[^@]+", inp_value):
                            return inp_value
                        else:
                            print("Invalid email")
                    else:
                        return inp_value
        if type == "fullname":
            return inp_value


def add_customer():
    print("-" * 50)
    new_customer_username = validate_and_input("Enter new customer username (type \"c\" to cancel): ", 0, "username")
    new_customer_email = validate_and_input("Enter new customer email (type \"c\" to cancel): ", 1, "email")
    new_customer_name = validate_and_input("Enter new customer name (type \"c\" to cancel): ", 2,"fullname")
    new_customer_password = validate_and_input("Enter new customer password (type \"c\" to cancel): ", 3, "pwd")
    customer_file = open("customer_list", "a")
    customer_file.write(
        f"\n{new_customer_username.lower()}, {new_customer_email.lower()}, {new_customer_name}, {new_customer_password}, customer")
    customer_file.close()
    print("New customer added")
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

    print(f"Edit user: {listofcustimers[edit_customer_num]}")
    splitcustomerinfo = listofcustimers[edit_customer_num].split(", ")

    print("-" * 50)
    print("1: Edit username")
    print("2: Edit email")
    print("3: Edit name")
    print("4: Edit password")
    print("5: Go Back")
    edit_customer_detail = input("Choose an option from 1 to 4: ")

    if edit_customer_detail == "1":
        print("-" * 50)
        print("Edit username")
        new_username = validate_and_input("Enter new username (type \"c\" to cancel): ", 0, "username")

        edit_customer_list(splitcustomerinfo[0], 0, new_username)

        print("Username has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "2":
        print("-" * 50)
        print("Edit email")
        new_email = validate_and_input("Enter new email (type \"c\" to cancel): ", 1, "email")

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
        new_password = validate_and_input("Enter new password (type \"c\" to cancel): ", 3, "pwd")

        edit_customer_list(splitcustomerinfo[0], 3, new_password)

        print("Password has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "5":
        manage_customer()
    else:
        print("Invalid input")
        manage_customer()


def delete_customer():
    print("-" * 50)
    global user_nm
    user = input("Enter username to delete: ")
    user = user.lower()
    customer_file = open("customer_list", "r")
    customer_file = list(customer_file)
    for line in customer_file:
        if user == line.split(", ")[0]:
            user_nm = line.split(", ")[0]
            del customer_file[customer_file.index(line)]
        else:
            print("User not found")

    with open("customer_list", "w") as f:
        for customer in customer_file:
            f.write(f"{customer}")

    print(f"Deleted user: {user_nm}")
    manage_customer()


def manage_customer():
    print("-" * 50)
    print("Manage Customer")
    print("1: Add Customer")
    print("2: Edit Customer")
    print("3: Delete Customer")
    print("4: Go Back")

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


def manage_menuandpricing():
    print("-" * 50)
    print("Manage menu categories and pricing")
    print("1: Add Menu Item")
    print("2: Edit Menu Item")
    print("3: Delete Menu Item")
    print("4: Go Back")
    manage_menuandpricing_option = input("Choose an option from 1 to 4: ")

    while True:
        if manage_menuandpricing_option == "1":
            print("Add Menu Item")
            break
        elif manage_menuandpricing_option == "2":
            print("Edit Menu Item")
            break
        elif manage_menuandpricing_option == "3":
            print("Delete Menu Item")
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


def start():
    print("-" * 50)
    print("Manager Menu")
    print("1: Manage Customer")
    print("2: Manage menu categories and pricing")
    print("3: View ingredients list requested by chef")
    print("4: Update own profile")

    while True:
        option = input("Choose an option from 1 to 4: ")
        if option == "1":
            manage_customer()
            break
        elif option == "2":
            manage_menuandpricing()
        elif option == "3":
            view_ingredientlist()
        elif option == "4":
            updateprofile()
        else:
            print("Invalid input. Please type a number from 1 to 4")
            continue


start()
