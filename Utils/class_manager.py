import csv
import os
import pandas as pd
import openpyxl
from pandas import DataFrame

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


def store_attendance(data: DataFrame, class_name: str, in_out: str):
    student_data_path = os.path.join(BASE_DIR, "../Data/Attendance/" + class_name + "_data.xlsx")
    student_attendance_path = os.path.join(BASE_DIR, "../Data/Attendance/" + class_name + "_attendance.xlsx")

    student_data = pd.read_excel(student_data_path)
    student_attendance = pd.read_excel(student_attendance_path)

    student_data["AU_id"] = student_data["AU_id"].astype(str)
    student_attendance["AU_id"] = student_attendance["AU_id"].astype(str)

    print(student_attendance)

    date = str(data.loc[0, "Date"])
    punch_col = f"{date}_{in_out}"
    print(data)

    data["Id"] = data["Id"].apply(lambda x: f"AU{str(x)}")
    print(data)

    if punch_col not in student_data.columns:
        student_data[punch_col] = ""

    pin_col = f"{date}_in"
    pout_col = f"{date}_out"

    for i in range(len(data)):
        _id = data.loc[i, "Id"]
        _time = data.loc[i, "Time"]
        student_data.loc[student_data["AU_id"] == _id, punch_col] = _time

    if in_out == "_out":
        if date not in student_attendance.columns:
            student_attendance[date] = ""
        if pin_col in student_data.columns and pout_col in student_data.columns:
            print("pin",student_attendance[pin_col])
            print("pout",student_data[pout_col])
            for i, row in student_data.iterrows():
                print(row)
                au_id = row["AU_id"]
                pin = str(row.get(pin_col, "")).strip()
                pout = str(row.get(pout_col, "")).strip()
                student_attendance.loc[student_attendance["AU_id"] == au_id, date] = "P" if pin and pout else "A"

    print(student_attendance)

    student_data.to_excel(student_data_path, index=False)
    student_attendance.to_excel(student_attendance_path, index=False)
    return True


def add_student(au_id: str, student_name: str, class_name: str):
    _id: str = "AU"+str(au_id)
    student_data_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_data.xlsx")
    student_attendance_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_attendance.xlsx")
    print(student_data_path)
    print(student_attendance_path)

    student_data = openpyxl.load_workbook(student_data_path)
    data_sheet = student_data.active
    print(pd.read_excel(student_data_path))
    student_attendance = openpyxl.load_workbook(student_attendance_path)
    attendance_sheet = student_attendance.active
    print(pd.read_excel(student_attendance_path))

    try:
        data_sheet.append((_id, student_name))
        attendance_sheet.append((_id, student_name))
        student_data.save(student_data_path)
        student_attendance.save(student_attendance_path)
        print(pd.read_excel(student_data_path))
        print(pd.read_excel(student_attendance_path))
        return True
    except Exception as e:
        print(e)
        return False


def delete_student(au_id: str,class_name: str):
    student_data_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_data.xlsx")
    student_attendance_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_attendance.xlsx")

    student_data = pd.read_excel(student_data_path)
    student_attendance = pd.read_excel(student_attendance_path)

    new_student_data = student_data[student_data['AU_id'] != au_id]
    new_student_attendance = student_attendance[student_attendance['AU_id'] != au_id]

    new_student_data.to_excel(student_data_path, index=False)
    new_student_attendance.to_excel(student_attendance_path, index=False)

    with open(os.path.join(BASE_DIR, "../Data/Students/Details.csv"), 'r') as student_details:
        rows = list(csv.reader(student_details))

        new_rows = [row for row in rows if row[0] != au_id[2:]]

        try:
            with open(os.path.join(BASE_DIR, "../Data/Students/Details.csv"), "w", newline="") as new_login_data:
                writer = csv.writer(new_login_data)
                writer.writerows(new_rows)
        except Exception as e:
            print("Error:",e)
