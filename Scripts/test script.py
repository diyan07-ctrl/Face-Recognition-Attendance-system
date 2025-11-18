import os
import pandas as pd

class_name = "ENR106"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
student_data_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_data.xlsx")
student_attendance_path = os.path.join(BASE_DIR, "../Data/Attendance/"+class_name+"_attendance.xlsx")

student_data = pd.read_excel(student_data_path)
student_attendance = pd.read_excel(student_attendance_path)

student_data["19-11-25"+"_in"] = ""
student_data.loc[0, "19-11-25"+"_in"] = "11.56.24"

print(student_data)
print(student_attendance)