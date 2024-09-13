import json

print("-" * 50)
new_customer_username = input("Enter new customer username (type \"c\" to cancel): ")
new_customer_password = input("Enter new customer password (type \"c\" to cancel): ")

try:
    with open('passwords.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

data[new_customer_username] = {
    "password": new_customer_password
}

with open('passwords.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Customer added successfully.")