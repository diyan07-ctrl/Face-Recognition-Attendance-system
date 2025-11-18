import csv
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def retrieve_classes(user:str, acc_type: str) -> list:
    classes = []
    print(os.path.join(BASE_DIR, "../Data/classes.csv"))
    try:
        with open(os.path.join(BASE_DIR, "../Data/classes.csv"), "r") as class_data:
            reader = csv.DictReader(class_data)
            for row in reader:
                if row[acc_type] == user:
                    classes.append(row)
    except Exception as e:
        print(e)
    return classes


def retrieve_class_attendance(_class: str):
    file_path=os.path.join(BASE_DIR, "../Data/Attendance/"+_class+"_attendance.xlsx")
    return pd.read_excel(file_path)

def store_attendance(_class: str):
    print("WIP")

def add_student(au)
