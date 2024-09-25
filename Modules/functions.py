import os
import re
import time
import tabulate
import datetime
import random
import configparser
projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(f"{projectRoot}/config.ini")

wordlist_path = config['Misc']['wordlist']

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
        
def generate_password():
    # return a random word list password with 3 words and a number with a capital letter delimited by -
    with open(f"{wordlist_path}", "r") as word_list:
        words = [line.strip() for line in word_list]
    
    word_choice_1 = random.choice(words)
    word_choice_2 = random.choice(words)
    
    random_index = random.randint(0, len(word_choice_1) - 1)
    word_choice_1 = word_choice_1[:random_index] + word_choice_1[random_index].upper() + word_choice_1[random_index + 1:]
    
    word_choices = [word_choice_1, str(random.randint(10, 90)), word_choice_2]
    random.shuffle(word_choices)
    password = "-".join(word_choices)
    return password

"""
Function to take user input with validation
    msg: The message to display to the user
    type: The type of input to expect (int, float, email, password, phone, date, str)
    valid_values: A list of valid values for the input
    reverse: If True, the input must not be in the valid_values list
    invalidInpMsg: A custom message to display when the input is invalid
    cancelAllowed: If True, the user can cancel the input by typing 'c'
    cancelFunc: A function to run when the user cancels the input

Returns: the user input or None if the user cancels the input
"""
def inp(msg: str="Input your value: ", type: str="str", valid_values: list=None, reverse=False, invalidInpMsg: str=None, cancelAllowed=False, cancelFunc=None):
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
                # check if it is format of dd-mmm-yyyy
                if re.fullmatch(r'\d{2}-[a-zA-Z]{3}-\d{4}', user_input):
                    try:
                        date = datetime.datetime.strptime(user_input, "%d-%b-%Y")
                        # check if the date is in the future
                        if date < datetime.datetime.now():
                            break
                        else:
                            printD("Date is in the future. Please enter a date in the past.", "yellow")
                            continue
                    except ValueError:
                        printD("Invalid date! Please try again.", "yellow")
                        continue
                else:
                    printD("Invalid date format! Please try again.", "yellow")
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