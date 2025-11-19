from tkinter import messagebox
import cv2
import os
import pandas as pd
import datetime
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
TRAINER_PATH = os.path.join(DATA_DIR, "TrainingImageLabel", "Trainer.yml")
CASCADE_PATH = os.path.join(DATA_DIR, "haarcascade_frontalface_default.xml")
STUDENT_CSV = os.path.join(DATA_DIR, "Students", "Details.csv")


def track_images():
    try:
        if not os.path.exists(TRAINER_PATH):
            messagebox.showerror("Error", f"Trainer.yml not found:\n{TRAINER_PATH}")
            return

        if not os.path.exists(STUDENT_CSV):
            messagebox.showerror("Error", f"student_details.csv not found:\n{STUDENT_CSV}")
            return

        if not os.path.exists(CASCADE_PATH):
            messagebox.showerror("Error", f"Cascade file missing:\n{CASCADE_PATH}")
            return

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(TRAINER_PATH)

        faceCascade = cv2.CascadeClassifier(CASCADE_PATH)

        df = pd.read_csv(STUDENT_CSV, header=None, names=["Id", "Name"])

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
                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                    name_row = df[df['Id'] == Id]

                    if not name_row.empty:
                        name = name_row['Name'].values[0]
                        label = f"{Id} - {name}"
                        attendance.loc[len(attendance)] = [Id, name, date, timestamp]
                    else:
                        label = f"{Id} - Unknown"

                else:
                    label = "Unknown"

                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(im, label, (x, y - 10), font, 0.75, (0, 255, 0), 2)

            cv2.imshow("Tracking Attendance", im)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        attendance.drop_duplicates(subset=['Id'], inplace=True)
        return attendance

    except Exception as e:
        messagebox.showerror("Error", f"Attendance tracking failed.\nError: {e}")
