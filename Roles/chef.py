import json
from datetime import datetime
from tabulate import tabulate

# Import common functions from functions.py
from Modules.utils import inp, printD, color_text, get_next_id

TABLE_FORMAT = "rounded_outline"  # The table format to be displayed

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# PATHS
ORDERS = "Data/orders.json"
INGREDIENTS = "Data/Ingredients.json"


# 0 - Start function
def start(cur_usr):
    while True:
        printD(f"Chef menu", "magenta", True)
        print(
            "1. View orders placed by customers. \n2. Update orders \n3. Request ingredients \n4. Update own profile. "
            "\n5. Logout")

        option = inp("Choose an option from 1 to 5: ", "int", [1, 2, 3, 4, 5])
        match option:
            case 1:
                show_orders(cur_usr)
            case 2:
                update_order_status(cur_usr)
            case 3:
                request_ingredients(cur_usr)
            case 4:
                update_profile(cur_usr, start)
            case 5:
                logout(cur_usr)


# 1 - Display orders in a grid format
def show_orders(current_user, active=True):
    orders = get_orders() if active else get_orders(active=False)
    if not orders:  # Checking the truthy value of orders to make sure it's not empty
        printD("No orders :D", "green", True)
        return False

    headers = ["Order ID", "Item ID", "Quantity"]
    rows = []

    # Preparing row data
    for order in orders:
        # Add the first item with the order ID
        for index, item in enumerate(order["items"]):
            if index == 0:
                color = "green" if order['status'] in ["Completed", "Delivered"] else "red"
                order_id = color_text(order['order_id'], color, True)
                rows.append([order_id, item['ID'], item['quantity']])
            else:
                # For subsequent items, leave the order ID blank
                rows.append(["", item['ID'], item['quantity']])
        rows.append(["-----------", "----------", "---------"])  # Creates a separator between orders
    rows.pop()  # removing last separator for the final order

    print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    return True


# 1.0.1 - Function to get the current date and time in the formats 05-Sep-2024 and 10:30 PM respectively
def time_object():
    now = datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')


# 1.0.2 - Function to retrieve active orders and all orders from the database
def get_orders(original=False, active=True):
    try:
        with open(ORDERS) as file:
            orders_object = json.load(file)
    except json.JSONDecodeError as e:
        printD(f"Error reading JSON file: {e}", "red", True)
        return {}
    except Exception as e:
        printD(f"Error: {e}", "red", True)
        return {}
    if original:
        return orders_object
    if active:
        return [
            {"order_id": order, "items": orders_object[order]["details"]["items"],
             "status": orders_object[order]["status"]}
            for order in orders_object if orders_object[order]["status"] not in ["Completed", "Delivered"]
        ]
    else:
        return [
            {"order_id": order, "items": orders_object[order]["details"]["items"],
             "status": orders_object[order]["status"]}
            for order in orders_object
        ]


# 1.0.3 - Function to save orders to the database
def save_orders(orders):
    with open(ORDERS, "w") as file:
        json.dump(orders, file, indent=4)


# 2 - Update order status to "Completed" or "Delivered" depending on dining option and cannot be undone.
def update_order_status(current_user):
    if show_orders(current_user, False):
        orders_object = get_orders(original=True)
        order_id = input("\nPlease input the order ID to mark as completed\nOrder ID: ").upper()
        if order_id not in orders_object:
            printD("Invalid Order ID", "red", True)
            return update_order_status(current_user)
        else:
            dining_option = orders_object[order_id]["details"]["diningOption"]
            orders_object[order_id]["status"] = "Completed" if dining_option == "Dine-in" else "Delivered"
            orders_object[order_id]["chef"] = current_user
            orders_object[order_id]["time"] = time_object()[1]
            orders_object[order_id]["date"] = time_object()[0]
            save_orders(orders_object)


# 3 - Request ingredients and update the quantity
def request_ingredients(current_user):
    requested_items = list()  # A set to keep track of requests made by the user
    handle_request_options(current_user, requested_items)


# 3.1 - Handle request options for adding/editing/deleting ingredients
def handle_request_options(current_user, requested_ingredients: list):
    while True:
        show_requests(requested_ingredients)
        try:
            option = int(
                input("\n1. Add ingredient\n2. Edit ingredient\n3. Delete ingredient\n4. Complete request\nOption: "))
            if option not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            printD("\nInvalid option", "red", True)
            continue

        if option == 1:
            add_ingredient(requested_ingredients, current_user)
        elif option == 2:
            edit_request(requested_ingredients, current_user)
        elif option == 3:
            delete_request(requested_ingredients, current_user)
        elif option == 4:
            complete_request(requested_ingredients, current_user)


# 3.1.1 - Add a new ingredient to the request
def add_ingredient(requested_ingredients: list, current_user):
    item_name = input("Enter the name of the ingredient you'd like to request: ")
    item_unit = input("Unit of measure: ")
    try:
        item_quantity = int(input("Quantity number: "))
        if item_quantity < 1:
            raise ValueError
    except ValueError:
        printD("\nInvalid quantity", "red", True)
        return add_ingredient(requested_ingredients)

    requested_ingredient = {
        "name": item_name,
        "quantity": item_quantity,
        "unit": item_unit
    }

    requested_ingredients.append(requested_ingredient)
    printD(f"Added {item_name} to the request", "green", True)
    handle_request_options(current_user, requested_ingredients)


