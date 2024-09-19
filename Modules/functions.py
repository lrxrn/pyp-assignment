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

def inp(msg="Input your value: ", type="str", valid_values=None):
    def is_valid(value):
        return valid_values is None or value in valid_values

    match type:
        case "int":
            while True:
                try:
                    value = int(input(msg))
                    if is_valid(value):
                        break
                    else:
                        print(f"Invalid input! Expected one of {valid_values}. Please try again.")
                except ValueError:
                    print("Invalid input! Expected an integer. Please try again.")
            return value
        case "float":
            while True:
                try:
                    value = float(input(msg))
                    if is_valid(value):
                        break
                    else:
                        print(f"Invalid input! Expected one of {valid_values}. Please try again.")
                except ValueError:
                    print("Invalid input! Expected a float. Please try again.")
            return value
        case "email":
            while True:
                value = input(msg)
                if re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    if is_valid(value):
                        break
                    else:
                        print(f"Invalid email! Expected one of {valid_values}. Please try again.")
                else:
                    print(f"Invalid email! Please try again.")
            return value
        case "password":
            while True:
                value = input(msg)
                if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', value):
                    break
                else:
                    print(f"Password does not meet requirements. Please try again.")
            return value
        case _:
            while True:
                value = input(msg)
                if is_valid(value):
                    break
                else:
                    print(f"Invalid input! Expected one of {valid_values}. Please try again.")
            return value