from tabulate import tabulate
from Modules.db import db_addKey, db_getKey, db_getAllKeys, db_deleteKey, db_getFilKeys
from Modules.utils import get_next_id, display_table, wait_for_enter, printD, inp, time_object

# Customer Menu
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
        print("Invalid choice")
        start(current_user)

# Function to display the menu
def show_menu():
    menu_keys = db_getAllKeys("menu")  # Retrieve list of menu item keys
    rows = [(key, db_getKey("menu", key)["name"], db_getKey("menu", key)["price"]) for key in menu_keys]
    display_table(["Item ID", "Name", "Price"], rows)

# Function to display the orders
def show_orders(current_user):
    order_keys = db_getAllKeys("orders")
    orders = []
    for order_id in order_keys:
        order = db_getKey("orders", order_id)
        order["order_id"] = order_id
        orders.append(order)
    user_orders = [order for order in orders if order["customer"] == current_user]
    
    if not user_orders:
        print("No orders.")
        return

    headers = ["Order ID", "Status", "Date", "Time", "Total Amount"]
    rows = [
        (order["order_id"], order["status"], order["date"], order["time"], order["details"]["totalAmount"]) 
        for order in user_orders
    ]
    display_table(headers, rows)

# 1. View and Order food
def collect_order(current_user):
    orderItems = []
    while True:
        show_menu()
        item = input("Enter item number: ").upper()
        if not db_getKey("menu", item):
            print("Invalid item number")
            continue
        quantity = int(input("Enter quantity: "))
        orderItems.append({"ID": item, "quantity": quantity})
        if input("Order more? (y/n): ").lower() == "n":
            break

    diningOpt = input("Dining option (Dine-in/Takeaway): ").lower()
    address = input("Enter address: ") if diningOpt == "takeaway" else "Dine-in"
    
    display_table(
        ["Item", "Quantity"],
        [(db_getKey("menu", i["ID"])["name"], i["quantity"]) for i in orderItems]
    )
    totalAmt = sum([db_getKey("menu", i["ID"])["price"] * i["quantity"] for i in orderItems])
    print(f"Total Amount: {totalAmt}")
    
    order_id = get_next_id("orders")
    date, time = time_object()
    db_addKey("orders", order_id, {
        "status": "Order Placed",
        "details": {
            "items": orderItems,
            "totalAmount": totalAmt,
            "diningOption": diningOpt,
            "deliveryAddress": address
        },
        "date": date,
        "time": time,
        "customer": current_user,
        "chef": "N/a",
        "payment": {"method": "", "status": "", "amount": 0, "change": 0},
        "feedback": {"rating": "", "comments": "", "response": ""}
    })
    print(f"Order placed successfully! Order ID: {order_id}")
    start(current_user)

# 2. View order status
def view_order_status(current_user):
    print(f"Orders placed by {current_user}")
    show_orders(current_user)
    start(current_user)

# 3. Send feedback
def send_feedback(current_user):
    show_orders(current_user)
    order_id = input("Enter order ID for feedback: ").upper()
    order = db_getKey("orders", order_id)

    if not order:
        print("Invalid order ID")
        start(current_user)
    
    if order["customer"] != current_user:
        print("You can only provide feedback for your own orders.")
        start(current_user)
    
    if order["status"] not in ["Delivered", "Completed"]:
        print("Feedback can only be provided for delivered or completed orders.")
        start(current_user)
    
    if order["feedback"]["rating"] != "":
        print("Feedback already provided for this order.")
        start(current_user)
    
    rating = input("Rate the food (1-5): ")
    comments = input("Additional feedback? (y/n): ").lower() == "y" and input("Enter feedback: ") or ""
    
    order["feedback"] = {"rating": rating, "comments": comments, "response": ""}
    db_addKey("orders", order_id, order)
    print("Feedback submitted successfully!")
    start(current_user)

# 4. Update profile
def update_profile(current_user):
    from main import update_profile as update_profile_main
    update_profile_main(current_user)

# 5. Logout
def logout(current_user):
    from main import logout as logout_main
    logout_main(current_user)