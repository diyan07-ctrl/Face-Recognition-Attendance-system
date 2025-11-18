from tkinter import messagebox
import cv2
import os
import csv
import numpy as np
from PIL import Image
import time



def take_images(au_id: str,stud_name: str):
    Id = au_id
    name = stud_name

    cascade_path = "haarcascade_frontalface_default.xml"
    if not os.path.exists(cascade_path):
        messagebox.showerror("Error", f"Face detector file not found: {cascade_path}")
        return

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cascade_path)
    sampleNum = 0

    os.makedirs("Faces", exist_ok=True)

    while True:
        ret, img = cam.read()
        if not ret:
            messagebox.showerror("Camera Error", "Failed to read image from camera.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleNum += 1
            cv2.imwrite(f"Faces/{name}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow('Capturing Image', img)

        if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= 30:
            break

    cam.release()
    time.sleep(0.1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    if sampleNum >= 30:
        os.makedirs("Students", exist_ok=True)
        with open('Students/Details.csv', 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Id, name])

        messagebox.showinfo("Success", f"Images Saved for ID: {Id}, Name: {name}")

        # Auto-Train Feature
        train_images()
    else:
        messagebox.showwarning("Capture Incomplete", f"Only {sampleNum} images were captured. Training skipped.")

def train_images():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Ids = get_images_and_labels("Faces")

    if not faces:
        messagebox.showerror("Error", "No images found for training. Please capture images first.")
        return

    recognizer.train(faces, np.array(Ids))

    os.makedirs("TrainingImageLabel", exist_ok=True)
    recognizer.save("TrainingImageLabel/Trainer.yml")

    messagebox.showinfo("Training Complete", "Model trained successfully!")

def get_images_and_labels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    faces, Ids = [], []
    for imagePath in imagePaths:
        try:
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)
        except Exception as e:
            print(f"Error loading {imagePath}: {e}")
    return faces, Ids


