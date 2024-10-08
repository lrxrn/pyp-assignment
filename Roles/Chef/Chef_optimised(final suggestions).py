import json
from datetime import datetime
from tabulate import tabulate
from math import ceil

TABLE_FORMAT = "rounded_outline"  # The table format to be displayed


# Function to get the current date and time in the formats 05-Sep-2024 and 10:30 PM respectively
def time_object():
    now = datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')


# Function to retrieve active orders from the database
def get_orders(orders_object):
    return [
        {"order_id": order, "items": orders_object[order]["details"]["items"]}
        for order in orders_object if orders_object[order]["status"] not in ["Completed", "Delivered"]
    ]


# Display orders in a grid format
def show_orders(orders_object):
    orders = get_orders(orders_object)
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
def update_order_status(orders_object):
    if show_orders(orders_object):
        order_id = input("\nPlease input the order ID to mark as completed\nOrder ID: ").upper()
        if order_id not in orders_object:
            print("Invalid Order ID")
        else:
            dining_option = orders_object[order_id]["details"]["diningOption"]
            orders_object[order_id]["status"] = "Completed" if dining_option == "Dine-in" else "Delivered"
    return orders_object


# Display ingredients in a grid format
def show_ingredients(ingredients):
    headers = ["Item ID", "Ingredient", "Measure (Unit)"]
    rows = [[i + 1, ingredient, details["Measure"]] for i, (ingredient, details) in enumerate(ingredients.items())]
    print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))


# Display ingredient requests
def show_requests(requests):
    if any(v["Quantity"] > 0 for v in requests.values()):
        headers = ["Item ID", "Ingredient", "Quantity", "Measure (Unit)"]
        rows = [[i + 1, ingredient, details["Quantity"], details["Measure"]] for i, (ingredient, details) in
                enumerate(requests.items()) if details["Quantity"] > 0]
        print(tabulate(rows, headers, tablefmt=TABLE_FORMAT))
    else:
        print("\nNo requests made :D")


# Request ingredients and update the quantity
def request_ingredients():
    requested_ingredients = dict()  # A dictionary to store the ingredients
    while True:
        # requested_ingredients = {k: v.copy() for k, v in ingredients.items()}
        # show_ingredients(ingredients)

        try:
            ingredient = input("\nPlease input the ingredient you want to request for "
                               "the quantity and measure\nIngredient: ")
            if not ingredient.isalpha():
                raise ValueError
        except ValueError as e:
            print(f"\nInvalid ingredient input: {e}. Please put a valid ingredient")
            continue
        try:
            quantity = ceil(float(input("Quantity: ")))
            if quantity <= 0:
                raise ValueError
        except ValueError as e:
            print(f"Invalid quantity: {e}")
            continue
        try:
            measure = input("Measure: ")
            measures = ["Kg", "L", "Litres", "Bottle", "Bottles", "Can", "Cans", "Tray", "Trays"]
            if not (measure.isalpha() and measure.capitalize() in measures):
                raise ValueError
        except ValueError as e:
            print(f"Invalid measure: {e}")
            continue

        requested_ingredients.update(get_ingredients(ingredient, quantity, measure))
        # requested_item_ids = set()  # A set to keep track of requests made

        # show_requests(requested_ingredients)
        if not handle_request_options(requested_ingredients):
            break

    return {k: v for k, v in requested_ingredients.items() if v["Quantity"] > 0}


# Handle request options for adding/editing/deleting ingredients
def handle_request_options(requested_ingredients):
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
            return True
        elif option == 2:
            edit_request(requested_ingredients)
        elif option == 3:
            delete_request(requested_ingredients)
        elif option == 4:
            return False


# Edit an existing request
def edit_request(requested_ingredients):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("\nChoose an ingredient to edit: "))
        requested_item_ids = [x for x in range(1, len(requested_ingredients) + 1)]
        if item_number not in requested_item_ids:
            raise ValueError
    except ValueError:
        print("\nInvalid Item ID")
        edit_request(requested_ingredients)
        return

    try:
        new_quantity = int(input("New Quantity: "))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        print("\nInvalid quantity")
        edit_request(requested_ingredients)
        return

    item_name = list(requested_ingredients.keys())[item_number - 1]
    requested_ingredients[item_name]["Quantity"] = new_quantity


# Delete an existing request
def delete_request(requested_ingredients):
    show_requests(requested_ingredients)

    try:
        item_number = int(input("Choose the ingredient to delete: "))
        requested_item_ids = [x for x in range(1, len(requested_ingredients) + 1)]
        if item_number not in requested_item_ids:
            raise ValueError
    except ValueError:
        print("\nInvalid Item ID")
        delete_request(requested_ingredients)
        return

    item_name = list(requested_ingredients.keys())[item_number - 1]
    requested_ingredients[item_name]["Quantity"] = 0
    requested_ingredients.pop(item_name)


# Complete the request by creating a boilerplate
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
    print(boiler_plate)
    print("\nRequest was successfully submitted :D")
    return boiler_plate


# A function that gets the requested items. Takes information such as ingredient, unit and quantity
def get_ingredients(Ingredient, Quantity, Measure):
    boiler_plate = {
        Ingredient.capitalize(): {
            "Quantity": ceil(Quantity),
            "Measure": Measure.capitalize()
        }
    }
    return boiler_plate


# Main function to test the above code
def main():
    try:
        # with open("Used_ingredients.json", "r") as file:
        # INGREDIENTS = json.load(file)

        with open("Orders.json", "r") as file:
            ORDERS = json.load(file)

        show_orders(ORDERS)
        # update_order_status(ORDERS)
        # show_ingredients(INGREDIENTS)
        request = complete_request(request_ingredients(), "ING-006", "Harry")

        with open("ingredients.json", "r") as file:
            requests = json.load(file)

        requests.update(request)

        with open("ingredients.json", "w") as file:
            json.dump(requests, file, indent=4)

        print("Ingredients JSON file updated successfully!")

    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
