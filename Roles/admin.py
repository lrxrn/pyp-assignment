import re
import datetime
import base64

from Modules.db import db_addKey, db_deleteKey, db_updateKey, db_getKey, db_getAllKeys, db_getAllValues
from Modules.functions import clear_console, inp, printD, wait_for_enter, generate_password, display_table

def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)
    
def update_profile(cur_usr, return_func):
    from main import update_profile as update_profile_main
    update_profile_main(cur_usr, return_func)
    
def start(cur_usr):
    clear_console()
    printD("Administrator Menu", "magenta")
    print("1. Manage staff")
    print("2. View sales report")
    print("3. View feedback")
    print("4. Update profile")
    print("5. Logout")
    ch = inp("Enter your choice: ", "int", [1, 2, 3, 4, 5])
    match ch:
        case 1:
            manageStaff(cur_usr)
        case 2:
            viewSalesReport(cur_usr)
        case 3:
            viewFeedback(cur_usr)
        case 4:
            update_profile(cur_usr, start)
        case 5:
            logout(cur_usr)
            
def viewSalesReport(cur_usr):
    clear_console()
    printD("Admin: View Sales Report", "magenta")
    orders = db_getAllKeys("orders")
    sales = []
    for order in orders:
        order_details = db_getKey("orders", order)
        sales.append({"order_id": order, "customer": order_details["customer"], "chef": order_details["chef"], "date": order_details["date"], "total_price": order_details["OrderDetails"]["TotalAmount"]})
    
    if sales is []:
        print("No sales available.")
        wait_for_enter()
        start(cur_usr)
        return
    
    print("Choose a filter to view the sales report: \n1. Yearly \n2. Monthly \n3. By Chef \n4. Back")
    inp_choice = inp("Enter your choice: ", "int", [1, 2, 3, 4, 5])
    match inp_choice:
        case 1:
            input_year = inp("Enter the year to view the sales report: ", "int")
            sales = [sale for sale in sales if datetime.datetime.strptime(sale["date"], "%d-%b-%Y").year == input_year]
            
            if len(sales) == 0:
                print(f"No sales available for the year {input_year}.")
                wait_for_enter()
                start(cur_usr)
                return
            
            print(f"Sales Report for the year {input_year}")
            print(f"Total orders: {len(sales)}")
            print(f"Total amt in sales: {sum([sale['total_price'] for sale in sales])}")
            print(f"Average amt per order: {sum([sale['total_price'] for sale in sales])/len(sales)}")
            print(f"Total customers: {len(set([sale['customer'] for sale in sales]))}")
            
        case 2:
            input_year = inp("Enter the year to view the monthly sales report: ", "int")
            sales = [sale for sale in sales if datetime.datetime.strptime(sale["date"], "%d-%b-%Y").year == input_year]
            
            if len(sales) == 0:
                print(f"No sales available for the year {input_year}.")
                wait_for_enter()
                start(cur_usr)
                return
            
            table_headers = ["Month", "Total Orders", "Total Sales", "Average Sales", "Total Customers"]
            table_data = []
            data_months = {}
            
            for sale in sales:
                if datetime.datetime.strptime(sale["date"], "%d-%b-%Y").month not in data_months:
                    data_months[datetime.datetime.strptime(sale["date"], "%d-%b-%Y").month] = []
                
                data_months[datetime.datetime.strptime(sale["date"], "%d-%b-%Y").month].append(sale)
                
            for month in data_months:
                month_sales = data_months[month]
                total_sales = sum([sale['total_price'] for sale in month_sales])
                table_data.append([datetime.date(1900, month, 1).strftime('%B'), len(month_sales), total_sales, total_sales/len(month_sales), len(set([sale['customer'] for sale in month_sales]))])
                
            display_table(table_headers, table_data)
            
        case 3:
            table_headers = ["Chef", "Total Orders", "Total Sales", "Average Sales", "Total Customers"]
            table_data = []
            data_chefs = {}
            
            for sale in sales:
                if sale["chef"] not in data_chefs:
                    data_chefs[sale["chef"]] = []
                
                data_chefs[sale["chef"]].append(sale)
                
            for chef in data_chefs:
                chef_sales = data_chefs[chef]
                total_sales = sum([sale['total_price'] for sale in chef_sales])
                table_data.append([chef, len(chef_sales), total_sales, total_sales/len(chef_sales), len(set([sale['customer'] for sale in chef_sales]))])
            
            display_table(table_headers, table_data)
            
        case _:
            start(cur_usr)
            
    wait_for_enter()
    start(cur_usr)

