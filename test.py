from Modules.functions import generate_password
import base64

while True:
    password = generate_password()
    print(f"Generated password: {password} ({base64.b64encode(password.encode()).decode()})")