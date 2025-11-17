import Initialise
import os
import Scripts.GUI as start
from datetime import datetime
import subprocess


print(f"{datetime.now()}: Initialising")
print(f"{datetime.now()}: ⬇️ Downloading required packages")
Initialise.install_requirements()
print(f"{datetime.now()}: ✅ Downloaded required packages")

print(f"{datetime.now()}: Starting main app")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(BASE_DIR, "Scripts\\GUI.py")
subprocess.run(["python", MAIN_DIR])