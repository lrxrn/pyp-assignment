def logout(cur_usr):
    from main import logout as logout_main
    logout_main(cur_usr)

def start(cur_usr):
    print(f"Welcome, {cur_usr}!")
    print("Customer menu is currently under construction.")
    logout(cur_usr)