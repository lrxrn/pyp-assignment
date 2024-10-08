import json
from datetime import datetime
from tabulate import tabulate
TABLE_FORMAT = "rounded_outline"  # The table format to be displayed

# Import common functions from functions.py
from Modules.functions import inp, printD, get_next_id


def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)

def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)


# Function to get the current date and time in the formats 05-Sep-2024 and 10:30 PM respectively
def time_object():
    now = datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')


# Function to retrieve active orders from the database
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

def save_orders(orders):
    with open("Data/orders.json", "w") as file:
        json.dump(orders, file, indent=4)


# Display orders in a grid format
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


# Update order status to "Completed" or "Delivered" depending on dining option and cannot be undone.
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


# # Display ingredients in a grid format
# def show_ingredients(ingredients):
#     headers = ["Item ID", "Ingredient", "Measure (Unit)"]
#     rows = [[i + 1, ingredient, details["unit"]] for i, (ingredient, details) in enumerate(ingredients.items())]
#     print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))


# Display ingredient requests
def show_requests(requests):
    if len(requests) != 0:
        headers = ["#", "Ingredient", "Quantity", "Measure (Unit)"]
        rows = [[i + 1, ingredient["name"], ingredient["quantity"], ingredient["unit"]] for i, (ingredient) in enumerate(requests)]
        print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    else:
        print("\nNo requests made :D")
        
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
        
        
def get_ingredients():
    try:
        with open("Data/ingredients.json", "r") as file:
            ingredients = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

    return ingredients


# Request ingredients and update the quantity
def request_ingredients(current_user):
    requested_items = list()  # A set to keep track of requests made

    handle_request_options(current_user, requested_items)


# Handle request options for adding/editing/deleting ingredients
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

# Add a new ingredient to the request
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

# Edit an existing request
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


# Delete an existing request
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


# Complete the request by creating a boilerplate
def complete_request(requested_items, current_user):
    request_id = get_next_id("ingredients")
    date, time = time_object()
    request_object = {
            "status": "pending",
            "items": requested_items,
            "request_Chef": {"user": current_user, "date": date, "time": time},
            "review_user": {"user": "", "date": "", "time": ""}
        }
    add_request_to_file(request_id, request_object)
    print(f"\nRequest with id {request_id} was successfully submitted :D")
    start(current_user)


# 0 Start function
def start(cur_usr):
    while True:
        printD(f"Welcome, {cur_usr}!", "cyan", True)
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

# # Main function to test the above code
# def main():
#     try:
#         with open("Used_ingredients.json", "r") as file:
#             INGREDIENTS = json.load(file)

#         with open("Orders.json", "r") as file:
#             ORDERS = json.load(file)

#         show_orders(ORDERS)
#         # update_order_status(ORDERS)
#         # show_ingredients(INGREDIENTS)
#         request = complete_request(request_ingredients(INGREDIENTS), "ING-005", "Jonny")

#         with open("ingredients.json", "r") as file:
#             requests = json.load(file)

#         requests.update(request)

#         with open("ingredients.json", "w") as file:
#             json.dump(requests, file, indent=4)

#         print("Ingredients JSON file updated successfully!")

#     except json.JSONDecodeError as e:
#         print(f"Error reading JSON file: {e}")
#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     main()
