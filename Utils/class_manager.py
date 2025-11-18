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

def store_attendance(data: DataFrame, class_name, in_out: str):
    student_data_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_data.xlsx")
    student_attendance_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_attendance.xlsx")

    student_data = pd.read_excel(student_data_path)
    student_attendance = pd.read_excel(student_attendance_path)

    _date = str(data.loc[0, 'Date'])+str(in_out)
    student_data[_date] = ""
    student_attendance[_date] = ""
    print(student_data)

    if str(data.loc[0, 'Date'])+"_in" in student_data.columns and str(data.loc[0, 'Date'])+"_out" in student_data.columns:
        print(f"Column '{column_name_to_check}' exists in the DataFrame.")
    else:


    try:
        for i in range(len(data)):
            _id = data.loc[i, "Id"]
            _time = data.loc[i, "Time"]
            student_data.loc[student_data["AU_id"] == "_id", _date] = _time
        return True
    except Exception as e:
        print(e)
        return False


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
