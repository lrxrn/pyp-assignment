import os
import re
import time
from tabulate import tabulate


# Clear console function to de-clutter the console
def clear_console(wait_time=None):
    # Wait for specifc time before clearing the console
    if wait_time:
        time.sleep(wait_time)
    os.system('clear' if os.name == 'posix' else 'cls')

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
    print(tabulate(data, headers=headers, tablefmt="grid"))

def inp(msg="Input your value: ", type="str"):
    match type:
        case "int":
            while True:
                try:
                    value = int(input(msg))
                    break
                except ValueError:
                    print("Invalid input! Expected an integer. Please try again.")
            return value
        case "float":
            while True:
                try:
                    value = float(input(msg))
                    break
                except ValueError:
                    print("Invalid input! Expected a float. Please try again.")
            return value
        case "email":
            while True:
                value = input(msg)
                if re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    break
                else:
                    print("Invalid email! Please try again.")
        case _:
            while True:
                value = input(msg)
                break
            return value