import csv
from tkinter import messagebox


def file_path(acc_type) -> str:
    if acc_type == "admin":
        file_path_of_acc = "../Data/Users/login_admin.csv"
    elif acc_type == "prof":
        file_path_of_acc = "../Data/Users/login_professor.csv"
    else:
        file_path_of_acc = "../Data/Users/login_TA.csv"
    return file_path_of_acc


def create_account(username: str, password: str, acc_type: str) -> bool:
    special_chars: set = set("!@#$%^&*()-_=+[]{}|;:'\",.<>?/~`")
    valid_username = True
    valid_password = True

    with open(file_path(acc_type), 'r') as login_data:
        for row in csv.reader(login_data):
            if row[0] == username:
                messagebox.showwarning("Username already exists", "Username already exists, please select a different username.")
                valid_username = False

    if username == "":
        valid_username = False

    if len(password) < 8:
        messagebox.showwarning("Invalid Password", "Password must be at least 8 characters long")
        valid_password = False

    if any(char.isupper() for char in password) == False or any(char.islower() for char in password) == False or any(
            char.isdigit() for char in password) == False or set(password).isdisjoint(special_chars) == True:
        messagebox.showwarning("Invalid Password", """Password must Contain at least one upper case and one lower case letter
Password must contain at least one number (1-9) \
Password must Contain at least one special character""")
        valid_password = False

    if valid_username == True and valid_password == True:
        try:
            with open(file_path(acc_type), 'a', newline='') as login_data: #storing username and password
                csv.writer(login_data).writerow([username, password])
                """Hash password before saving"""
                return True
        except Exception as e:
            print("Error:",e)
    return False


def login(username: str,password: str,acc_type: str) -> bool:
    with open(file_path(acc_type), 'r') as login_data:
        for row in csv.reader(login_data):
            if row[0] == username and row[1] == password:
                return True
        return False

def retrieve_accounts(acc_type: str) -> list:
    with open(file_path(acc_type), 'r') as login_data:
        return [row[0] for row in csv.reader(login_data)]

def delete_account(index: int, acc_type: str) -> bool:
    with open(file_path(acc_type), 'r') as login_data:
        rows = list(csv.reader(login_data))
        print(rows)

        if 0 <= index < len(rows):
            print(rows.pop(index))
        else:
            print("Index out of bounds while deleting account")
            return False
        print(rows)

        try:
            with open(file_path(acc_type), "w", newline="") as new_login_data:
                writer = csv.writer(new_login_data)
                writer.writerows(rows)
        except Exception as e:
            print("Error:",e)
            return False
        else:
            return True
