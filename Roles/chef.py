from tabulate import tabulate
import json as j
from Modules.utils import printD, inp

with open("./Data/ingredients.json", "r") as file:
    INGREDIENTS = j.load(file)

with open("./Data/orders.json", "r") as file:
    ORDERS = j.load(file)


# A function that gets the active orders
def get_orders(orders_object):
    orders = []
    order_status = ["Completed", "Delivered"]

    for order in orders_object:
        if orders_object[order]["status"] not in order_status:
            order = {
                "order_id": order,
                "items": orders_object[order]["details"]["items"],
            }
            orders.append(order)
    return orders


# A function to display the orders made by customers in a grid. Takes in an orders object
def show_orders(orders_object):
    orders = get_orders(orders_object)

    if not orders:
        print("No orders :D")
        return False
    else:
        headers = ["Order ID", "Order (Item --> Quantity)"]
        rows = [
            [order["order_id"], "\n".join([f'{item["ID"]} {item["quantity"]}' for item in order["items"]])]
            for order in orders
        ]
        print(tabulate(rows, headers, tablefmt="grid"))
        return True


# Function to update the status of an order
def update_order_status(orders_object):
    order_ids = orders_object.keys()

    if show_orders(orders_object):
        order_id = input("\nPlease input the order ID to mark as completed\nOrder ID: ").upper()
        if order_id not in order_ids:
            print("Invalid Order ID")
        else:
            dining_option = orders_object[order_id]["details"]["diningOption"]
            orders_object[order_id]["status"] = "Completed" if dining_option == "Dine-in" else "Delivered"
    return orders_object


# A function to show the list of ingredients required to make any dish
def show_ingredients(ingredients):
    headers = ["Item ID", "Ingredient"]
    rows = [[item_number + 1, ingredient] for item_number, ingredient in enumerate(ingredients)]
    print(tabulate(rows, headers, tablefmt="grid"))


# A function to show the requests made by the chef
def show_requests(requests):
    requests_exist = any(quantity > 0 for quantity in requests.values())
    if requests_exist:
        headers = ["Item ID", "Ingredient", "Quantity"]
        rows = [(item_number + 1, ingredient, quantity)
                for item_number, (ingredient, quantity) in enumerate(requests.items()) if quantity > 0]
        print(tabulate(rows, headers, tablefmt="grid"))
    else:
        print("\nNo requests made :D")


# Function to request ingredients
def request_ingredients(ingredients):
    requested_ingredients = {ingredient: 0 for ingredient in ingredients}
    requested_item_ids = set()

    is_requesting = True
    while is_requesting:
        show_ingredients(ingredients)  # Display ingredient options

        try:
            item_number = int(input("\nSelect the number corresponding to the item you'd like to request: "))
            if not (1 <= item_number <= len(ingredients)):
                raise ValueError
        except ValueError:
            print("Invalid Item ID")
            continue

        try:
            quantity = int(input("Quantity number: "))
            if quantity < 0:
                raise ValueError
        except ValueError:
            print("Invalid quantity")
            continue

        item_name = ingredients[item_number - 1]
        requested_ingredients[item_name] += quantity
        if item_number not in requested_item_ids:
            requested_item_ids.add(item_number)

        show_requests(requested_ingredients)  # Show current requests after updating

        while True:
            try:
                option = int(input("\nWould you like to:\n1. Add ingredient\n2. Edit ingredient\n"
                                   "3. Delete ingredient\n4. Complete request\nOption: "))
                if option not in [1, 2, 3, 4]:
                    raise ValueError
            except ValueError:
                print("Invalid option")
                continue

            if option == 1:
                break  # Go back to outer loop to add another item
            elif option == 2:
                if not any(quantity > 0 for quantity in requested_ingredients.values()):
                    print("\nNo requests made :D")
                else:
                    edit_request(ingredients, requested_ingredients, requested_item_ids)
            elif option == 3:
                if not any(quantity > 0 for quantity in requested_ingredients.values()):
                    print("\nNo requests made :D")
                else:
                    delete_request(ingredients, requested_ingredients, requested_item_ids)
            elif option == 4:
                requested_ingredients = {k: v for k, v in requested_ingredients.items() if v > 0}
                if requested_ingredients:
                    print("\nFinal Request:")
                    show_requests(requested_ingredients)  # Show final request before confirmation
                else:
                    print("\nNo requests made.")
                return requested_ingredients


# Function to edit an existing request
def edit_request(ingredients, requested_ingredients, requested_item_ids):
    show_requests(requested_ingredients)  # Always show requests before editing

    if not any(quantity > 0 for quantity in requested_ingredients.values()):
        print("\nNo requests made :D")
        return

    try:
        item_number = int(input("\nChoose an ingredient to edit: "))
        if item_number not in requested_item_ids:
            raise ValueError
    except ValueError:
        print("Invalid Item ID")
        return

    try:
        new_quantity = int(input("New Quantity: "))
        if new_quantity < 0:
            raise ValueError
    except ValueError:
        print("Invalid quantity")
        return

    item_name = ingredients[item_number - 1]
    requested_ingredients[item_name] = new_quantity
    if new_quantity == 0:
        requested_item_ids.remove(item_number)
    show_requests(requested_ingredients)  # Show updated requests after editing


# Function to delete an existing request
def delete_request(ingredients, requested_ingredients, requested_item_ids):
    show_requests(requested_ingredients)  # Always show requests before deleting

    if not any(quantity > 0 for quantity in requested_ingredients.values()):
        print("\nNo requests made :D")
        return

    try:
        item_number = int(input("Choose the ingredient to delete: "))
        if item_number not in requested_item_ids:
            raise ValueError
    except ValueError:
        print("Invalid Item ID")
        return

    item_name = ingredients[item_number - 1]
    requested_ingredients[item_name] = 0
    requested_item_ids.remove(item_number)
    show_requests(requested_ingredients)  # Show updated requests after deletion
    
def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)

def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)
    
def start(cur_usr):
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


# A function to test the working of the rest of the functions
# def main():
#     # show_orders(ORDERS)
#     # update_order_status(ORDERS)
#     request_ingredients(["Fish", "Eggs"])


# main()