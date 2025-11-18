from tkinter import messagebox
import cv2
import os
import pandas as pd
import datetime
import time


def track_images():
    try:

        if not os.path.exists("TrainingImageLabel/Trainer.yml"):
            messagebox.showerror("Error","Trainer.yml not found. Please train images in 'register_train.py' first.")
        if not os.path.exists("Students/Details.csv"):
            messagebox.showerror("Error","EmployeeDetails.csv not found. Please capture images in 'register_train.py' first.")

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel/Trainer.yml")
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        df = pd.read_csv("Students/Details.csv", header=None, names=["Id", "Name"])
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        attendance = pd.DataFrame(columns=['Id', 'Name', 'Date', 'Time'])

        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                if conf < 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                    name_data = df[df['Id'] == Id]

                    if not name_data.empty:
                        name = name_data['Name'].values[0]
                        label = f"{Id} - {name} (Present)"
                        # Log attendance
                        attendance.loc[len(attendance)] = [Id, name, date, timeStamp]
                    else:
                        label = f"{Id} - Unknown (No Record)"
                else:
                    label = "Unknown"

                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(im, label, (x, y - 10), font, 0.75, (0, 255, 0), 2)

            cv2.imshow('Tracking Attendance', im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        # Save attendance log
        attendance.drop_duplicates(subset=['Id'], inplace=True)
        return attendance

    except Exception as e:
        messagebox.showerror("Error",
                             f"Attendance tracking failed. Ensure files exist and camera works. Error: {e}")
