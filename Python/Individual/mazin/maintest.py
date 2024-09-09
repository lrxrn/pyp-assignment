while True:
    global user_nm
    user = input("Enter username to delete: ").lower()
    customer_file = open("customer_list", "r")
    customer_file = list(customer_file)
    for line in customer_file:
        if user == line.split(", ")[0]:
            user_nm = line
            del customer_file[customer_file.index(line)]

    with open("customer_list", "w") as f:
        for customer in customer_file:
            f.write(f"{customer}")

    try:
        print(f"Deleted user: {user_nm.split(', ')[0]}")
    except NameError:
        print("User not found")