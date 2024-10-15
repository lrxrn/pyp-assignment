from tabulate import tabulate
from Modules.db import *
from Modules.utils import get_next_id, time_object, display_table, wait_for_enter, printD, inp


# this function is to start the customer menu
def start(current_user):
    printD("Customer Menu", "magenta")
    print("1. View and Order food")
    print("2. View order status")
    print("3. Send feedback")
    print("4. Update profile")
    print("5. Logout")
    choice = inp("Enter a choice: ", "int", [1, 2, 3, 4, 5])
    if choice == 1:
        collect_order(current_user)
    elif choice == 2:
        view_order_status(current_user)
    elif choice == 3:
        send_feedback(current_user)
    elif choice == 4:
        update_profile(current_user)
    elif choice == 5:
        logout(current_user)
    else:
        print("wrong input")
        start(current_user)


# 1. this function is to collect the order from the customer
def collect_order(current_user):
    orderItems = []
    while True:
        show_menu()
        item = input("Enter the item number you want to order: ").upper()
        if not db_getKey("menu", item):
            print("Invalid item number")
            continue
        quantity = int(input("Enter the quantity: "))
        orderItems.append({"ID": item, "quantity": quantity})
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
    rows = [(db_getKey("menu", item["ID"])["name"], item["quantity"]) for item in orderItems]
    display_table(rows, headers)
    print(f"Dining Option: {diningOpt}")
    if diningOpt.lower() == "takeaway":
        print(f"Delivery Address: {address}")
    totalAmt = sum([db_getKey("menu", item["ID"])["price"] * item["quantity"] for item in orderItems])
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
    wait_for_enter("Press Enter to continue...", clear=True)
    start(current_user)


# 1.0.1 this function is to place the order
def place_order(orderItems, diningOpt, address, current_user, payment_dict):
    order_dict = create_order_dict(orderItems, diningOpt, address, current_user, payment_dict)
    order_id = get_next_id("orders")
    db_addKey("orders", order_id, order_dict)
    print(f"Order placed successfully. Your order ID is {order_id}")


  
# 1.0.2 this function is to create the order dictionary
def create_order_dict(orderItems, diningOpt, address, customer, payment_dict):
    date, time = time_object()
    totalAmt = sum([db_getKey("menu", item["ID"])["price"] * item["quantity"] for item in orderItems])
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


# 1.0.3 this function is to display the menu
def show_menu():
    menu = db_getAllKeys("menu")
    items = []
    for item in menu:
        dbMenuItem = db_getKey("menu", item)
        menuItem = { "ID": item, "name": dbMenuItem['name'], "category": dbMenuItem["category"], "cuisineType": dbMenuItem["cuisineType"], "price": dbMenuItem["price"] }
        items.append(menuItem)

    headers = ["Item number", "Item", "Price"]
    rows = [(items[i]["ID"],items[i]["name"], items[i]["price"]) for i in range(len(items))]
    display_table(rows, headers)


# 2. this function is to show the order status
def view_order_status(current_user):
    orders = db_getAllKeys("orders")
    order_list = []
    for order in orders:
        order_dict = db_getKey("orders", order)
        order_dict["ID"] = order
        if order_dict["customer"] == current_user and order_dict["status"].lower() != "completed":
            order_list.append(order_dict)
    if not order_list:
        print("No orders found")
        start(current_user)
    headers = ["Order ID", "Status", "Date", "Time", "Total Amount"]
    rows = [(order["ID"], order["status"], order["date"],
             order["time"], order["details"]["totalAmount"]) for order in order_list]
    display_table(rows, headers)
    order_id = input("Enter the order ID to view details: ").upper()
    order_details = db_getKey("orders", order_id)
    if not order_details:
        print("Invalid Order ID")
        start(current_user)
    print("Order Details")
    print(f"Order ID: {order_id}")
    print(f"Status: {order_details['status']}")
    print(f"Date: {order_details['date']}")
    print(f"Time: {order_details['time']}")
    print("Items")
    headers = ["Item", "Quantity"]
    rows = [(db_getKey("menu", item["ID"])["name"], item["quantity"]) for item in order_details["details"]["items"]]
    display_table(rows, headers)
    print(f"Total Amount: {order_details['details']['totalAmount']}")
    print(f"Dining Option: {order_details['details']['diningOption']}")
    if order_details['details']['diningOption'].lower() == "takeaway":
        print(f"Delivery Address: {order_details['details']['deliveryAddress']}")
    print("Payment Details")
    print(f"Payment Method: {order_details['payment']['method']}")
    print(f"Payment Status: {order_details['payment']['status']}")
    print(f"Amount: {order_details['payment']['amount']}")
    if order_details['payment']['method'].lower() == "cash":
        print(f"Change: {order_details['payment']['change']}")
    wait_for_enter("Press Enter to continue...", clear=True)
    start(current_user)


# 2.0.1 this function is to show the feedback   
def show_orders(user=None):
    if not user:
        orders = db_getAllKeys("orders")
    else:
        orders = db_getAllKeys("orders")
        for order in orders:
            order_dict = db_getKey("orders", order)
            if order_dict["customer"] != user:
                orders.remove(order)
        
    order_list = []
    for order in orders:
        order_dict = db_getKey("orders", order)
        order_dict["ID"] = order
        order_list.append(order_dict)
    
    if not orders:
        print("No orders :D")
        return False
    else:
        headers = ["Order ID", "Item ID", "Quantity"]
        rows = [(order["ID"], order["status"], order["date"], order["time"], order["details"]["totalAmount"]) for order in order_list]
        display_table(rows, headers)
        return True


# 3. this function is asking the customer for feedbacks
def send_feedback(current_user):
    show_orders(current_user)
    order_id = input("Enter the order ID to give feedback: ").upper()
    order = db_getKey("orders", order_id)
    if not order:
        print("Invalid Order ID")
        start(current_user)
    if order["customer"] != current_user:
        print("You can only give feedback for your orders")
        start(current_user)
    if order["status"].lower() != "completed":
        print("You can only give feedback for completed orders")
        start(current_user)
    if order["feedback"] != {}:
        print("Feedback already given")
        start(current_user)
    feedback = input("How much would you rate the food? (1-5): ")
    ch = input("Any additional feedback? (y/n): ")
    if ch.lower() == "y":
        additional_feedback = input("Enter your feedback: ")
    else:
        additional_feedback = ""
    order["feedback"] = {
        "rating": feedback,
        "comments": additional_feedback,
        "response": ""
    }
    db_updateKey("orders", order_id, order)
    print("Feedback submitted successfully")
    wait_for_enter("Press Enter to continue...", clear=True)


# 4. this function is to update the profile of the user which is loaded in from the main.py
def update_profile(cur_user):
    from main import update_profile as update_profile_main
    update_profile_main(cur_user)


# 5. this function is to logout the user which is loaded in from the main.py
def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)