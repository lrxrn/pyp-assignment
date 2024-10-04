def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)

def start(cur_usr):
    print(f"Welcome, {cur_usr}!")
    print("Customer menu is currently under construction.")
    logout(cur_usr)

from tabulate import  tabulate
# Function to display the menu
def show_menu(menu):
    items = []
    for item in menu:
        items.append(item.values())

    headers = ["Item number", "Item", "Price"]
    rows = [[1+num, name, price] for num, (id, name, type, price, category) in enumerate(items)]
    table = tabulate(rows, headers, tablefmt="grid")
    print(table)




# this function is to show the order status
def view_order_status(order_id):
    print(f"Order Status: {database["orders"][order_id]["OrderStatus"]}")
# this function is asking the customer for feedbacks
def show_feedback(Feedback_ID):
    rating = input("pleas give us your rating:" )
    additionalfeedbck=input("pleas give us any addiotion: ")
    return  {Feedback_ID: { "rating": rating,"additionfeedback":additionalfeedbck}}

# print(show_feedback("Tony"))

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


show_menu(database["menu"])