# 3.1.2 - Edit an existing request
def edit_request(requested_ingredients: list, current_user):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("\nChoose an ingredient to edit: "))
        if item_number > len(requested_ingredients) or item_number < 1:
            raise ValueError
    except ValueError:
        printD("\nInvalid Item ID", "red", True)
        return edit_request(requested_ingredients)

    item_name = requested_ingredients[item_number - 1]["name"]
    try:
        new_quantity = int(input("New Quantity: "))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        printD("\nInvalid quantity", "red", True)
        return edit_request(requested_ingredients)

    printD(
        f"Changed quantity of {item_name} from {requested_ingredients[item_number - 1]['quantity']} to {new_quantity}",
        "green", True)

    requested_ingredients[item_number - 1]["quantity"] = new_quantity
    handle_request_options(current_user, requested_ingredients)


# 3.1.3 - Delete an existing request
def delete_request(requested_ingredients: list, current_user):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("Choose the ingredient to delete: "))
        if item_number > len(requested_ingredients) or item_number < 1:
            raise ValueError
    except ValueError:
        printD("\nInvalid Item ID", "red", True)
        return delete_request(requested_ingredients)

    item_name = requested_ingredients[item_number - 1]["name"]
    printD(f"Deleted {item_name} from the request", "green", True)
    requested_ingredients.pop(item_number - 1)
    handle_request_options(current_user, requested_ingredients)


# 3.1.4 - Complete the request by creating a boilerplate
def complete_request(requested_items, current_user):
    request_id = get_next_id("ingredients", prefix="ING")
    date, time = time_object()
    request_object = {
        "status": "pending",
        "items": requested_items,
        "request_chef": {"user": current_user, "date": date, "time": time},
        "review_user": {"user": "", "date": "", "time": ""}
    }
    add_request_to_file(request_id, request_object)
    printD(f"\nRequest with id {request_id} was successfully submitted :D", "green", True)
    start(current_user)


# 3.2 - Display ingredient requests
def show_requests(requests):
    if len(requests) != 0:
        headers = ["#", "Ingredient", "Quantity", "Measure (Unit)"]
        rows = [[i + 1, ingredient["name"], ingredient["quantity"], ingredient["unit"]] for i, (ingredient) in
                enumerate(requests)]
        print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    else:
        printD("\nNo requests made :D", "green", True)


# 3.3 - Add a complete request to the file
def add_request_to_file(request_id, request_object):
    try:
        with open(INGREDIENTS) as file:
            requests = json.load(file)
    except json.JSONDecodeError as e:
        printD(f"Error reading JSON file: {e}", "red", True)
        return
    except Exception as e:
        printD(f"Error: {e}", "red", True)
        return

    requests[request_id] = request_object

    with open(INGREDIENTS, "w") as file:
        json.dump(requests, file, indent=4)


# 4 - Update profile function
def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)


TABLE_FORMAT = "rounded_outline"  # The table format to be displayed

# Import common functions from functions.py
from Modules.utils import inp, printD, get_next_id

# 0 - Start function
def start(cur_usr):
    while True:
        printD(f"Chef menu", "magenta", True)
        print("1. View orders placed by customers. \n2. Update orders \n3. Request ingredients \n4. Update own profile. \n5. Logout")

        option = inp("Choose an option from 1 to 5: ", "int", [1, 2, 3, 4, 5])
        match option:
            case 1:
                show_orders(cur_usr)
            case 2:
                update_order_status(cur_usr)
            case 3:
                request_ingredients(cur_usr)
            case 4:
                update_profile(cur_usr, start)
            case 5:
                logout(cur_usr)

# 1 - Display orders in a grid format
def show_orders(current_user):
    orders = get_orders()
    if not orders:  # Checking the truthy value of orders to make sure it's not empty
        print("No orders :D")
        return False

    headers = ["Order ID", "Item ID", "Quantity"]
    rows = []

    # Preparing row data
    for order in orders:
        # Add the first item with the order ID
        for index, item in enumerate(order["items"]):
            if index == 0:
                rows.append([order['order_id'], item['ID'], item['quantity']])
            else:
                # For subsequent items, leave the order ID blank
                rows.append(["", item['ID'], item['quantity']])
        rows.append(["-----------", "----------", "---------"])  # Creates a separator between orders
    rows.pop()  # removing last separator for the final order

    print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    return True

# 1.0.1 - Function to get the current date and time in the formats 05-Sep-2024 and 10:30 PM respectively
def time_object():
    now = datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')

# 1.0.2 - Function to retrieve active orders from the database
def get_orders():
    try:
        with open("Data/orders.json", "r") as file:
            orders_object = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}
    return [
        {"order_id": order, "items": orders_object[order]["details"]["items"]}
        for order in orders_object if orders_object[order]["status"] not in ["Completed", "Delivered"]
    ]

