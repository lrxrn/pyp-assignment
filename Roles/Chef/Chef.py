import json
from datetime import datetime
from tabulate import tabulate
from math import ceil

TABLE_FORMAT = "rounded_outline"  # Table format to display in tabular form
ORDERS_FILE = "Orders.json"
REQUESTS_FILE = "Ingredients.json"


# Function to get the current date and time in the formats 05-Sep-2024 and 10:30 PM respectively
def time_object():
    now = datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')


# Function to retrieve active orders from the database (orders_object)
def get_orders(orders_object):
    # returning an order if status is not "Completed" or "Delivered"
    return [
        {"order_id": order, "items": orders_object[order]["details"]["items"]}
        for order in orders_object if orders_object[order]["status"] not in ["Completed", "Delivered"]
    ]


# Function to display orders in a table format using tabulate.
# Returns a boolean value to be used by the update_order_status() function
def show_orders(orders_object):
    orders = get_orders(orders_object)
    if not orders:  # Check if requests are made or not
        print("No orders :D")
        return False

    headers = ["Order ID", "Item ID", "Quantity"]
    rows = []

    # Building row data for table display
    for order in orders:
        for index, item in enumerate(order["items"]):
            if index == 0:
                rows.append([order['order_id'], item['ID'], item['quantity']])
            else:
                rows.append(["", item['ID'], item['quantity']])
        rows.append(["-----------", "----------", "---------"])  # Separator between orders
    rows.pop()  # Remove the last separator

    print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    return True


# Function to update the status of an order to either "Completed" or "Delivered"
def update_order_status(orders_object):
    try:
        # Checking the boolean value returned by show_orders() function to
        if show_orders(orders_object):
            order_id = input("\nPlease input the order ID to mark as completed\nOrder ID: ").upper().strip()
            if order_id not in orders_object:
                print("Invalid Order ID")
                raise ValueError
            else:
                dining_option = orders_object[order_id]["details"]["diningOption"]
                orders_object[order_id]["status"] = "Completed" if dining_option == "Dine-in" else "Delivered"
        return orders_object
    except ValueError:
        return update_order_status(orders_object)


# Function to display ingredients in a tabular format
def show_ingredients(ingredients):
    headers = ["Item ID", "Ingredient", "Measure (Unit)"]
    rows = [[i + 1, ingredient, details["Measure"]] for i, (ingredient, details) in enumerate(ingredients.items())]
    print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))


# Function to display ingredient requests in a tabular format
def show_requests(requests):
    if any(v["Quantity"] > 0 for v in requests.values()):
        headers = ["Item ID", "Ingredient", "Quantity", "Measure (Unit)"]
        rows = [[i + 1, ingredient, details["Quantity"], details["Measure"]] for i, (ingredient, details) in
                enumerate(requests.items()) if details["Quantity"] > 0]
        print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    else:
        print("\nNo requests made :D")


# Function to request ingredients, handling inputs and errors
# Returns a request object containing the requests made by the chef
def request_ingredients():
    requested_ingredients = dict()  # Store the requested ingredients
    while True:
        try:
            ingredient = input("\nPlease input the ingredient you want to request\nIngredient: ")
            if not ingredient.isalpha():
                raise ValueError("Invalid ingredient input. Please enter a valid name.")
        except ValueError as e:
            print(f"{e}")
            continue
        try:
            quantity = ceil(float(input("Quantity: ")))
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except ValueError as e:
            print(f"Invalid quantity: {e}")
            continue
        try:
            measure = input("Measure: ")
            valid_measures = ["Kg", "L", "Litres", "Bottle", "Bottles", "Can", "Cans", "Tray", "Trays"]
            if measure.capitalize() not in valid_measures:
                raise ValueError("Invalid measure.")
        except ValueError as e:
            print(f"Invalid measure: {e}")
            continue

        # Adding the request to the requests dictionary
        requested_ingredients.update(get_ingredients(ingredient, quantity, measure))

        if not handle_request_options(requested_ingredients):
            break

    # Returning the requested items and making sure the quantity is greater than 0
    return {k: v for k, v in requested_ingredients.items() if v["Quantity"] > 0}


# Function to handle request options such as adding, editing, or deleting ingredients
# Returns a boolean value used to determine whether to break out of the outer loop in request_ingredients()
def handle_request_options(requested_ingredients):
    while True:
        show_requests(requested_ingredients)
        try:
            option = int(
                input("\n1. Add ingredient\n2. Edit ingredient\n3. Delete ingredient\n4. Complete request\nOption: "))
            if option not in [1, 2, 3, 4]:
                raise ValueError("Invalid option.")
        except ValueError as e:
            print(f"{e}")
            continue

        if option == 1:
            return True
        elif option == 2:
            edit_request(requested_ingredients)
        elif option == 3:
            delete_request(requested_ingredients)
        elif option == 4:
            return False


# Function to edit an existing request
def edit_request(requested_ingredients):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("\nChoose an ingredient to edit: "))
        if item_number not in range(1, len(requested_ingredients) + 1):
            raise ValueError("Invalid Item ID.")
    except ValueError as e:
        print(f"{e}")
        return

    try:
        new_quantity = int(input("New Quantity: "))
        if new_quantity < 1:
            raise ValueError("Quantity must be greater than zero.")
    except ValueError as e:
        print(f"{e}")
        return

    item_name = list(requested_ingredients.keys())[item_number - 1]
    requested_ingredients[item_name]["Quantity"] = new_quantity


# Function to delete an existing request
def delete_request(requested_ingredients):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("Choose the ingredient to delete: "))
        if item_number not in range(1, len(requested_ingredients) + 1):
            raise ValueError("Invalid Item ID.")
    except ValueError as e:
        print(f"{e}")
        return

    item_name = list(requested_ingredients.keys())[item_number - 1]
    requested_ingredients.pop(item_name)


# Function to complete the ingredient request and create a boilerplate object
def complete_request(request_object, request_id, name):
    date, time = time_object()
    boiler_plate = {
        f"{request_id}": {
            "status": "pending",
            "items": [{"name": req, "quantity": details["Quantity"], "unit": details["Measure"]}
                      for req, details in request_object.items()],
            "request_Chef": {"user": name, "date": date, "time": time},
            "review_user": {"user": "", "date": "", "time": ""}
        }
    }
    # print(boiler_plate)
    print("\nRequest successfully submitted :D")
    return boiler_plate


# Function to create a dictionary for requested ingredients
def get_ingredients(Ingredient, Quantity, Measure):
    return {
        Ingredient.capitalize(): {
            "Quantity": ceil(Quantity),
            "Measure": Measure.capitalize()
        }
    }


# Main function to test the functions
def main():
    def load_file(file_name):
        with open(file_name) as file:
            return json.load(file)

    def write_to_file(file_name, data, mode="w"):
        with open(file_name, mode) as file:
            json.dump(data, file, indent=4)
        print(f"{file_name} updated successfully")

    def _show_orders_():
        ORDERS = load_file(ORDERS_FILE)
        show_orders(ORDERS)

    def _update_order_status_():
        ORDERS = load_file(ORDERS_FILE)
        orders = update_order_status(ORDERS)
        print(orders)
        ORDERS.update(orders)
        write_to_file(ORDERS_FILE, orders)

    def make_request(request_id, chef_name):
        REQUESTS = load_file(REQUESTS_FILE)
        request = complete_request(request_ingredients(), request_id, chef_name)
        REQUESTS.update(request)
        write_to_file(REQUESTS_FILE, REQUESTS)

    try:
        # _show_orders_()
        # _update_order_status_()
        make_request("ING-008", "Jeff")
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
