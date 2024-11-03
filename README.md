# PYP Assignment

This project is a Python-based application for managing a restaurant's orders, ingredients, and user profiles.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
  - [Database Functions](#database-functions)
  - [Utility Functions](#utility-functions)
- [File Structure](#file-structure)
- [License](#license)

## Features

- Manage orders and ingredients
- User profile management
- Role-based access control (Admin, Chef, Customer, Manager)
- Display data in tabular format

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd PYP-assignment
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the `main.py` file:
```sh
python main.py
```

## File Structure

```
.
├── CODE_OF_CONDUCT.md
├── Data
│   ├── ingredients.json
│   ├── menu.json
│   ├── orders.json
│   ├── passwords.json
│   └── users.json
├── LICENSE
├── Modules
│   ├── db.py
│   └── utils.py
├── README.md
├── Roles
│   ├── admin.py
│   ├── chef.py
│   ├── customer.py
│   └── manager.py
├── config.ini
├── file_strcuture.txt
├── main.py
├── output.txt
├── requirements.txt
└── wordlist.txt

4 directories, 20 files
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.