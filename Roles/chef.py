from tabulate import tabulate
import json as j
import os as o

# Import common functions from functions.py
from Modules.functions import inp


def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)

def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)

def start(cur_usr):
    print(f"Welcome, {cur_usr}!")
    print("Chef menu is currently under construction.")
    logout(cur_usr)

# A function to display the orders made by customers in a grid
def show_orders(orders):
    selected_keys = ["MenuItems", "DineOpt", "OrderStatus"]
    headers = ["Order ID"] + selected_keys
    rows = [[orderID] + [data[key] for key in selected_keys] for orderID, data in orders.items()]
    print(tabulate(rows, headers, tablefmt="grid"))


# Function to update order status
# Sets status to "In Progress" if status = 0 and "Completed" if status = 1
def update_order_status(orders, orderID, status):
    status_mapping = {"0": "In Progress", "1": "Completed"}
    if status in status_mapping:
        orders[orderID]["OrderStatus"] = status_mapping[status]
    else:
        print("Invalid input")
    show_orders(orders)


# A function to show the list of ingredients required to make any dish
# It is assumed that in the database a list of ingredients is stored as a list, that is, ingredients = []
def show_ingredients(ingredients):
    headers = ["Item Number", "Ingredient"]
    rows = [(item_number + 1, ingredient) for item_number, ingredient in enumerate(ingredients)]
    print(tabulate(rows, headers, tablefmt="grid"))


# A function to print a grid of requests to the console
def show_requests(requests):
    headers = ["Item Number", "Ingredient", "Quantity"]
    rows = [(item_number + 1, ingredient, quantity) for item_number, (ingredient, quantity) in
            enumerate(requests.items()) if quantity != 0]
    print(tabulate(rows, headers, tablefmt="grid"))


# Function to request ingredients
# Returns a dictionary {"ingredient": "quantity"}
def request_ingredients(ingredients):
    requested_ingredients = {ingredient: 0 for ingredient in ingredients}  # Initialize all ingredients with quantity 0
    is_requesting = True

    def edit_request(_ingredients_, _requested_ingredients_):
        _item_number_ = int(input("Choose an ingredient to edit: "))
        _quantity_ = int(input("New Quantity: "))
        requested_ingredients[ingredients[_item_number_ - 1]] = _quantity_

    def delete_request(_ingredients_, _requested_ingredients_):
        _item_number_ = int(input("Choose the ingredient to delete: "))
        requested_ingredients[ingredients[_item_number_ - 1]] = 0

    while is_requesting:
        show_ingredients(ingredients)
        item_number = int(input("\nSelect the number corresponding to the item "
                                "you'd like to request and give the required quantity\nItem number: "))
        quantity = int(input("Quantity number: "))
        requested_ingredients[ingredients[item_number - 1]] += quantity  # Update quantity

        want_to_edit = True
        while want_to_edit:
            show_requests(requested_ingredients)
            option = int(input("Would you like to make changes to your request?\n"
                               "1.Add ingredient\n2.Edit ingredient\n3.Delete ingredient\n4.Complete request"))
            match option:
                case 1:
                    want_to_edit = False
                case 2:
                    edit_request(ingredients, requested_ingredients)
                case 3:
                    delete_request(ingredients, requested_ingredients)
                case 4:
                    is_requesting = False
                    want_to_edit = False
                case _:
                    print("Invalid choice. Try again.")

    # Remove ingredients with zero quantity
    requested_ingredients = {key: value for key, value in requested_ingredients.items() if value != 0}
    return requested_ingredients


#print(request_ingredients(["fish", "eggs"]))

# 0 Start function
def start(cur_usr):
    print(
        "Chef Menu\n1. View orders placed by customers. \n2. Update orders \n3. Request ingredients \n4. Update own profile. \n5. Logout")

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


database = {
    "users": {
        "username": {
            "name": "Name",
            "email": "Email",
            "role": "Customer",
            "Phone": "+1243456789",
            "DOB": "01/01/2000",
            "address": "One South"
        }
    },
    "passwords": {
        "username": "Password"
    },
    "orders": {
        "1": {
            "date": "01/01/2000",
            "MenuItems": ["MenuOptID"],
            "OrderStatus": "In Progress",
            "DineOpt": "Dine in",
            "PaymentOpt": "Cash",
            "TotalAmt": 52
        },
        "2": {
            "date": "01/01/2000",
            "MenuItems": "Burger\nsoda\ndrinks",
            "OrderStatus": "In Progress",
            "DineOpt": "Dine in",
            "PaymentOpt": "Cash",
            "TotalAmt": 52
        }
    },
    "menu": [
        {
            "MenuOptID": "C_01_1",
            "Name": "Dish1",
            "CuisineType": "Arabic",
            "Price": 4,
            "Category": "Main Dish"
        }
    ],
    "ingridients": [
        {
            "RequestID": "R_1",
            "RequestStatus": "Completed",
            "Ingredient": {
                "name": "egg",
                "quantity": 2
            },
            "RequestedChef": "user1",
            "History": [
                {
                    "User": "jonh",
                    "Status": "Completed Request",
                    "Date": "01/01/2020",
                    "Time": "01:00PM"
                }
            ]
        }
    ],
    "feedback": {
        "FeedbackID": {
            "rating": 3,
            "additionalFeedback": "null",
            "adminResponse": "null",
            "Customer": "null"
        }
    }
}

# data = database["orders"]