def viewFeedback(cur_usr):
    clear_console()
    printD("Admin: View Feedback", "magenta")
    orders = db_getAllKeys("orders")
    feedback_objs = []
    feedback_ratings = []
    for order in orders:
        feedback_custmr = db_getKey("orders", order)["customer"]
        feedback = db_getKey("orders", order)["feedback"]
        if feedback is {}:
            continue
        else:
            feedback_rating = db_getKey("orders", order)["feedback"]["rating"]
            feedback_comment = db_getKey("orders", order)["feedback"]["comments"]
            feedback_response = db_getKey("orders", order)["feedback"]["response"]
            feedback_objs.append({"order_id": order, "customer": feedback_custmr,  "rating": feedback_rating, "comments": feedback_comment, "response": feedback_response})
    
    feedbackOrders = [feedback_obj["order_id"] for feedback_obj in feedback_objs]
    for feedback_obj in feedback_objs:
        if feedback_obj is None:
            return
        
        feedback_ratings.append(feedback_obj["rating"])
    
    if feedback_ratings is []:
        printD("No feedback available.", "red")
        wait_for_enter()
        start(cur_usr)
        return
    
    table_headers = ["Order_ID", "Customer", "Rating", "Feedback", "Responded?"]
    table_data = []
    for feedback_obj in feedback_objs:
        responded = "Yes" if feedback_obj["response"] else "No"
        table_data.append([feedback_obj["order_id"], feedback_obj["customer"], feedback_obj["rating"], feedback_obj["comments"], responded])
        
    display_table(table_headers, table_data)
    
    ch = inp("Do you want to view a feedback? [y/n]: ", "str", ["y", "n"])
    ch = ch.lower()
    match ch:
        case "y":
            order_id = inp("Enter the Order ID to respond to: ", "str")
            if order_id not in feedbackOrders:
                print("OrderID does not have a feedback or does not exist.")
                wait_for_enter()
                start(cur_usr)
                return
            print("Order ID: ", order_id.upper())
            print("Customer: ", db_getKey("orders", order_id)["customer"])
            print("Rating: ", db_getKey("orders", order_id)["feedback"]["rating"])
            print("Feedback: ", db_getKey("orders", order_id)["feedback"]["comments"])
            print("Response: ", db_getKey("orders", order_id)["feedback"]["response"])
            
            ch2 = inp("Do you want to respond to this feedback? [y/n]: ", "str", ["y", "n"])
            ch2 = ch2.lower()
            match ch2:
                case "y":
                    response = inp("Enter your response: ", "str")
                    feedback = db_getKey("orders", order_id)
                    feedback["feedback"]["response"] = response
                    db_updateKey("orders", order_id, feedback)
                    print("Response added successfully.")
                    
                case "n":
                    print("Operation cancelled.")
            
        case "n":
            print("Operation cancelled.")
            
    wait_for_enter()
    start(cur_usr)


def manageStaff(cur_usr):
    clear_console()
    printD("Admin: Manage Staff", "magenta")
    print("1. Add staff")
    print("2. Remove staff")
    print("3. Update staff")
    print("4. View staff")
    print("5. Back")
    ch = inp("Enter your choice: ", "int", [1, 2, 3, 4, 5])
    match ch:
        case 1:
            manageStaff_addStaff(cur_usr)
        case 2:
            manageStaff_removeStaff(cur_usr)
        case 3:
            manageStaff_updateStaff(cur_usr)
        case 4:
            manageStaff_viewStaff(cur_usr)
        case 5:
            start(cur_usr)

def manageStaff_addStaff(cur_usr):
    clear_console()
    printD("Admin/Manage Staff: Add Staff", "magenta")
    from main import register as register_main
    register_main(cur_usr, manageStaff)

def manageStaff_removeStaff(cur_usr):
    clear_console()
    printD("Admin/Manage Staff: Remove Staff", "magenta")
    username = inp("Enter the username of the staff to remove: ", "str")
    
    if username not in db_getAllKeys("users"):
        print("User not found.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    
    # check if the user is the current user
    if username == cur_usr:
        printD("You cannot remove yourself.", "red")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    
    # check if the user is a customer
    if db_getKey("usrRoles", username) == "customer":
        printD("You can remove only staff.", "red")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    
    ch = inp(f"Are you sure you want to remove User '{username}'? [y/n]: ", "str", ["y", "n"])
    ch = ch.lower()
    match ch:
        case "y":
            db_deleteKey("users", username)
            db_deleteKey("passwords", username)
            printD("User removed successfully.", "green")
        case "n":
            printD("Operation cancelled.", "yellow")
    
    wait_for_enter()
    manageStaff(cur_usr)
    
def manageStaff_updateStaff(cur_usr):
    from main import update_profile as update_profile_main
    clear_console()
    printD("Admin/Manage Staff: Update Staff", "magenta")
    usr = inp("Enter the username of the staff to update: ", "str")
    if usr not in db_getAllKeys("users"):
        print("User not found.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    if usr == cur_usr:
        printD("You cannot update yourself. Please use the 'Update Profile' option.", "yellow")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    if db_getKey("users", usr)["role"] == "customer":
        printD("You can update only staff.", "red")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    update_profile_main(usr, cur_usr, None, manageStaff) 

def manageStaff_viewStaff(cur_usr):
    clear_console()
    printD("Admin/Manage Staff: View Staff", "magenta")
    staff = db_getAllKeys("users")
    staff = [usr for usr in staff if db_getKey("users", usr)["role"] != "customer"]
    table_headers = ["#", "Username", "Name", "Role"]
    table_data = []
    for i, staff in enumerate(staff):
        table_data.append([i+1, staff, db_getKey("users", staff)["name"], db_getKey("users", staff)["role"]])
        
    display_table(table_headers, table_data)
    printD(f"Total Staff: {len(staff)-1}", "white", True)
    wait_for_enter()
    manageStaff(cur_usr)