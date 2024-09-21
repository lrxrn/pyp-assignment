import os
import re
import time
import tabulate


# Clear console function to de-clutter the console
def clear_console(wait_time=None):
    # Wait for specifc time before clearing the console
    if wait_time:
        time.sleep(wait_time)
    
    # Clear the console
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

# Function to wait for user to press Enter
def wait_for_enter(msg="Press Enter to proceed...", clear=False):
    input(msg)
    if clear:
        clear_console()
        
# Function that takes in Menu Item Name and Category and generates a unique ID
def generate_id(name, category):
    return f"{name[:3].upper()}{category[:3].upper()}{int(time.time())}"
        
# Function to display a table
def display_table(headers, data):
    print(tabulate.tabulate(data, headers=headers, tablefmt="grid"))
    
# Function to display messages in color
def printD(msg, color="white", bold=False):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "end": "\033[0m"
    }
    if bold:
        print(f"{colors['bold']}{colors[color]}{msg}{colors['end']}")
    else:
        print(f"{colors[color]}{msg}{colors['end']}")

def inp(msg="Input your value: ", type="str", valid_values=None, reverse=False, invalidInpMsg=None, cancelAllowed=False, cancelFunc=None):
    if cancelAllowed:
        if cancelFunc is None:
            cancelFunc = lambda: None
        valid_values = valid_values + ["c"]
        msg = f"{msg} (Type 'c' to cancel): "
    
    def is_valid(value):
        if valid_values is None:
            return True
        if reverse:
            return value not in valid_values
        else:
            return value in valid_values
        
    def output_invalid_msg():
        if invalidInpMsg:
            print(invalidInpMsg)
        else:
            printD(f"Invalid input! Expected one of {valid_values}. Please try again.", "yellow")
    
    match type:
        case "int":
            while True:
                try:
                    user_input = input(msg)
                    if cancelAllowed and user_input.lower() == 'c':
                        cancelFunc()
                        return None
                    value = int(user_input)
                    if is_valid(value):
                        break
                    else:
                        output_invalid_msg()
                        continue
                except ValueError:
                    printD("Invalid input type! Expected an integer. Please try again.", "yellow")
            return value
        case "float":
            while True:
                try:
                    user_input = input(msg)
                    if cancelAllowed and user_input.lower() == 'c':
                        cancelFunc()
                        return None
                    value = float(user_input)
                    if is_valid(value):
                        break
                    else:
                        output_invalid_msg()
                        continue
                except ValueError:
                    printD("Invalid input type! Expected a float. Please try again.", "yellow")
            return value
        case "email":
            while True:
                user_input = input(msg)
                if cancelAllowed and user_input.lower() == 'c':
                    cancelFunc()
                    return None
                if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
                    if is_valid(user_input):
                        break
                    else:
                        output_invalid_msg()
                        continue
                else:
                    printD(f"Invalid email format! Please try again.", "yellow")
            return user_input
        case "password":
            while True:
                user_input = input(msg)
                if cancelAllowed and user_input.lower() == 'c':
                    cancelFunc()
                    return None
                if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', user_input):
                    break
                else:
                    printD(f"Password does not meet requirements. It must be at least 8 characters long and include uppercase letters, lowercase letters, digits, and special characters (@#$%^&+=). \nPlease try again.", "yellow")
            return user_input
        case "phone":
            while True:
                user_input = input(msg)
                if cancelAllowed and user_input.lower() == 'c':
                    cancelFunc()
                    return None
                if re.fullmatch(r'\+?\d{10,12}', user_input):
                    break
                else:
                    printD(f"Invalid phone number format! (e.g. +1234567890) Please try again.", "yellow")
            return user_input
        case "date":
            while True:
                user_input = input(msg)
                if cancelAllowed and user_input.lower() == 'c':
                    cancelFunc()
                    return None
                if re.fullmatch(r'\d{4}-\d{2}-\d{2}', user_input):
                    break
                else:
                    printD(f"Invalid date format! (e.g. 2021-01-01) Please try again.", "yellow")
            return user_input
        case _:
            while True:
                user_input = input(msg)
                if cancelAllowed and user_input.lower() == 'c':
                    cancelFunc()
                    return None
                if is_valid(user_input):
                    break
                else:
                    output_invalid_msg()
                    continue
            return user_input