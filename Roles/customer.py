from tabulate import tabulate
from Modules.db import *


def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)

def update_profile(cur_user):
    from main import update_profile as update_profile_main
    update_profile_main(cur_user)


def start(current_user):
    print("1. View and Order food")
    print("2. View order status")
    print("3. Send feedback to owner")
    print("4. Update profile")
    print("5. Logout")
    choice = int(input("Enter a choice: "))
    if choice == 1:
        show_menu(current_user)
    elif choice == 2:
        view_order_status(current_user)
    elif choice == 3:
        show_feedback(current_user)
    elif choice == 4:
        update_profile(current_user)
    elif choice == 5:
        logout(current_user)
    else:
        print("wrong input")
        start(current_user)


# Function to display the menu
def show_menu(current_user):
    menu = db_getAllKeys("menu")
    items = []
    for item in menu:
        dbMenuItem = db_getKey("menu", item)
        menuItem = { "ID": item, "name": dbMenuItem['name'], "category": dbMenuItem["category"], "cuisineType": dbMenuItem["cuisineType"], "price": dbMenuItem["price"] }
        items.append(menuItem)

    headers = ["Item number", "Item", "Price"]
    rows = [(items[i]["ID"],items[i]["name"], items[i]["price"]) for i in range(len(items))]
    table = tabulate(rows, headers, tablefmt="grid")
    print(table)
    start(current_user)


# this function is to show the order status
def view_order_status(order_id):
    print(f"Order Status: {database["orders"][order_id]["OrderStatus"]}")


# this function is asking the customer for feedbacks
def show_feedback(Feedback_ID):
    rating = input("pleas give us your rating:")
    additionalfeedbck = input("pleas give us any addiotion: ")
    return {Feedback_ID: {"rating": rating, "additionfeedback": additionalfeedbck}}


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
        "OrderID": {
            "date": "01/01/2000",
            "MenuItems": [
                "MenuOptID"
            ],
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
        },
        {
            "MenuOptID": "C_01_1",
            "Name": "Dish2",
            "CuisineType": "Arabic",
            "Price": 4.8,
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
            "additionalFeedback": 0,
            "adminResponse": 0,
            "Customer": 0
        }
    }
}


