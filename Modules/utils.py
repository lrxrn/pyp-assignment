import os
import re
import time
import tabulate
import datetime
import random
import configparser
import base64
from pwinput import pwinput
from rich.console import Console
from rich.table import Table
from rich import box
projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(f"{projectRoot}/config.ini")

wordlist_path = config['Misc']['wordlist']

log_path = config['Misc']['log_file']

def log(msg, log_type="info", file_name=None):
    """Function to log messages to a log file

    Args:
        msg (str): The message to log
        log_type (str, optional): Type of log entry. Defaults to "info".
        file_name (str, optional): File to save log entry to. Defaults to None.
    """
    with open(f"{log_path}","a") as log_file:
        log_file.write(f"[{datetime.datetime.strftime(datetime.datetime.now(), '%d-%b-%Y %I:%M %p')}] [{log_type.upper()}] [{file_name if file_name is not None else "Program"}] {msg}\n")

def time_object():
    """Function to get the current date and time

    Returns:
        tuple: A tuple containing the current date and time
    """
    now = datetime.datetime.now()
    return now.strftime('%d-%b-%Y'), now.strftime('%I:%M %p')

# Function to get the difference between two dates
# Function to get the difference between two dates
def date_diff(datetime1, datetime2=datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p"), type="normal"):
    if type == "dob":
        datetime2 = datetime.datetime.now().strftime("%d-%b-%Y")
        
        date1 = datetime.datetime.strptime(datetime1, "%d-%b-%Y")
        date2 = datetime.datetime.strptime(datetime2, "%d-%b-%Y")
    else:
        date1 = datetime.datetime.strptime(datetime1, "%d-%b-%Y %I:%M %p")
        date2 = datetime.datetime.strptime(datetime2, "%d-%b-%Y %I:%M %p")
    
    diff = date2 - date1
    seconds = diff.total_seconds()
    
    if seconds < 0:
        past = False
        seconds = abs(seconds)
    else:
        past = True
        
    formatted_time = int(f"{seconds:.0f}")
    
    if seconds == 0:
        return "Just now"
    elif seconds < 60:
        time_str = f"{formatted_time} second{"" if formatted_time == 1 else "s"}"
    elif seconds < 3600: # 60 * 60 = 3600
        minutes = seconds // 60
        formatted_time = int(f"{minutes:.0f}")
        time_str = f"{formatted_time} minute{"" if formatted_time == 1 else "s"}"
    elif seconds < 86400: # 24 * 60 * 60 = 86400
        hours = seconds // 3600
        formatted_time = int(f"{hours:.0f}")
        time_str = f"{formatted_time} hour{"" if formatted_time == 1 else "s"}"
    elif seconds < 2592000: # 30 * 24 * 60 * 60 = 2592000
        days = seconds // 86400
        formatted_time = int(f"{days:.0f}")
        time_str = f"{formatted_time} day{"" if formatted_time == 1 else "s"}"
    else:
        months = (date2.year - date1.year) * 12 + date2.month - date1.month
        if months < 12:
            formatted_time = int(f"{months:.0f}")
            time_str = f"{formatted_time} month{"" if formatted_time == 1 else "s"}"
        else:
            years = months // 12
            formatted_time = int(f"{years:.0f}")
            time_str = f"{formatted_time} year{"" if formatted_time == 1 else "s"}"
    
    match type:
        case "dob":
            return f"{time_str}"
        case _:
            if past:
                return f"{time_str} ago"
            else:
                return f"in {time_str}"

# Clear console function to de-clutter the console
def clear_console(wait_time=None):
    # Wait for specifc time before clearing the console
    if wait_time:
        wait_for(wait_time)
    
    # Clear the console
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
        
def wait_for(seconds=1):
    time.sleep(seconds)

# Function to wait for user to press Enter
def wait_for_enter(msg="Press Enter to proceed...", clear=False):
    pwinput(prompt=msg, mask='')
    if clear:
        clear_console()
        
# Function to get the next available ID for a given database
def get_next_id(DBName, prefix="UNK"):
    from Modules.db import db_getAllKeys
    data = db_getAllKeys(DBName)
    # ORD-001
    if data:
        ids = [int(item.split("-")[1]) for item in data]
        prefix = data[0].split("-")[0]
        new_id = max(ids) + 1
    else:
        new_id = 1
    
    return f"{prefix}-{new_id:03}"
        
# Function that takes in Menu Item Name and Category and generates a unique ID
def generate_id(name, category):
    return f"{name[:3].upper()}{category[:3].upper()}{int(time.time())}"
        
# Function to display a table
def display_table(headers=[], data=[], tablefmt="rounded_grid"):
    # bold out the data using color_text function
    headers = [color_text(header, "bold") for header in headers]
    print(tabulate.tabulate(data, headers=headers, tablefmt=tablefmt))
    
def display_rich_table(data, title, title_style="black on white"):
    table = Table(title=title, show_header=False, box=box.ROUNDED, show_lines=False, title_style=title_style, row_styles=["", "dim"])

    for row in data:
        table.add_row(*row)

    console = Console()
    console.print(table)

# Function to color text
def color_text(text, color="white", bold=False):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "pink": "\033[95m",
        "white": "\033[97m",
        "dim": "\033[2m",
        "bold": "\033[1m",
        "end": "\033[0m"
    }
    if bold:
        return f"{colors['bold']}{colors[color]}{text}{colors['end']}"
    else:
        return f"{colors[color]}{text}{colors['end']}"

# Function to display messages in color
def printD(msg, color="white", bold=False):
    """Function to display messages in color

    Args:
        msg (str): The message to display
        color (str, optional): The color to display the message in. Defaults to "white".
        bold (bool, optional): If True, the message will be displayed in bold. Defaults to False.
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "pink": "\033[95m",
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

def encode_password(password):
    return base64.b64encode(password.encode()).decode()

def decode_password(encoded_password):
    return base64.b64decode(encoded_password.encode()).decode()

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
def inp(msg: str="Input your value: ", type: str="str", valid_values: list=None, reverse=False, invalidInpMsg: str=None, cancelAllowed=False, cancelFunc=None, stringUpperSensitive=False):
    if cancelAllowed:
        if cancelFunc is None:
            cancelFunc = lambda: None
        if valid_values:
            valid_values = valid_values + ["c"]
        msg = f"{msg} (Type 'c' to cancel): "
        
    # stringCaseSensitive is only applicable to string type
    if type == "str" and stringUpperSensitive:
        valid_values = [str(val).upper() for val in valid_values]
    
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
            valid_values_str = ", ".join(str(value) for value in valid_values)
            printD(f"Invalid input! Expected one of ({valid_values_str}). Please try again.", "yellow")
    
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
        case "pwd":
            user_input = pwinput(prompt=msg, mask='*')
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
                if stringUpperSensitive:
                    user_input = user_input.upper()
                if is_valid(user_input):
                    break
                else:
                    output_invalid_msg()
                    continue
            return user_input