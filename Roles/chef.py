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

# Paths
ORDERS = "Data/orders.json"
INGREDIENTS = "Data/Ingredients.json"

# 0 - Start function
def start(cur_usr):
    while True:
        printD("Chef menu", "magenta", True)
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
def show_orders(current_user, active=True):
    orders = get_orders(active=active)
    if not orders:
        printD("No orders :D", "green", True)
        return False

    headers = ["Order ID", "Item ID", "Quantity"]
    rows = []

    for order in orders:
        for index, item in enumerate(order["items"]):
            if index == 0:
                color = "green" if order['status'] in ["Completed", "Delivered"] else "red"
                order_id = color_text(order['order_id'], color, True)
                rows.append([order_id, item['ID'], item['quantity']])
            else:
                rows.append(["", item['ID'], item['quantity']])
        rows.append(["-----------", "----------", "---------"])  # Separator
    rows.pop()  # Remove the last separator

    print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    return True

# 1.0.1 - Date and time function
def time_object():
    now = datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')

# 1.0.2 - Function to retrieve active orders and all orders
def get_orders(original=False, active=True):
    try:
        with open(ORDERS) as file:
            orders_object = json.load(file)
    except json.JSONDecodeError as e:
        printD(f"Error reading JSON file: {e}", "red", True)
        return []
    except Exception as e:
        printD(f"Error: {e}", "red", True)
        return []

    if original:
        return orders_object
    
    # Filtering based on order status
    return [
        {"order_id": order, "items": orders_object[order]["details"]["items"], "status": orders_object[order]["status"]}
        for order in orders_object 
        if ((orders_object[order]["status"] not in ["Completed", "Delivered"]) if active else True)
    ]

# 1.0.3 - Function to save orders
def save_orders(orders):
    with open(ORDERS, "w") as file:
        json.dump(orders, file, indent=4)

# 2 - Update order status function
def update_order_status(current_user):
    if show_orders(current_user, True):
        orders_object = get_orders(original=True)
        filtered_orders = get_orders()
        keys = [key["order_id"] for key in filtered_orders]
        order_id = input("\nPlease input the order ID to mark as completed\nOrder ID: ").upper()
        if order_id not in keys:
            printD("Invalid Order ID", "red", True)
            return update_order_status(current_user)
        
        dining_option = orders_object[order_id]["details"]["diningOption"]
        orders_object[order_id]["status"] = "Completed" if dining_option == "Dine-in" else "Delivered"
        save_orders(orders_object)

# 3 - Request ingredients
def request_ingredients(current_user):
    requested_items = []
    handle_request_options(current_user, requested_items)

# 3.1 - Handle ingredient request options
def handle_request_options(current_user, requested_ingredients):
    while True:
        show_requests(requested_ingredients)
        try:
            option = int(input("\n1. Add ingredient\n2. Edit ingredient\n3. Delete ingredient\n4. Complete request\nOption: "))
            if option not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            printD("Invalid option", "red", True)
            continue

        if option == 1:
            add_ingredient(requested_ingredients, current_user)
        elif option == 2:
            edit_request(requested_ingredients, current_user)
        elif option == 3:
            delete_request(requested_ingredients, current_user)
        elif option == 4:
            complete_request(requested_ingredients, current_user)

# 3.1.1 - Add new ingredient request
def add_ingredient(requested_ingredients, current_user):
    item_name = input("Enter the name of the ingredient you'd like to request: ")
    item_unit = input("Unit of measure: ")
    try:
        item_quantity = int(input("Quantity number: "))
        if item_quantity < 1:
            raise ValueError
    except ValueError:
        printD("Invalid quantity", "red", True)
        return add_ingredient(requested_ingredients)

    requested_ingredients.append({"name": item_name, "quantity": item_quantity, "unit": item_unit})
    printD(f"Added {item_name} to the request", "green", True)

# 3.1.2 - Edit ingredient request
def edit_request(requested_ingredients, current_user):
    show_requests(requested_ingredients)
    try:
        item_number = int(input("Choose an ingredient to edit: "))
        if not (1 <= item_number <= len(requested_ingredients)):
            raise ValueError
    except ValueError:
        printD("Invalid Item ID", "red", True)
        return edit_request(requested_ingredients)

    item_name = requested_ingredients[item_number - 1]["name"]
    try:
        new_quantity = int(input("New Quantity: "))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        printD("Invalid quantity", "red", True)
        return edit_request(requested_ingredients)

    requested_ingredients[item_number - 1]["quantity"] = new_quantity
    printD(f"Changed quantity of {item_name} to {new_quantity}", "green", True)

# 3.1.3 - Delete ingredient request
def delete_request(requested_ingredients, current_user):
    show_requests(requested_ingredients)
    try:
        item_number = int(input("Choose the ingredient to delete: "))
        if not (1 <= item_number <= len(requested_ingredients)):
            raise ValueError
    except ValueError:
        printD("Invalid Item ID", "red", True)
        return delete_request(requested_ingredients)

    item_name = requested_ingredients[item_number - 1]["name"]
    requested_ingredients.pop(item_number - 1)
    printD(f"Deleted {item_name} from the request", "green", True)

# 3.1.4 - Complete request
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
    printD(f"Request with id {request_id} was successfully submitted :D", "green", True)
    start(current_user)

# 3.2 - Show requests
def show_requests(requests):
    if requests:
        headers = ["#", "Ingredient", "Quantity", "Measure (Unit)"]
        rows = [[i + 1, ingredient["name"], ingredient["quantity"], ingredient["unit"]] for i, ingredient in enumerate(requests)]
        print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    else:
        printD("No requests made :D", "green", True)

# 3.3 - Add request to file
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