import re
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
    printD("Administrator Menu", "cyan")
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

def viewFeedback(cur_usr):
    clear_console()
    printD("Admin: View Feedback", "cyan")
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
        print("No feedback available.")
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
    printD("Admin: Manage Staff", "cyan")
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
    printD("Admin/Manage Staff: Add Staff", "cyan")
    from main import register as register_main
    register_main(cur_usr, manageStaff)

def manageStaff_removeStaff(cur_usr):
    clear_console()
    printD("Admin/Manage Staff: Remove Staff", "cyan")
    username = inp("Enter the username of the staff to remove: ", "str")
    
    if username not in db_getAllKeys("users"):
        print("User not found.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    
    # check if the user is the current user
    if username == cur_usr:
        print("You cannot remove yourself.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    
    # check if the user is a customer
    if db_getKey("usrRoles", username) == "customer":
        print("You can remove only staff.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    
    ch = inp(f"Are you sure you want to remove User '{username}'? [y/n]: ", "str", ["y", "n"])
    ch = ch.lower()
    match ch:
        case "y":
            db_deleteKey("users", username)
            db_deleteKey("passwords", username)
            print("User removed successfully.")
        case "n":
            print("Operation cancelled.")
    
    wait_for_enter()
    manageStaff(cur_usr)
    
def manageStaff_updateStaff(cur_usr):
    from main import update_profile as update_profile_main
    clear_console()
    printD("Admin/Manage Staff: Update Staff", "cyan")
    usr = inp("Enter the username of the staff to update: ", "str")
    if usr not in db_getAllKeys("users"):
        print("User not found.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    if usr == cur_usr:
        print("You cannot update yourself. Please use the 'Update Profile' option.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    if db_getKey("users", usr)["role"] == "customer":
        print("You can update only staff.")
        wait_for_enter()
        manageStaff(cur_usr)
        return
    update_profile_main(usr, cur_usr, None, manageStaff) 

def manageStaff_viewStaff(cur_usr):
    clear_console()
    printD("Admin/Manage Staff: View Staff", "cyan")
    staff = db_getAllKeys("users")
    staff = [usr for usr in staff if db_getKey("users", usr)["role"] != "customer"]
    table_headers = ["#", "Username", "Name", "Role"]
    table_data = []
    for i, staff in enumerate(staff):
        table_data.append([i+1, staff, db_getKey("users", staff)["name"], db_getKey("users", staff)["role"]])
        
    display_table(table_headers, table_data)
    print(f"Total Staff: {len(staff)-1}")
    wait_for_enter()
    manageStaff(cur_usr)