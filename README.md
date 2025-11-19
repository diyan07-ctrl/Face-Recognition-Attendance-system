
Face Recognition Attendance System
=

======================================================================

Dummy Username: guest

Dummy Password: guest

======================================================================

This system offers a robust and efficient solution for managing attendance through facial recognition technology. It is structured into two distinct modules: Registration & Training and Real-Time Recognition & Tracking. The system utilises OpenCV for computer vision tasks and standard Python libraries for data management and graphical user interface (GUI) development.

# Core Features

- Integrated Registration Workflow: The system handles student data input, image capture, and model training within a single, streamlined process (register.py).

- Automatic Training: The facial recognition model is automatically trained upon the successful capture of the required face samples, eliminating the need for manual intervention.

- High-Fidelity Capture: Captures 30 unique face samples per user to ensure a high-accuracy training set.

- Secure Data Storage: Student details and attendance logs are saved in structured CSV formats.

- Real-Time Attendance: Utilises the trained model (Trainer.yml) to identify students in a live video stream and record their attendance instantly (recognize.py).

# Setup and Installation
1. Prerequisites:

Before starting, ensure you have the following installed: 
-       Python 3  
 -     A functional webcam

2. Installing Dependencies:

All necessary dependencies will be downloaded automatically

3. Face Detector Configuration:
 
The system relies on a pre-trained Haar Cascade classifier for initial face detection. (included in the zip file)


🚀 Features
✅ Admin Features

Create/Remove accounts for Professors and TAs

View all registered accounts

Highly secure access control

🧑‍🏫 Professor Features

View classes assigned

Punch In / Punch Out attendance

Add or delete students

Live camera-based face detection

View attendance summary for each student

🎓 TA Features

Punch In / Punch Out attendance

View class roster

Support instructors in marking attendance

🧍‍♂️ Student Management

Add students with AU ID

Capture face images for recognition

Save student metadata to Excel

📊 Attendance Workflow

The system uses a two-phase attendance process:

🔹 Punch In

Every detected student is marked Present (P)

Those not detected remain Absent (A)

🔹 Punch Out

Only students who appear again get final Present (P)

Others are converted to Absent (A)

Ensures students do not leave mid-lecture

📁 Project Structure
AttendanceSystem/
│
├── main.py                         # Main Tkinter application
│
├── Utils/
│   ├── account_manager.py          # Login system and account storage
│   ├── class_manager.py            # Class, student, and attendance handling
│   ├── helpers.py                  # GUI helper utilities
│
├── recognize.py                    # Real-time face recognition
├── register.py                     # Capture & save student images
│
├── Data/
│   ├── classes.csv                 # Mapping of classes to professors/TAs
│   ├── Students/
│   │   ├── Details.csv             # Student metadata
│   │   ├── Faces/                  # Saved face datasets
│   ├── Attendance/
│       ├── CLASSNAME_data.xlsx     # Student info + punch times
│       ├── CLASSNAME_attendance.xlsx # Final attendance sheet
│
└── README.md

🛠️ Technologies Used

Python 3.x

OpenCV (face detection & recognition)

Tkinter (GUI)

Pandas (data handling)

OpenPyXL (Excel file writing)

CSV / Excel files for persistent storage

📦 Installation
1️⃣ Clone the repository
git clone <your-repo-url>
cd AttendanceSystem

2️⃣ Install dependencies
pip install opencv-python
pip install pandas
pip install openpyxl

3️⃣ Run the application
python main.py

🧠 How Attendance is Stored
✔ Punch In (_in)

Updates the *_data.xlsx and *_attendance.xlsx files:

Marks students appearing as Present

Others remain Absent

✔ Punch Out (_out)

Finalizes the attendance for the day:

Students who punched in but NOT punched out = A

Only repeated detections = P

✔ Excel Format
student_data.xlsx
AU_id	Name	DATE_in	DATE_out
AU2540001	John Doe	10:02:11	10:58:22
student_attendance.xlsx
AU_id	Name	DATE
AU2540001	John Doe	P
🎥 Face Recognition Flow

Person stands in front of the camera

System detects face

Recognizes student using trained dataset

Logs punch-in/punch-out time

Updates Excel attendance

🔐 Account System

Accounts are stored in CSV with roles:

admin

prof

TA

Each user gets access to limited features depending on role.

📌 Known Limitations

Face recognition accuracy depends on lighting and camera quality

Excel files must be present beforehand (recommended to generate them during class creation)

Duplicate AU IDs may break attendance mapping

🧩 Future Improvements

Replace Excel/CSV with SQLite or Firebase

Improve face recognition model

Add QR code fallback option

Web dashboard

Mobile app support
