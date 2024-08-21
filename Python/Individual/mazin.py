import re


def validate_and_input(prompt, index, type="string"):
    while True:
        inp_value = input(prompt)
        if "," in inp_value:
            if index == 0:
                print("Username should not contain ,")
                continue
            elif index == 1:
                print("Email should not contain ,")
                continue
            elif index == 2:
                print("Name should not contain ,")
                continue
            elif index == 3:
                print("Password should not contain ,")
                continue

        customer_file_r = open("customer_list", "r")
        customer_file_r = list(customer_file_r)
        records = []
        if type == "pwd":
            if re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", inp_value):
                return inp_value
            else:
                print(
                    "Password must be at least 8 characters long and contain at least one letter and one number and should not contain any ,")
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
        return inp_value


def add_customer():
    print("-" * 50)
    new_customer_username = validate_and_input("Enter new customer username: ", 0, "username")
    new_customer_email = validate_and_input("Enter new customer email: ", 1, "email")
    new_customer_name = validate_and_input("Enter new customer name: ", 2)
    new_customer_password = validate_and_input("Enter new customer password: ", 3, "pwd")
    customer_file = open("customer_list", "a")
    customer_file.write(
        f"\n{new_customer_username.lower()}, {new_customer_email.lower()}, {new_customer_name}, {new_customer_password}, customer")
    customer_file.close()
    print("New customer added")
    manage_customer()


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
    edit_customer_num = int(input(f"Choose a customer to edit from 1 to {n}: ")) - 1
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
        new_username = validate_and_input("Enter new username: ", 0)

        file = open("customer_list", "r")
        lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(splitcustomerinfo[0]):
                customer_info = line.split(", ")
                customer_info[0] = new_username
                lines[i] = ", ".join(customer_info)

        file = open("customer_list", "w")
        file.writelines(lines)
        print("Username has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "2":
        print("-" * 50)
        print("Edit email")
        new_email = validate_and_input("Enter new email: ", 1, "email")

        file = open("customer_list", "r")
        lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(splitcustomerinfo[0]):
                customer_info = line.split(", ")
                customer_info[1] = new_email
                lines[i] = ", ".join(customer_info)

        file = open("customer_list", "w")
        file.writelines(lines)
        print("Email has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "3":
        print("-" * 50)
        print("Edit name")
        new_name = input("Enter new name: ")

        file = open("customer_list", "r")
        lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(splitcustomerinfo[0]):
                customer_info = line.split(", ")
                customer_info[2] = new_name
                lines[i] = ", ".join(customer_info)

        file = open("customer_list", "w")
        file.writelines(lines)
        print("Name has been changed successfully.")
        manage_customer()

    elif edit_customer_detail == "4":
        print("-" * 50)
        print("Edit password")
        new_password = validate_and_input("Enter new password: ", 3, "pwd")

        file = open("customer_list", "r")
        lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(splitcustomerinfo[0]):
                customer_info = line.split(", ")
                customer_info[3] = new_password
                lines[i] = ", ".join(customer_info)

        file = open("customer_list", "w")
        file.writelines(lines)
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
    manage_customer_option = input("Choose an option from 1 to 4: ")

    if manage_customer_option == "1":
        add_customer()
    elif manage_customer_option == "2":
        edit_customer()
    elif manage_customer_option == "3":
        delete_customer()
    elif manage_customer_option == "4":
        start()
    else:
        print("Invalid input")


def manage_menuandpricing():
    print("-" * 50)
    print("Manage menu categories and pricing")
    print("1: Add Menu Item")
    print("2: Edit Menu Item")
    print("3: Delete Menu Item")
    print("4: Go Back")
    manage_menuandpricing_option = input("Choose an option from 1 to 4: ")

    if manage_menuandpricing_option == "1":
        print("Add Menu Item")
    elif manage_menuandpricing_option == "2":
        print("Edit Menu Item")
    elif manage_menuandpricing_option == "3":
        print("Delete Menu Item")
    elif manage_menuandpricing_option == "4":
        start()
    else:
        print("Invalid input")


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
    option = input("Choose an option from 1 to 4: ")

    if option == "1":
        manage_customer()
    elif option == "2":
        manage_menuandpricing()
    elif option == "3":
        view_ingredientlist()
    elif option == "4":
        updateprofile()
    else:
        print("Invalid input")


start()