# 1.0.3 - Function to save orders to the database
def save_orders(orders):
    with open("Data/orders.json", "w") as file:
        json.dump(orders, file, indent=4)

# 2 - Update order status to "Completed" or "Delivered" depending on dining option and cannot be undone.
def update_order_status(current_user):
    if show_orders(current_user):
        orders_object = get_orders_raw()
        order_id = input("\nPlease input the order ID to mark as completed\nOrder ID: ").upper()
        if order_id not in orders_object:
            print("Invalid Order ID")
        else:
            dining_option = orders_object[order_id]["details"]["diningOption"]
            orders_object[order_id]["status"] = "Completed" if dining_option == "Dine-in" else "Delivered"
            save_orders(orders_object)

# 2.0.1 - Function to retrieve all orders from the database 
def get_orders_raw():
    try:
        with open("Data/orders.json", "r") as file:
            orders_object = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}
    return orders_object

# 3 - Request ingredients and update the quantity
def request_ingredients(current_user):
    requested_items = list()  # A set to keep track of requests made by the user
    handle_request_options(current_user, requested_items)

# 3.1 - Handle request options for adding/editing/deleting ingredients
def handle_request_options(current_user, requested_ingredients: list):
    while True:
        show_requests(requested_ingredients)
        try:
            option = int(
                input("\n1. Add ingredient\n2. Edit ingredient\n3. Delete ingredient\n4. Complete request\nOption: "))
            if option not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            print("\nInvalid option")
            continue

        if option == 1:
            add_ingredient(requested_ingredients, current_user)
        elif option == 2:
            edit_request(requested_ingredients, current_user)
        elif option == 3:
            delete_request(requested_ingredients, current_user)
        elif option == 4:
            complete_request(requested_ingredients, current_user)

# 3.1.1 - Add a new ingredient to the request
def add_ingredient(requested_ingredients: list, current_user):
    item_name = input("Enter the name of the ingredient you'd like to request: ")
    item_unit = input("Unit of measure: ")
    try:
        item_quantity = int(input("Quantity number: "))
        if item_quantity < 1:
            raise ValueError
    except ValueError:
        print("\nInvalid quantity")
        add_ingredient(requested_ingredients)
        return

    requested_ingredient = {
        "name": item_name,
        "quantity": item_quantity,
        "unit": item_unit
    }

    requested_ingredients.append(requested_ingredient)
    print(f"Added {item_name} to the request")
    handle_request_options(current_user, requested_ingredients)

# 3.1.2 - Edit an existing request
def edit_request(requested_ingredients: list, current_user):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("\nChoose an ingredient to edit: "))
        if item_number > len(requested_ingredients) or item_number < 1:
            raise ValueError
    except ValueError:
        print("\nInvalid Item ID")
        edit_request(requested_ingredients)
        return

    item_name = requested_ingredients[item_number - 1]["name"]
    try:
        new_quantity = int(input("New Quantity: "))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        print("\nInvalid quantity")
        edit_request(requested_ingredients)
        return

    print(f"Changed quantity of {item_name} from {requested_ingredients[item_number - 1]['quantity']} to {new_quantity}")

    requested_ingredients[item_number - 1]["quantity"] = new_quantity
    handle_request_options(current_user, requested_ingredients)

# 3.1.3 - Delete an existing request
def delete_request(requested_ingredients: list, current_user):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("Choose the ingredient to delete: "))
        if item_number > len(requested_ingredients) or item_number < 1:
            raise ValueError
    except ValueError:
        print("\nInvalid Item ID")
        delete_request(requested_ingredients)
        return

    item_name = requested_ingredients[item_number - 1]["name"]
    print(f"Deleted {item_name} from the request")
    requested_ingredients.pop(item_number - 1)
    handle_request_options(current_user, requested_ingredients)

# 3.1.4 - Complete the request by creating a boilerplate
def complete_request(requested_items, current_user):
    request_id = get_next_id("ingredients")
    date, time = time_object()
    request_object = {
            "status": "pending",
            "items": requested_items,
            "request_chef": {"user": current_user, "date": date, "time": time},
            "review_user": {"user": "", "date": "", "time": ""}
        }
    add_request_to_file(request_id, request_object)
    print(f"\nRequest with id {request_id} was successfully submitted :D")
    start(current_user)

# 3.2 - Display ingredient requests
def show_requests(requests):
    if len(requests) != 0:
        headers = ["#", "Ingredient", "Quantity", "Measure (Unit)"]
        rows = [[i + 1, ingredient["name"], ingredient["quantity"], ingredient["unit"]] for i, (ingredient) in enumerate(requests)]
        print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    else:
        print("\nNo requests made :D")

# 3.3 - Add a complete request to the file
def add_request_to_file(request_id, request_object):
    try:
        with open("Data/Ingredients.json", "r") as file:
            requests = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    requests[request_id] = request_object

    with open("Data/Ingredients.json", "w") as file:
        json.dump(requests, file, indent=4)

# 4 - Update profile function
def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)

# 5 - Logout function
def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)
