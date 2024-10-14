from tabulate import tabulate
from Modules.db import *
from datetime import datetime
from Modules.functions import get_next_id

def time_object():
    now = datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')


def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)

def update_profile(cur_user):
    from main import update_profile as update_profile_main
    update_profile_main(cur_user)


def start(current_user):
    print("Customer Menu")
    print("1. View and Order food")
    print("2. View order status")
    print("3. Send feedback to owner")
    print("4. Update profile")
    print("5. Logout")
    choice = int(input("Enter a choice: "))
    if choice == 1:
        collect_order(current_user)
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
def show_menu():
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
    
def collect_order(current_user):
    orderItems = []
    while True:
        show_menu()
        item = input("Enter the item number you want to order: ").upper()
        if not db_getKey("menu", item):
            print("Invalid item number")
            continue
        quantity = int(input("Enter the quantity: "))
        orderItems.append({"item": item, "quantity": quantity})
        ch = input("Do you want to order more items? (y/n): ")
        if ch.lower() == "n":
            break

    diningOpt = input("Enter the dining option (Dine-in/Takeaway): ")
    if diningOpt.lower() == "takeaway":
        address = input("Enter the address: ")
    else:
        address = "Dine-in"
        
    print("Order Summary")
    headers = ["Item", "Quantity"]
    rows = [(db_getKey("menu", item["item"])["name"], item["quantity"]) for item in orderItems]
    print(tabulate(rows, headers, tablefmt="grid"))
    print(f"Dining Option: {diningOpt}")
    if diningOpt.lower() == "takeaway":
        print(f"Delivery Address: {address}")
    totalAmt = sum([db_getKey("menu", item["item"])["price"] * item["quantity"] for item in orderItems])
    print(f"Total Amount: {totalAmt}")
    confirm = input("Confirm Order? (y/n): ")
    if confirm.lower() == "y":
        while True:
            payment_method = input("How would you like to pay? (Card, Cash): ")
            payment_amount = int(input("Enter the amount: "))
            if payment_method.lower() == "cash":
                if payment_amount < totalAmt:
                    print("Insufficient amount")
                    continue
                elif payment_amount > totalAmt:
                    change = payment_amount - totalAmt
                    print(f"Change: {change}")
                print("Payment successful")
                break
            elif payment_method.lower() == "card":
                print("Payment successful")
                break
            else:
                print("Invalid payment method")
                continue
        payment_dict = {
            "method": payment_method,
            "status": "Paid",
            "amount": payment_amount,
            "change": change if payment_method.lower() == "cash" else 0
        }
        place_order(orderItems, diningOpt, address, current_user, payment_dict)
    else:
        print("Order Cancelled")
    start(current_user)


def place_order(orderItems, diningOpt, address, current_user, payment_dict):
    order_dict = create_order_dict(orderItems, diningOpt, address, current_user, payment_dict)
    order_id = get_next_id("orders")
    db_addKey("orders", order_id, order_dict)
    print(f"Order placed successfully. Your order ID is {order_id}")
        

def create_order_dict(orderItems, diningOpt, address, customer, payment_dict):
    date, time = time_object()
    totalAmt = sum([db_getKey("menu", item["item"])["price"] * item["quantity"] for item in orderItems])
    order = {
        "status": "Order Placed",
        "details": {
            "items": orderItems,
            "totalAmount": totalAmt,
            "diningOption": diningOpt,
            "deliveryAddress": address
        },
        "date": date,
        "time": time,
        "customer": customer,
        "chef": "N/a",
        "payment": payment_dict,
        "feedback": {}
    }
    return order

# this function is to show the order status
def view_order_status(order_id):
    print(f"Order Status: {database["orders"][order_id]["OrderStatus"]}")


# this function is asking the customer for feedbacks
def show_feedback(Feedback_ID):
    rating = input("pleas give us your rating:")
    additionalfeedbck = input("pleas give us any addiotion: ")
    return {Feedback_ID: {"rating": rating, "additionfeedback": additionalfeedbck}}