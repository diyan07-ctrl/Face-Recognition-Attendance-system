from tkinter import messagebox
import cv2
import os
import csv
import numpy as np
from PIL import Image
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
FACES_DIR = os.path.join(DATA_DIR, "Faces")
TRAINER_DIR = os.path.join(DATA_DIR, "TrainingImageLabel")
STUDENT_DIR = os.path.join(DATA_DIR, "Students")
CASCADE_PATH = os.path.join(DATA_DIR, "haarcascade_frontalface_default.xml")
TRAINER_PATH = os.path.join(TRAINER_DIR, "Trainer.yml")

os.makedirs(FACES_DIR, exist_ok=True)
os.makedirs(TRAINER_DIR, exist_ok=True)
os.makedirs(STUDENT_DIR, exist_ok=True)


def take_images(au_id: str, stud_name: str):
    Id = au_id
    name = stud_name

    if not os.path.exists(CASCADE_PATH):
        messagebox.showerror("Error", f"Face detector file not found:\n{CASCADE_PATH}")
        return

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(CASCADE_PATH)
    sampleNum = 0

    while True:
        ret, img = cam.read()
        if not ret:
            messagebox.showerror("Camera Error", "Failed to read from camera.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1

            img_path = os.path.join(FACES_DIR, f"{name}.{Id}.{sampleNum}.jpg")
            cv2.imwrite(img_path, gray[y:y + h, x:x + w])

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow("Capturing Image", img)

        if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= 30:
            break

    cam.release()
    time.sleep(0.1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    if sampleNum >= 30:
        student_file = os.path.join(STUDENT_DIR, "Details.csv")

        with open(student_file, "a+", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Id, name])

        messagebox.showinfo("Success", f"Images Saved for {name} ({Id})")
        train_images()

    else:
        messagebox.showwarning("Capture Incomplete",
                               f"Only {sampleNum} images captured, training skipped.")


def train_images():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Ids = get_images_and_labels(FACES_DIR)

    if not faces:
        messagebox.showerror("Error", "No images found for training.")
        return

    recognizer.train(faces, np.array(Ids))
    recognizer.save(TRAINER_PATH)

    messagebox.showinfo("Training Complete",
                        f"Model trained successfully.\nSaved at:\n{TRAINER_PATH}")


def get_images_and_labels(folder):
    imagePaths = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".jpg")
    ]

    faces, Ids = [], []

    for img_path in imagePaths:
        try:
            pilImage = Image.open(img_path).convert('L')
            imageNp = np.array(pilImage, 'uint8')

            # filename format: name.ID.sample.jpg
            Id = int(os.path.basename(img_path).split(".")[1])

            faces.append(imageNp)
            Ids.append(Id)

        except Exception as e:
            print(f"[Error] Could not load {img_path}: {e}")

    return faces, Ids
